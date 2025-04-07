from __future__ import annotations

from typing import TYPE_CHECKING

from FL.objects.Matrix import Matrix

if TYPE_CHECKING:
    from typing import Any


class Point:
    __slots__ = ["_parent", "_x", "_y"]

    # Constructor

    def __init__(
        self, p_or_x: Point | float | None = None, y: float | None = None
    ) -> None:
        """
        Point - base class to represent point

        Args:
            p_or_x (Point | float | None, optional): The `Point` to copy coordinates
                from, or the x coordinate. Defaults to None.
            y (float | None, optional): The y coordinate. Defaults to None.
        """
        self._parent = None
        self.x = 0
        self.y = 0
        if p_or_x is not None:
            self.Assign(p_or_x, y)

    def __repr__(self) -> str:
        return '<Point x="%g" y="%g">' % (self.x, self.y)

    # Additions for FakeLab

    def fake_update(self, parent: Any | None = None) -> None:
        """
        Is called from FontLab.UpdateFont()
        """
        self._parent = parent

    # Attributes

    @property
    def parent(self) -> Any:
        """
        Point's parent object
        """
        # TODO: What can be a point's parent?
        return self._parent

    @property
    def x(self) -> float:
        """
        Horizontal position of the point

        Returns:
            float: The x coordinate
        """
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        self._x = float(value)

    @property
    def y(self) -> float:
        """
        Vertical position of the point

        Returns:
            float: The y coordinate
        """
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        self._y = float(value)

    # Operations

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    # coerce?
    def __coerce__(self, other):
        """
        can be operated on Point, float value, Matrix and Rect
        """
        raise NotImplementedError

    def __add__(self, other: Point) -> Point:
        """
        Point must be second operand, both coordinates are added
        """
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point) -> Point:
        """
        Point must be second operand, both coordinates are subtracted
        """
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other: Point | float | Matrix) -> Point | float:
        """
        Second operand may be `Point`, `float` or `Matrix`. If second operand is
        `Point`, then result of scalar product is returned
        """
        if isinstance(other, Point):
            # Scalar product
            return self.x * other.x + self.y * other.y

        elif isinstance(other, Matrix):
            # Transform the point with the matrix
            p = Point(self)
            p.Transform(other)
            return p

        return Point(self.x * other, self.y * other)

    # Methods

    def Assign(self, p_or_x: Point | float, y: float | None = None) -> None:
        """
        Assigns new values to a Point
        """
        if isinstance(p_or_x, Point):
            # copy
            if y is not None:
                raise RuntimeError

            self._parent = p_or_x.parent
            self.x = p_or_x.x
            self.y = p_or_x.y
        else:
            # coordinates
            self._parent = None
            if p_or_x is not None:
                self.x = p_or_x
            if y is None:
                raise RuntimeError

            else:
                self.y = float(y)

    def Shift(self, p_or_x: Point | float, y: float | None = None) -> None:
        """
        Shifts Point on a position defined by p or x and y values
        """
        if isinstance(p_or_x, Point):
            p = p_or_x
        else:
            p = Point(p_or_x, y)
        self.x += p.x
        self.y += p.y

    def Add(self, p: Point) -> None:
        """
        Same as Shift(Point p)
        """
        self.Shift(p)

    def Sub(self, p: Point) -> None:
        """
        Subtracts p coordinates from the current Point
        """
        self.x -= p.x
        self.y -= p.y

    def Mul(self, s: float) -> None:
        """
        Multiplies Point's position to s value
        """
        self.x *= s
        self.y *= s

    def Transform(self, m: Matrix) -> None:
        """
        Applies Matrix transformation to the Point
        """
        m.fake_transform_point(self)
