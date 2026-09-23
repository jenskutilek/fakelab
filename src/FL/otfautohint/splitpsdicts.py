# Copyright 2022 Adobe. All rights reserved.

import argparse
import logging
import plistlib
import re
import sys
from copy import deepcopy

from afdko.fdkutils import (
    get_temp_file_path,
    run_shell_command,
    validate_path,
)
from fontTools.cffLib import FDArrayIndex, FDSelect, FontDict, PrivateDict
from fontTools.designspaceLib import DesignSpaceDocument
from fontTools.ttLib import TTFont

logger = logging.getLogger(__name__)


class ShellCommandError(Exception):
    pass


def replaceCFF(otfPath: str, tempFilePath: str) -> None:
    if not run_shell_command(["sfntedit", "-a", f"CFF ={tempFilePath}", otfPath]):
        raise ShellCommandError


def get_options(args: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-m",
        "--metadata",
        dest="metaPath",
        type=validate_path,
        help="path to hinting metadata file",
        required=True,
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-d",
        "--designspace",
        dest="dsPath",
        type=validate_path,
        help="path to design space file",
    )
    group.add_argument(
        "-f",
        "--fontpath",
        dest="fPath",
        type=validate_path,
        help="path to individual OTF font to modify",
    )
    options = parser.parse_args(args)

    return options


class Dictspec:
    name: str
    re: list[re.Pattern]
    BluePairs: list[int]
    OtherPairs: list[int]
    SIV: list[int]
    SIH: list[int]
    foundGlyph: bool


def getDictmap(options: argparse.Namespace) -> list[Dictspec]:
    with open(options.metaPath, "rb") as dictmapfile:
        rawdictmap = plistlib.load(dictmapfile)

    dictmap = []
    for name, d in rawdictmap.items():
        dct = Dictspec()
        dct.name = name
        dct.BluePairs = d.get("blue_pairs", [])
        dct.OtherPairs = d.get("other_blue_pairs", [])
        dct.SIV = d.get("stem_indexes_v", [])
        dct.SIH = d.get("stem_indexes_h", [])
        dct.re = []
        for r in d.get("regex", []):
            dct.re.append(re.compile(r))
        dct.foundGlyph = False
        dictmap.append(dct)

    return dictmap


def remapDicts(fpath: str, dictmap: list[Dictspec]) -> None:
    f = TTFont(fpath)
    if "CFF " not in f:
        logger.error(f"No CFF table in {fpath}: will not modify")
        return

    cff = f["CFF "]
    top = cff.cff[0]
    if hasattr(top, "FDArray"):
        logger.error(
            f"CFF table in {fpath} already has {len(top.FDArray)} private dicts: will not modify"
        )
        return

    hasExtra = False

    # Create a new FDSelect object for the font and map the glyphs to
    # dictionary indexes according to the regular expressions in
    # Dictspec.re
    fdselect = top.FDSelect = FDSelect()
    for gn in cff.getGlyphOrder():
        done = False
        for i, dictspec in enumerate(dictmap):
            for r in dictspec.re:
                if r.search(gn):
                    fdselect.append(i)
                    dictspec.foundGlyph = True
                    done = True
                    break
            if done:
                break
        if not done:
            fdselect.append(i + 1)
            hasExtra = True

    # Rebuild the dictionary indices and the dictmap itself to remove
    # any dictionaries that didn't contain any glyphs, so that we don't
    # wind up with empty dictionaries later.
    j = 0
    indexMap = []
    newdictmap: list[Dictspec] = []
    for dictspec in dictmap:
        if dictspec.foundGlyph:
            newdictmap.append(dictspec)
            indexMap.append(j)
            j += 1
        else:
            logger.warning(f"No glyphs found for entry {dictspec.name}, skipping")
            indexMap.append(-1)
    if hasExtra:
        indexMap.append(j)

    for i, v in enumerate(fdselect):
        assert indexMap[v] != -1
        fdselect[i] = indexMap[v]

    # Create new FDArray and top-level private dictionaries, keeping
    # a reference to the original private dictionary in origPriv
    fdarray = top.FDArray = FDArrayIndex()
    origPriv = top.Private
    # Make sure info doesn't leak though in non-FDArray private dict
    top.Private = PrivateDict()

    # For each dictionary containing glyphs, make a copy of the original
    # private dictionary and then modify the Other/Family/Blues, StemSnap,
    # and Std?W values according to the dictspec. (Note that by assigning
    # to blah[:] the new values wind up in the lists inside the dictionary
    # copy.)
    #
    # Then add that dictionary to a new FontDict and append the later
    # to the fdarray.
    for dictspec in newdictmap:
        # Make a new dictonary starting with the old private dictionary
        # values
        npr = deepcopy(origPriv)
        for bvals, fvals, indexes in [
            (
                getattr(npr, "BlueValues", None),
                getattr(npr, "FamilyBlues", None),
                dictspec.BluePairs,
            ),
            (
                getattr(npr, "OtherBlues", None),
                getattr(npr, "FamilyOtherBlues", None),
                dictspec.OtherPairs,
            ),
        ]:
            nbvals = []
            nfvals = []
            for pi in sorted(indexes):
                if bvals:
                    nbvals.extend([bvals[2 * pi], bvals[2 * pi + 1]])
                if fvals:
                    nfvals.extend([fvals[2 * pi], fvals[2 * pi + 1]])
            if bvals:
                bvals[:] = nbvals
            if fvals:
                fvals[:] = nfvals
        snapvs = getattr(npr, "StemSnapV", None)
        if snapvs is not None:
            npr.StemSnapV[:] = [snapvs[i] for i in dictspec.SIV]
            npr.StdVW = npr.StemSnapV[0]
        elif getattr(npr, "StdVW", None) is None:
            logger.error("No StemSnapV or StdVW in combined dict")

        snaphs = getattr(npr, "StemSnapH", None)
        if snaphs is not None:
            npr.StemSnapH[:] = [snaphs[i] for i in dictspec.SIH]
            npr.StdHW = npr.StemSnapH[0]
        elif getattr(npr, "StdHW", None) is None:
            logger.error("No StemSnapH or StdHW in combined dict")

        fontDict = FontDict()
        fontDict.setCFF2(True)
        fontDict.Private = npr
        fdarray.append(fontDict)

    # Add a dictionary for any remaining glyphs with zones far outside of
    # the bounds of existing glyphs. (Leave the stem values.)
    if hasExtra:
        bbox = top.FontBBox
        font_max = bbox[3]
        font_min = bbox[1]
        npr = deepcopy(fdarray[0].Private)  # To get reasonable stem values
        npr.BlueValues[:] = [
            font_min - 100,
            font_min - 85,
            font_max + 85,
            font_max + 100,
        ]
        if hasattr(npr, "FamilyBlues"):
            npr.FamilyBlues[:] = [
                font_min - 100,
                font_min - 85,
                font_max + 85,
                font_max + 100,
            ]
        if hasattr(npr, "OtherBlues"):
            npr.OtherBlues[:] = []
        if hasattr(npr, "FamilyOtherBlues"):
            npr.FamilyOtherBlues[:] = []
        fontDict = FontDict()
        fontDict.setCFF2(True)
        fontDict.Private = npr
        fdarray.append(fontDict)

    numdicts = len(newdictmap) + 1 if hasExtra else 0

    logger.warning(f"Updating {fpath} with {numdicts} dictionaries")
    cfftpath = get_temp_file_path()
    with open(cfftpath, "w+b") as cfftfile:
        cff.cff.compile(cfftfile, f, False)
    f.close()

    replaceCFF(fpath, cfftpath)


def main(args: list[str] | None = None) -> int:
    options = get_options(args)

    dictmap = getDictmap(options)

    if options.dsPath is not None:
        ds = DesignSpaceDocument.fromfile(options.dsPath)
        otf_paths = [s.path.replace(".ufo", ".otf") for s in ds.sources]
    else:
        otf_paths = [options.fPath]

    for p in otf_paths:
        remapDicts(p, dictmap)

    return 0


if __name__ == "__main__":
    sys.exit(main())
