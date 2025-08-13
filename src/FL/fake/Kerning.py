from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from FL.fake.KerningClass import KerningClass

if TYPE_CHECKING:
    from pathlib import Path

    from FL.objects.Font import Font


logger = logging.getLogger(__name__)


__doc__ = """
Base class for Kerning
"""


class FakeKerning:
    def __init__(self, font: Font | None = None) -> None:
        self._font = font
        # self.num_masters: int = 0
        # self.upm: int | None = None
        self.reset_classes()
        self.reset_pairs()

    def __len__(self) -> int:
        """
        Return the number of key pairs.

        Returns:
            int: The number of kerning pairs. Key and exception pairs only.
        """
        return len(self.kerning)

    def _expand(self) -> None:
        """
        Expand class-based kerning to flat kerning.
        """
        if self._font is None:
            raise ValueError

        self.flat_kerning = []
        cc = []  # Class-class pairs
        gc = []  # Glyph-class pairs
        cg = []  # Class-glyph pairs
        gg = []  # Glyph-glyph pairs
        for g in self._font.glyphs:
            for kerning_pair in g.kerning:
                value = kerning_pair.value
                if value == 0:
                    continue
                L = g.name
                R = self._font.glyphs[kerning_pair.key].name
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

    def expand(self) -> None:
        if self._font is None:
            logger.error("You need to supply a font before you can expand the kerning")
            return

        self.import_classes_from_font(self._font)
        self._expand()

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

    def export_flc(self, file_path: Path) -> None:
        raise NotImplementedError

    def import_afm(self, file_path: Path, master_index: int = 0) -> None:
        """
        Import kerning data from an AFM file at `file_path`.

        Args:
            file_path (Path): The path to the AFM file.
            master_index (int, optional): _description_. Defaults to 0.
        """
        raise NotImplementedError

    def import_classes_from_font(self, font: Font) -> None:
        """
        Import the kerning classes from a font.

        Args:
            font (Font): The font to import from.
        """
        self.reset_classes()
        for i, flclass in enumerate(font.classes):
            if not flclass.strip().startswith("_"):
                # Not a kerning class
                continue

            kc = KerningClass(fromFLClass=flclass)

            if len(kc) == 0:
                print(f"Skipping empty class: {kc}")
                continue

            if kc.keyglyph is None:
                print(f"Skipping class without keyglyph: {kc.name}")
                continue

            # Override the sides deduced from the class name
            sides = ""
            if font.GetClassLeft(i):
                sides += "L"
            if font.GetClassRight(i):
                sides += "R"
            kc.sides = sides

            if "L" in kc.sides:
                self.classes_left[kc.keyglyph] = kc

            if "R" in kc.sides:
                self.classes_right[kc.keyglyph] = kc

    def import_flc(self, file_path: Path) -> None:
        """
        Import the kerning classes from a FLC file.

        Args:
            file_path (Path): The path to the FLC file.
        """
        self.reset_classes()
        with open(file_path, "r") as flc:
            class_name = None
            class_glyphs = None
            class_sides = None
            for i, line in enumerate(flc):
                line = line.strip()
                if line.startswith("%%CLASS "):
                    class_name = line.split()[-1]
                if line.startswith("%%GLYPHS "):
                    _, class_glyphs = line.split(maxsplit=1)
                if line.startswith("%%KERNING"):
                    class_sides = line.split()[1]
                if line.startswith("%%END"):
                    if class_name is None:
                        logger.error(f"Skipping class without name in line {i}")
                        class_name = None
                        class_glyphs = None
                        class_sides = None
                        continue

                    if class_sides is None:
                        # Classes without side don't kern in FL
                        # Or they may be non-kerning classes; skip them
                        if class_name.startswith("_"):
                            logger.warning(
                                f"Skipping class without side flags: {class_name}"
                            )
                        class_glyphs = None
                        class_name = None
                        class_sides = None
                        continue

                    kc = KerningClass.fromFontLabClass(f"{class_name}: {class_glyphs}")
                    kc.sides = class_sides
                    if kc.keyglyph is None:
                        # Take the first glyph as keyglyph, if any
                        if kc.glyphs:
                            kc.keyglyph = kc.glyphs[0]
                            logger.warning(
                                f"Class without keyglyph: {class_name}, assuming first "
                                f"glyph is key ({kc.keyglyph})"
                            )
                        else:
                            logger.warning(f"Skipping empty class: {class_name}")
                            class_glyphs = None
                            class_name = None
                            class_sides = None
                            continue

                    if "L" in class_sides:
                        self.classes_left[kc.keyglyph] = kc

                    if "R" in class_sides:
                        self.classes_right[kc.keyglyph] = kc

                    # Clean up for the next class
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

    def reset_pairs(self) -> None:
        self.kerning: dict[tuple[str, str], list[int]] = {}
        self.flat_kerning: list[tuple[str, str, int]] = []
