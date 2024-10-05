from __future__ import annotations

from typing import TYPE_CHECKING

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
        pass
