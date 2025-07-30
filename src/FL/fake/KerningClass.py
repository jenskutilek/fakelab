from __future__ import annotations

import logging
from re import search
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from FL.fake.Kerning import FakeKerning


logger = logging.getLogger(__name__)


class KerningClass:
    """
    Object representing a kerning class.

    :param name: The class name.
    :type name:  str or None

    :param sides: The sides of the class. "", "L", "R", or "LR".
    :type sides:  str

    :param keyglyph: The name of the class key glyph.
    :type keyglyph:  str or None

    :param glyphs: The class member glyph names.
    :type glyphs:  list of str

    :param fromFLClass: A FontLab kerning class to import from.
    :type fromFLClass:  str or None

    :param parent: The :py:class:`fofa.kerning.KerningCollection`.
    :type parent:  str or None
    """

    def __init__(
        self,
        name: str | None = None,
        sides: str = "",
        keyglyph: str | None = None,
        glyphs: list[str] | None = None,
        fromFLClass: str | None = None,
        parent: FakeKerning | None = None,
    ) -> None:
        self.name = name
        self.sides = sides  # "", "L", "R", "LR"
        self._keyglyph = keyglyph
        self.glyphs = glyphs or []
        self._parent = parent
        if self.keyglyph in self.glyphs:
            self.glyphs.remove(self.keyglyph)
        if fromFLClass:
            self.importFromFontLabClass(fromFLClass)

    def __len__(self) -> int:
        length = len(self.glyphs)
        if self.keyglyph:
            length += 1
        return length

    def __repr__(self) -> str:
        result = f"Kerning class {self.name} ({self.sides})\n"
        result += "  Key: %s\n" % self.keyglyph
        result += "  Glyphs: %s\n\n" % self.glyphs
        return result

    @classmethod
    def fromFontLabClass(cls, flClass: str) -> KerningClass:
        kc = cls()
        kc.importFromFontLabClass(flClass)
        return kc

    @property
    def keyglyph(self) -> str | None:
        """
        Return or set the keyglyph to a glyph name. Setting the keyglyph
        removes that glyph name from the members list.
        """
        return self._keyglyph

    @keyglyph.setter
    def keyglyph(self, value: str | None) -> None:
        if value is None:
            # Key glyph can not be none
            raise ValueError

        if self._keyglyph:
            self.glyphs.append(self._keyglyph)
        self._keyglyph = value
        if self._keyglyph in self.glyphs:
            self.glyphs.remove(self._keyglyph)

    def importFromMMClass(self, mmClass: str) -> None:
        """
        Import the class from a MetricsMachine class.

        :param mmClass: The MM class as string.
        :type mmClass:  str or None
        """
        # Check lfFontTools.kerningClass if you need it
        raise NotImplementedError

    def importFromFontLabClass(self, flClass: str) -> None:
        """
        Builds a new kerning class from an fl.font.classes element string, e.g.
        "_LAT_a_LEFT: a' adieresis".

        Args:
            flClass (str): The FontLab class string

        Raises:
            ValueError: If there is a duplicate key glyph.
        """
        self.name = None
        self.glyphs = []
        self._keyglyph = None

        parts = flClass.split()
        self.name = parts[0][:-1]
        for p in parts[1:]:
            if len(p) > 0:  # ignore multiple spaces in FL class definitions
                if p[-1] == "'":
                    if self._keyglyph is None:
                        self.keyglyph = p[:-1]
                    else:
                        logger.warning(f"Duplicate key glyph in class {self.name}")
                        raise ValueError
                else:
                    self.glyphs.append(p)
        side = self.name.rsplit("_", 1)[-1]
        if side in ("LEFT", "1st", "1"):
            self.sides = "L"
        elif side in ("RIGHT", "2nd", "2"):
            self.sides = "R"
        else:
            self.sides = "LR"
        if self._keyglyph is None:
            # Fallback to first member glyph
            if self.glyphs:
                self.keyglyph = self.glyphs[0]
            else:
                logger.warning("Empty class: %s" % self.name)
                logger.warning("             %s" % flClass)

    def getFontLabExternalClassCode(self) -> str:
        """
        External class code is the format written by FontLab when saving classes from
        the Classes panel.
        """
        if self.sides == "L":
            sideName = "_LEFT"
        elif self.sides == "R":
            sideName = "_RIGHT"
        else:
            sideName = ""
            self.sides = "LR"

        result = f"%%CLASS _{self.name}{sideName}\n"
        result += f"%%GLYPHS {self.keyglyph}' {' '.join(self.glyphs)}\n"
        result += "%%%%KERNING %s 0\n%%%%END\n" % (self.sides)

        return result
