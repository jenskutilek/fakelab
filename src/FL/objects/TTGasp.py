from __future__ import annotations


class TTGasp:
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
                # copy constructor
                self.ppm = ttgasp_or_ppm.ppm
                self.behavior = ttgasp_or_ppm.behavior
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
        return self._ppm

    @ppm.setter
    def ppm(self, value: int) -> None:
        self._ppm = value

    @property
    def behavior(self) -> int:
        return self._behavior

    @behavior.setter
    def behavior(self, value: int) -> None:
        self._behavior = value
