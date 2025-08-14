from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from FL.objects.Font import Font

if TYPE_CHECKING:
    from FL.objects.Options import Options

__doc__ = "Support for importing binary fonts. Called from FontLab.Open() and FontLab.OpenFont()."


class FontImporter:
    def __init__(self, font_path: Path, options: Options) -> None:
        self.font_path = font_path
        self.options = options

    def import_font(self) -> Font:
        # TODO: Apply import options when importing a font file.
        raise NotImplementedError(
            "Importing a binary font is not implemented in FakeLab yet"
        )
