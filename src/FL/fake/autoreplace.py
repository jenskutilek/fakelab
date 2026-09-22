from itertools import chain
from typing import TYPE_CHECKING

from FL.objects.Hint import Hint
from FL.objects.Replace import (
    TYPE_HORIZONTAL_HINT,
    TYPE_NODE,
    TYPE_VERTICAL_HINT,
    Replace,
)
from FL.otfautohint.hinter import glyphHinter

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
        # for node_index, node in enumerate(glyph.nodes):
        #     print(node_index, node)
        #     for hint_index, h in enumerate(glyph.hhints):
        #         if h.position == node.y or h.position + h.width == node.y:
        #             hint_sets.append((TYPE_HORIZONTAL_HINT, hint_index))
        #     for hint_index, v in enumerate(glyph.vhints):
        #         if v.position == node.x or v.position + v.width == node.x:
        #             hint_sets.append((TYPE_VERTICAL_HINT, hint_index))
        #     # FIXME

        # Set green hint replacement flag
        glyph._glyph_hinting_options["hint_replacement"] = 1
        if "other" in glyph._glyph_hinting_options:
            opts = glyph._glyph_hinting_options["other"]
            if 28 in opts:
                opts.remove(28)
    else:
        # Remove hint replacement flag
        if "hint_replacement" in glyph._glyph_hinting_options:
            del glyph._glyph_hinting_options["hint_replacement"]

    # Add calculated data to the glyph
    glyph._replace_table.clean()
    for type, index in hint_sets:
        glyph.replace_table.append(Replace(type, index))
