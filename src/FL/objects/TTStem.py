from __future__ import annotations

from FL.fake.Base import Copyable


class TTStem(Copyable):
    """
    TTStem - class to represent TrueType-Stem

    TTStem.__doc__ reports only 'TTStem' ... so use this information with care
    """

    __slots__ = ["_name", "_width", "_ppm2", "_ppm3", "_ppm4", "_ppm5", "_ppm6"]

    # Constructor

    def __init__(
        self, ttstem_or_width: TTStem | int | None = None, upm: int | None = None
    ) -> None:
        self._name = ""
        self._width = 0
        self._ppm2 = 0
        self._ppm3 = 0
        self._ppm4 = 0
        self._ppm5 = 0
        self._ppm6 = 0
        if ttstem_or_width is not None:
            if isinstance(ttstem_or_width, TTStem):
                self._copy_constructor(ttstem_or_width)
            else:
                # fill in ppm steps based on width and upm
                if upm is None:
                    raise RuntimeError("Stem is expected in arg 1: TTStem(TTStem)")
                self.fake_recalc_ppms(ttstem_or_width, upm)

    def __repr__(self) -> str:
        return f"<TTStem: ppms: {self.ppm2}, {self.ppm3}, {self.ppm4}, {self.ppm5}, {self.ppm6}>"

    # FakeLab additions

    def fake_recalc_ppms(self, width: int, upm: int) -> None:
        """
        Calculate the ppms at which the scaled stem width will round up to the next pixel

        Args:
            width (int): The width of the stem
            upm (int): The units per em of the font
        """
        self.width = width
        self.ppm2 = int(upm // self.width * 1.5)
        self.ppm3 = int(upm // self.width * 2.5)
        self.ppm4 = int(upm // self.width * 3.5)
        self.ppm5 = int(upm // self.width * 4.5)
        self.ppm6 = int(upm // self.width * 5.5)

    # Attributes

    @property
    def name(self) -> str:
        """
        Name of the stem

        Returns:
            str: _description_
        """
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def width(self) -> int:
        """
        Width of the stem

        Returns:
            int: _description_
        """
        return self._width

    @width.setter
    def width(self, value: int) -> None:
        self._width = value

    # What about ppm1? It is stored in the VFB, but in a different entry, so it is
    # probably a later addition that didn't get added to the Python API.

    @property
    def ppm2(self) -> int:
        """
        From this ppm-size the stem becomes 2 pixels wide

        Returns:
            int: _description_
        """
        return self._ppm2

    @ppm2.setter
    def ppm2(self, value: int) -> None:
        self._ppm2 = value

    @property
    def ppm3(self) -> int:
        """
        From this ppm-size the stem becomes 3 pixels wide

        Returns:
            int: _description_
        """
        return self._ppm3

    @ppm3.setter
    def ppm3(self, value: int) -> None:
        self._ppm3 = value

    @property
    def ppm4(self) -> int:
        """
        From this ppm-size the stem becomes 4 pixels wide

        Returns:
            int: _description_
        """
        return self._ppm4

    @ppm4.setter
    def ppm4(self, value: int) -> None:
        self._ppm4 = value

    @property
    def ppm5(self) -> int:
        """
        From this ppm-size the stem becomes 5 pixels wide

        Returns:
            int: _description_
        """
        return self._ppm5

    @ppm5.setter
    def ppm5(self, value: int) -> None:
        self._ppm5 = value

    @property
    def ppm6(self) -> int:
        """
        From this ppm-size the stem becomes 6 pixels wide

        Returns:
            int: _description_
        """
        return self._ppm6

    @ppm6.setter
    def ppm6(self, value: int) -> None:
        self._ppm6 = value

    # Operations

    # (don't know)

    # Methods

    # (don't know)
