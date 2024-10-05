from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path
    from FL.objects.Font import Font


class VfbToFontReader:
    """
    Instantiate the Font object and all related objects from a `vfbLib.vfb.vfb.Vfb` (I
    know...) object (low-level representation of the binary VFB format)
    """

    def __init__(self, vfb_path: Path) -> None:
        """Load the VFB file from `vfb_path` and instantiate its data into `font`.

        Args:
            vfb_path (Path): The file path from which to load the VFB data
            font (Font): The target object of the data
        """
        self.vfb_path = vfb_path
        self.font = font

    def read_into_font(self, font: Font) -> None:
        pass
