from typing_extensions import TypedDict


class TTCommandDict(TypedDict):
    name: str
    params: list[str]


TT_COMMANDS: dict[int, TTCommandDict] = {
    # 0x00: {"name": "Nothing"},
    0x01: {"name": "AlignTop", "params": ["pt", "zone"]},
    0x02: {"name": "AlignBottom", "params": ["pt", "zone"]},
    0x03: {
        "name": "SingleLinkH",
        "params": ["pt1", "pt2", "stem", "align"],
    },
    0x04: {
        "name": "SingleLinkV",
        "params": ["pt1", "pt2", "stem", "align"],
    },
    0x05: {
        "name": "DoubleLinkH",
        "params": ["pt1", "pt2", "stem"],
    },
    0x06: {
        "name": "DoubleLinkV",
        "params": ["pt1", "pt2", "stem"],
    },
    0x07: {"name": "AlignH", "params": ["pt", "align"]},
    0x08: {"name": "AlignV", "params": ["pt", "align"]},
    # 0x09: {"name": "PointToRingH"},
    # 0x0A: {"name": "PointToRingV"},
    # 0x0B: {"name": "RingToGridH"},
    # 0x0C: {"name": "RingToGridV"},
    0x0D: {
        "name": "InterpolateH",
        "params": ["pti", "pt1", "pt2", "align"],
    },
    0x0E: {
        "name": "InterpolateV",
        "params": ["pti", "pt1", "pt2", "align"],
    },
    # 0x0F: {"name": "PointToRingXY"},
    # 0x10: {"name": "RingLinkH"},
    # 0x11: {"name": "RingLinkV"},
    # 0x12: {"name": "RingInterpolateH"},
    # 0x13: {"name": "RingInterpolateV"},
    0x14: {
        "name": "MDeltaH",
        "params": ["pt", "shift", "ppm1", "ppm2"],
    },
    0x15: {
        "name": "MDeltaV",
        "params": ["pt", "shift", "ppm1", "ppm2"],
    },
    0x16: {
        "name": "FDeltaH",
        "params": ["pt", "shift", "ppm1", "ppm2"],
    },
    0x17: {
        "name": "FDeltaV",
        "params": ["pt", "shift", "ppm1", "ppm2"],
    },
}

# TT command names to constants
TT_COMMAND_CONSTANTS = {v["name"]: k for k, v in TT_COMMANDS.items()}
