from __future__ import annotations

from FL.fake.Base import Copyable


class TTGasp(Copyable):
    """
    This class is completely undocumented
    """

    __slots__ = ["_ppm", "_behavior"]

    def __init__(self, ttgasp_or_ppm: TTGasp | int | None = None, behavior: int = 0):
        """
        A gasp table record.

        Args:
            ttgasp_or_ppm (TTGasp | int | None, optional): Copy attributes from
                `TTGasp`, set the ppm, or create a default gasp table record. Defaults
                to None.
            behavior (int, optional): The behavior flags for the ppm range. Must be used
                together with the ppm integer in the first argument. Defaults to 0.

        Raises:
            RuntimeError: When the arguments don't match the expectations.
        """
        self.ppm = 1000
        self.behavior = behavior
        if ttgasp_or_ppm is not None:
            if isinstance(ttgasp_or_ppm, TTGasp):
                self._copy_constructor(ttgasp_or_ppm)
            else:
                if not isinstance(behavior, int):
                    raise RuntimeError("Gasp is expected in arg 1: TTGasp(TTGasp)")
                self.ppm = ttgasp_or_ppm
                self.behavior = behavior

    def __repr__(self) -> str:
        return f"<TTGasp: {self.ppm}, {self.behavior}, Orphan>"

        # Or if parent is present:
        # f"<TTGasp: {self.ppm}, {self.behavior}, Reference>"

    @property
    def ppm(self) -> int:
        """
        Upper limit of range, in PPEM

        Returns:
            int: The maximum ppm for the gasp record
        """
        return self._ppm

    @ppm.setter
    def ppm(self, value: int) -> None:
        self._ppm = value

    @property
    def behavior(self) -> int:
        """
        Flags describing desired rasterizer behavior.

        Returns:
            int: The flags.

        0x0001 - Use gridfittig
        0x0002 - Use grayscale rendering

        Those additional flags are defined in version 1 of the gasp table specification,
        but they can not be accessed from the FontLab 5 UI:

        0x0004 - Use gridfitting with ClearType symmetric smoothing
        0x0008 - Use smoothing along multiple axes with ClearType®
        """
        # TODO: What happens if we set the unsupported flags via Python?
        return self._behavior

    @behavior.setter
    def behavior(self, value: int) -> None:
        self._behavior = value
