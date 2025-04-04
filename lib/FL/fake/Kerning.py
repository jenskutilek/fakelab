from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from FL import Font


logger = logging.getLogger(__name__)


class FakeKerning:
    def __init__(self, font: Font | None = None) -> None:
        self._font = font
        # self.num_masters: int = 0
        # self.upm: int | None = None
        self.reset_classes()
        self.kerning: dict[tuple[str, str], list[int]] = {}
        self.flat_kerning: list[tuple[str, str, int]] = []

    def __len__(self) -> int:
        return len(self.kerning)

    def expand(self) -> None:
        """
        Expand class-based kerning to flat kerning.
        """
        if self._font is None:
            raise ValueError

        self.flat_kerning = []
        glyphs = self._font.glyphs
        cc = []  # Class-class pairs
        gc = []  # Glyph-class pairs
        cg = []  # Class-glyph pairs
        gg = []  # Glyph-glyph pairs
        for i, g in enumerate(glyphs):
            for kerning_pair in g.kerning:
                value = kerning_pair.value
                if value == 0:
                    continue
                L = g.name
                R = glyphs[kerning_pair.key].name
                l_class = self.classes_left.get(L, None)
                r_class = self.classes_right.get(R, None)
                if l_class:
                    if r_class:
                        cc.append((l_class, r_class, value))
                    else:
                        cg.append((l_class, R, value))
                else:
                    if r_class:
                        gc.append((L, r_class, value))
                    else:
                        gg.append((L, R, value))

        pairs = {}
        for l_class, r_class, value in cc:
            for L in [l_class.keyglyph] + list(l_class.glyphs):
                for R in [r_class.keyglyph] + list(r_class.glyphs):
                    pairs[(L, R)] = value
        for l_class, R, value in cg:
            for L in [l_class.keyglyph] + list(l_class.glyphs):
                pairs[(L, R)] = value
        for L, r_class, value in gc:
            for R in [r_class.keyglyph] + list(r_class.glyphs):
                pairs[(L, R)] = value
        for L, R, value in gg:
            pairs[(L, R)] = value
        self.flat_kerning = sorted([(g[0], g[1], v) for g, v in pairs.items()])
        logger.info("Expanded kerning: %i pairs." % len(self.flat_kerning))

    def export_afm(self, file_path: Path, expand: bool = True) -> None:
        """
        Export kerning data to an AFM file at `file_path`.

        Args:
            file_path (Path): The path to the AFM file.
            expand (bool, optional): Whether to expand class kerning before export.
                If `False`, only key and exception pairs will be exported. Defaults to
                True.
        """
        if expand:
            self.expand()
        raise NotImplementedError

    def import_afm(self, file_path: Path) -> None:
        """
        Import kerning data from an AFM file at `file_path`.

        Args:
            file_path (Path): The path to the AFM file.
        """
        raise NotImplementedError

    def import_classes(self, file_path: Path) -> None:
        """
        Import the kerning classes from an FLC file.

        Args:
            file_path (Path): The path to the FLC file.
        """
        self.classes = []
        self.class_sides = {}
        with open(file_path, "r") as flc:
            class_name = None
            class_glyphs = None
            class_sides = None
            for line in flc:
                line = line.strip()
                if line.startswith("%%CLASS "):
                    class_name = line.split()[-1]
                if line.startswith("%%GLYPHS "):
                    class_glyphs = line.split()[1:]
                if line.startswith("%%KERNING"):
                    class_sides = line.split()[1]
                if line.startswith("%%END"):
                    if class_name is not None:
                        if class_sides is None:
                            # Classes without side don't kern in FL
                            # Or they may be non-kerning classes; skip them
                            if class_name.startswith("_"):
                                logger.warning(
                                    f"Class without side flags: {class_name}"
                                )
                            class_glyphs = None
                            class_name = None
                            class_sides = None
                            continue
                        else:
                            self.class_sides[class_name] = class_sides
                        if class_glyphs:
                            self.classes.append(
                                f"{class_name}: {' '.join(class_glyphs)}"
                            )
                        else:
                            # Empty class
                            self.classes.append(f"{class_name}:")
                        class_glyphs = None
                        class_name = None
                        class_sides = None

    def reset_classes(self) -> None:
        """
        Reset kerning classes to empty dicts.
        """
        self.classes: dict[str, dict[str, KerningClass]] = {"L": {}, "R": {}}
        self.classes_left: dict[str, KerningClass] = self.classes["L"]
        self.classes_right: dict[str, KerningClass] = self.classes["R"]
