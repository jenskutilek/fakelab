from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vfbLib.typing import PSInfoDict


def get_default_ps_info() -> PSInfoDict:
    return {
        "font_matrix": (0.001, 0.0, 0.0, 0.001, 0.0, 0.0),
        "force_bold": 0,
        "blue_values": [],  # max 14
        "other_blues": [],  # max 10
        "family_blues": [],  # max 14
        "family_other_blues": [],  # max 10
        "blue_scale": 0.039625,
        "blue_shift": 7,
        "blue_fuzz": 1,
        "std_hw": 100,
        "std_vw": 50,
        "stem_snap_h": [],  # max 12
        "stem_snap_v": [],  # max 12
        "bounding_box": {
            "xMin": 32767,
            "yMin": 32767,
            "xMax": -32767,
            "yMax": -32767,
        },
        "adv_width_min": 0,
        "adv_width_max": 0,
        "adv_width_avg": 500,
        "ascender": 750,
        "descender": -250,
        "x_height": 500,
        "cap_height": 700,
    }
