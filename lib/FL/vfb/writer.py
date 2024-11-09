from __future__ import annotations

# from fontTools.misc.textTools import deHexStr, hexStr
from typing import TYPE_CHECKING
from vfbLib.vfb.entry import VfbEntry
from vfbLib.vfb.header import VfbHeader
from vfbLib.vfb.vfb import Vfb

if TYPE_CHECKING:
    from pathlib import Path
    from FL.objects.Font import Font


class FontToVfbWriter:
    """
    Convert the Font object to the low-level `vfbLib.vfb.vfb.Vfb` structure and write it
    to `vfb_path`
    """

    def __init__(self, font: Font, vfb_path: Path) -> None:
        """Save the `font` into the VFB file at `vfb_path`.

        Args:
            font (Font): The source object of the data
            vfb_path (Path): The file path to which to write the VFB data
        """
        self.vfb_path = vfb_path
        self.font = font
        self.vfb = Vfb()
        self.compile()
        self.vfb.write(self.vfb_path)

    def compile(self) -> None:
        self.compile_header()
        self.compile_encoding()

    def compile_encoding(self) -> None:
        for i in range(len(self.font.encoding)):
            e = VfbEntry(self.vfb)
            e.id = 1500
            e.decompiled = [i, self.font.encoding[i].name]
            self.vfb.entries.append(e)
        e = VfbEntry(self.vfb)

        # We don't know what this does exactly:
        e.id = 1502
        e.decompiled = 0x0000
        self.vfb.entries.append(e)

    def compile_header(self) -> None:
        header = self.vfb.header = VfbHeader()
        header.decompiled = {
            "header0": 26,
            "filetype": "WLF10",
            "header1": 3,
            "header2": 44,
            "reserved": (
                "0000000000000000000000000000000000"
                "0000000000000000000000000000000000"
            ),
            "header3": 1,
            "header4": 0,
            "header5": 4,
            "header6": 0,
            "header7": 10,
            "header8": 11,
            "header9": {"1": 1},
            "header10": {"2": 84017792},
            "header11": {"3": 0},
            "header12": 0,
            "header13": 262,
            "header14": 0,
        }
        header.modified = True
