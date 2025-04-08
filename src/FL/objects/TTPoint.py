from __future__ import annotations


class TTPoint:
    """
    ===============================================
    TTPoint - class to represent TrueType points
    ===============================================

    All coordinates in TTPoint class are set in 10.6 fixed-point format
    """

    __slots__ = ["_x", "_y", "_flag"]

    # Constructor

    def __init__(self) -> None:
        """
        TTPoint() - generic constructor, creates a TTPoint with zero coordinates
        """
        self.x = 32767
        self.y = 32767
        self.flag = 255

    def __repr__(self) -> str:
        return f"<TTPoint: flags: {self.flag}, x: {self.x} y: {self.y}, Orphan>"

    # Attributes

    @property
    def x(self) -> int:
        """
        x coordinate

        Returns:
            int: _description_
        """
        return self._x

    @x.setter
    def x(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError
        self._x = value

    @property
    def y(self) -> int:
        """
        y coordinate

        Returns:
            int: _description_
        """
        return self._y

    @y.setter
    def y(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError
        self._y = value

    @property
    def flag(self) -> int:
        """
        point's flag (on-curve or off-curve)

        Returns:
            int: _description_
        """
        return self._flag

    @flag.setter
    def flag(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError
        self._flag = value

    # Operations: none

    # Methods: none
