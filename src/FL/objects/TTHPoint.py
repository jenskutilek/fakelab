from __future__ import annotations

from FL.objects.Point import Point


class TTHPoint:
    """
    TTHPoint - class to represent visual TrueType points

    All coordinates in TTHPoint class are set in 10.6 fixed-point format
    TODO: ^ I think this only applies to TTPoint, not TTHPoint
    """

    __slots__ = ["_x", "_y", "_mode", "_state"]

    # Constructor

    def __init__(
        self,
        tthpoint_or_p_or_x: TTHPoint | Point | int | None = None,
        mode_or_y: int | None = None,
    ) -> None:
        self.x = 0
        self.y = 0
        self._mode = 1
        self._state = 0

        if isinstance(tthpoint_or_p_or_x, TTHPoint):
            # copy
            self.x = tthpoint_or_p_or_x.x
            self.y = tthpoint_or_p_or_x.y
            self._mode = tthpoint_or_p_or_x.mode
            self._state = tthpoint_or_p_or_x.state
            if mode_or_y is not None:
                self._mode = mode_or_y
        elif isinstance(tthpoint_or_p_or_x, Point):
            # Set from Point
            self.x = tthpoint_or_p_or_x.x
            self.y = tthpoint_or_p_or_x.y
            if mode_or_y is not None:
                self._mode = mode_or_y
        elif isinstance(tthpoint_or_p_or_x, int) or isinstance(
            tthpoint_or_p_or_x, float
        ):
            self.x = float(tthpoint_or_p_or_x)
            if isinstance(mode_or_y, int) or isinstance(mode_or_y, float):
                self.y = float(mode_or_y)
            else:
                raise TypeError

    def __repr__(self) -> str:
        return "<TTHPoint: x: %g, y: %g, mode: %i>" % (self.x, self.y, self.mode)

    # Attributes

    @property
    def x(self) -> float:
        """
        x coordinate

        Returns:
            float: _description_
        """
        return float(self._x)

    @x.setter
    def x(self, value: float) -> None:
        self._x = int(value)

    @property
    def y(self) -> float:
        """
        y coordinate

        Returns:
            float: _description_
        """
        return float(self._y)

    @y.setter
    def y(self, value: float) -> None:
        self._y = int(value)

    @property
    def mode(self) -> int:
        """
        Point's mode (on-curve or off-curve). Read-only.

        Returns:
            int: _description_
        """
        return self._mode

    @mode.setter
    def mode(self, value: int) -> None:
        raise RuntimeError("class TTHPoint has no attribute mode")

    @property
    def state(self) -> int:
        """
        Point's state (touched or not). Read-only.

        Returns:
            int: _description_
        """
        return self._state

    @state.setter
    def state(self, value: int) -> None:
        raise RuntimeError("class TTHPoint has no attribute state")

    # Operations: none

    # Methods: none


"""
Incorrect # of args to:
 TTHPoint(void)
 TTHPoint([TTH]Point[,int newmode])
 THHPoint(int x,int y[,int newmode])

 Point, TTHPoint or Float is expected in arg 1:
 TTHPoint(Point,int mode)
 TTHPoint(TTHPoint,int mode)
 TTHPoint(int X,int Y)

 Point or TTHPoint is expected in arg 1:
 TTHPoint(Point)
 TTHPoint(TTHPoint)

 TTHPoint

 <TTHPoint: x: %g, y: %g, mode: %d> state mode

 class TTHPoint has no attribute %s
"""
