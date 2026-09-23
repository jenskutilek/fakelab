from itertools import chain
from typing import TYPE_CHECKING

from ufoLib2 import Font as UFOFont
from ufoLib2.objects.glyph import Glyph as UFOGlyph

from FL.objects.Hint import Hint
from FL.objects.Replace import (
    TYPE_HORIZONTAL_HINT,
    TYPE_NODE,
    TYPE_VERTICAL_HINT,
    Replace,
)
from FL.otfautohint.autohint import FontInstance, fontWrapper
from FL.otfautohint.hinter import glyphHinter
from FL.otfautohint.ufoFont import UFOFontData

if TYPE_CHECKING:
    from collections.abc import Iterable

    from FL.objects.Glyph import Glyph


def do_hints_overlap(hints: "Iterable[Hint]") -> bool:
    """
    Check whether the hints in the iterable overlap.

    Args:
        hints (Iterable[Hint]): The hints.

    Returns:
        bool: Whether any hints overlap.
    """
    hint_tuples = sorted(
        [sorted((hint.position, hint.position + hint.width)) for hint in hints]
    )
    hint_values = list(chain.from_iterable(hint_tuples))
    hint_values_unique = set(hint_values)
    if len(hint_values) != len(hint_values_unique):
        return True
    return hint_values != sorted(hint_values_unique)


def autoreplace_glyph(glyph: "Glyph") -> None:
    """
    Recalculate the hint masks for a glyph.

    Args:
        glyph (Glyph): The FLS5 glyph.
    """
    hint_sets = []

    # Check if any hints overlap
    if do_hints_overlap(glyph.hhints) or do_hints_overlap(glyph.vhints):
        # Calculate hint masks
        options = HintOptions()
        glyphHinter.initialize(options, dictRecord={})
        # Construct a single glyph UFO
        ufo = UFOWrapper()
        ufo_glyph = UFOGlyph(glyph.name)
        pen = ufo_glyph.getPointPen()
        glyph.fake_drawPoints(pen)
        ufo.addGlyph(ufo_glyph)

        inst = FontInstance(font=ufo, inpath="Memory", outpath=None)
        fw = fontWrapper(options, fil=[inst])
        r = glyphHinter.hint(glyph.name, glyphTuple=[], fdKey=None)
        print(r)

        # Set green hint replacement flag
        glyph._glyph_hinting_options["hint_replacement"] = 1
        if "other" in glyph._glyph_hinting_options:
            opts = glyph._glyph_hinting_options["other"]
            if 28 in opts:
                opts.remove(28)
    else:
        # Hints don't overlap, remove hint replacement flag
        if "hint_replacement" in glyph._glyph_hinting_options:
            del glyph._glyph_hinting_options["hint_replacement"]

    # Add calculated data to the glyph
    glyph._replace_table.clean()
    for type, index in hint_sets:
        glyph.replace_table.append(Replace(type, index))


class UFOWrapper(UFOFont):
    def getPSName(self) -> str:
        return "TemporaryUfo"

    def getGlyphList(self) -> list[str]:
        return [g.name for g in self]

    def isVF(self) -> bool:
        return False

    def getInputPath(self) -> str:
        return "Memory"


class HintOptions:
    def __init__(self) -> None:
        self.logOnly = False
        self.removeConflicts = True
        self.verbose = True
        self.glyphList = None
        self.fontinfoPath = None

    def justReporting(self) -> bool:
        return True


class GlyphHintReplacer(glyphHinter):
    pass
