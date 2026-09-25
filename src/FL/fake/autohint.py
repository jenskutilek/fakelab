from itertools import chain
from types import SimpleNamespace
from typing import TYPE_CHECKING

from FL.objects.Hint import Hint
from FL.objects.Replace import TYPE_NODE, Replace
from FL.otfautohint.__main__ import HintOptions
from FL.otfautohint.fdTools import FDDict, kBlueValueKeys, kOtherBlueValueKeys
from FL.otfautohint.glyphData import glyphData
from FL.otfautohint.hinter import glyphHinter

if TYPE_CHECKING:
    from collections.abc import Iterable

    from FL.objects.Font import Font
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


def autohint_glyph(glyph: "Glyph", master_index: int = 0) -> None:
    """
    Autohint a glyph and recalculate the hint masks.

    Args:
        glyph (Glyph): The FLS5 glyph.
    """
    glyph.replace_table.clean()

    if glyph.parent is None:
        raise ValueError(
            f"Can't calculate hint replacements for a glyph witout a font: {glyph.name}"
        )
    # Calculate hint masks

    # Initialize the hinter
    options = fake_HintOptions()
    dr = build_dict_record(glyph.parent)
    glyphHinter.initialize(options, dictRecord=dr)

    # Build glyph data in a format the hinter understands
    glyph_data = glyphData(roundCoords=False, name=glyph.name)
    glyph.fake_draw(glyph_data, master_index)

    # The original glyph_data object is modified after .hint()
    glyphHinter.hint(glyph.name, glyphTuple=(glyph_data,), fdKey=(0, 0))

    # Clear existing hints and links and add auto-generated hints
    glyph.hlinks.clean()
    glyph.hhints.clean()
    for y0, y1 in glyph_data.hstems:
        hint = Hint(y0, y1 - y0)
        glyph.hhints.append(hint)

    glyph.vlinks.clean()
    glyph.vhints.clean()
    for x0, x1 in glyph_data.vstems:
        hint = Hint(x0, x1 - x0)
        glyph.vhints.append(hint)

    # Transfer hint sets from the glyph_data object to the Glyph

    current_mask = glyph_data.startmasks
    if current_mask is None:
        # Hints don't overlap, remove hint replacement flag
        clear_hint_replacement_flag(glyph)
    else:
        node_index = 0
        for subpath in glyph_data.subpaths:
            for path_element in subpath:
                if current_mask is not None:
                    if node_index != 0:
                        glyph.replace_table.append(Replace(TYPE_NODE, node_index))
                    hintmask_hints: list[tuple[int, int]] = []
                    for i, hintmask in enumerate(current_mask):
                        for hint_index, hint_is_active in enumerate(hintmask):
                            if hint_is_active:
                                hintmask_hints.append((i + 1, hint_index))
                    # The order of hints for each hintmask is arbitrary, but we sort
                    # the hints for compatibility
                    for r_type, r_index in sorted(hintmask_hints):
                        glyph.replace_table.append(Replace(r_type, r_index))
                current_mask = path_element.masks
                node_index += 1

    # print([(r.type, r.index) for r in glyph.replace_table])

    # Set green hint replacement flag
    set_hint_replacement_flag_ok(glyph)


def autoreplace_glyph(glyph: "Glyph", master_index: int = 0) -> None:
    glyph.replace_table.clean()

    # Check if any hints overlap
    if do_hints_overlap(glyph.hhints) or do_hints_overlap(glyph.vhints):
        # TODO: Do the actual hint replacement calculations
        raise NotImplementedError

        # Set green hint replacement flag
        set_hint_replacement_flag_ok(glyph)
    else:
        # Hints don't overlap, remove hint replacement flag
        clear_hint_replacement_flag(glyph)


def clear_hint_replacement_flag(glyph: "Glyph") -> None:
    # TODO: Move to Glyph?
    if "hint_replacement" in glyph._glyph_hinting_options:
        del glyph._glyph_hinting_options["hint_replacement"]


def set_hint_replacement_flag_ok(glyph: "Glyph") -> None:
    # TODO: Move to Glyph?
    # Set green hint replacement flag
    glyph._glyph_hinting_options["hint_replacement"] = 1
    if "other" in glyph._glyph_hinting_options:
        opts = glyph._glyph_hinting_options["other"]
        if 28 in opts:
            opts.remove(28)


def build_dict_record(
    font: "Font", master_index: int = 0
) -> dict[int, dict[int, list[FDDict]]]:
    fddict = FDDict(fdIndex=0, fontName=font.font_name)
    for key, value in (
        ("LanguageGroup", 0),  # 1 if the glyphs are ideographic, else 0.
        ("OrigEmSqUnits", font.upm),
        ("DominantV", font.stem_snap_v[master_index]),
        ("DominantH", font.stem_snap_h[master_index]),
        (
            "VCounterChars",
            {
                "m": False,
                "M": False,
                "T": False,
                "ellipsis": False,
            },
        ),
        (
            "HCounterChars",
            {
                "element": False,
                "equivalence": False,
                "notelement": False,
                "divide": False,
            },
        ),
        ("FlexOK", True),  # TODO: can this be controlled in VFB?
        ("BlueFuzz", font.blue_fuzz[master_index]),
    ):
        fddict.setInfo(key, value)

    # From otfautohint.ufoFont.getPrivateFDDict():
    # Set values for BlueValues and OtherBlues

    blue_values = font.blue_values[master_index].copy()  # Don't modify the font
    num_blue_values = len(blue_values)
    if num_blue_values < 4:
        raise ValueError(
            "Font must have at least four values in its BlueValues array for otfautohint to work!"
        )
    blue_values.sort()
    # The first pair only is a bottom zone, where the first value is the
    # overshoot position; the rest are top zones, and second value of the
    # pair is the overshoot position.
    blue_values[0] = blue_values[0] - blue_values[1]
    for i in range(3, num_blue_values, 2):
        blue_values[i] = blue_values[i] - blue_values[i - 1]
    num_blue_values = min(num_blue_values, len(kBlueValueKeys))
    for i in range(num_blue_values):
        key = kBlueValueKeys[i]
        value = blue_values[i]
        fddict.setInfo(key, value)

    other_blues = font.other_blues[master_index].copy()  # Don't modify the font
    num_other_blues = len(other_blues)

    if num_other_blues > 0:
        other_blues.sort()
        for i in range(num_other_blues, 2):
            other_blues[i] = other_blues[i] - other_blues[i + 1]
        num_other_blues = min(num_other_blues, len(kOtherBlueValueKeys))
        for i in range(num_other_blues):
            key = kOtherBlueValueKeys[i]
            value = other_blues[i]
            fddict.setInfo(key, value)

    # Build and return the complete dict
    return {0: {0: [fddict]}}


def build_glyph_data(glyph: "Glyph", master_index: int = 0) -> glyphData:
    """
    Convert the FL Glyph to glyphData so otfautohint can handle it.

    Args:
        glyph (Glyph): The FL Glyph.

    Returns:
        glyphData: The glyph as glyphData.
    """
    glyph_data = glyphData(roundCoords=False, name=glyph.name)
    glyph.fake_draw(glyph_data, master_index)
    return glyph_data


def fake_HintOptions():
    pargs = SimpleNamespace()
    pargs.font_paths = None
    pargs.output_paths = None
    pargs.reference_font = None
    pargs.reference_out = None
    pargs.hint_all_ufo = True
    pargs.allow_changes = True
    pargs.no_flex = False
    pargs.no_hint_sub = False
    pargs.no_zones_stems = False
    pargs.ignore_fontinfo = False
    pargs.report_only = False
    pargs.keep_conflicts = False
    pargs.print_list_fddict = False
    pargs.print_all_fddict = False
    pargs.decimal = False  # round coordinates
    pargs.write_to_default_layer = True
    pargs.max_segments = 100
    pargs.verbose = True
    pargs.loose_overlap_mapping = True
    pargs.force_overlap = False
    pargs.force_no_overlap = False
    pargs.processes = 1
    options = HintOptions(pargs)
    return options
