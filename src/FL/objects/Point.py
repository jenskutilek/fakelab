from __future__ import annotations

from typing import TYPE_CHECKING, Any

from FL.fake.Base import Copyable
from FL.objects.Matrix import Matrix

if TYPE_CHECKING:
    from FL.objects.Rect import Rect

__doc__ = "Class to represent a point"


class Point(Copyable):
    __slots__ = ["_parent", "_x", "_y"]

    # Constructor

    def __init__(
        self, p_or_x: Point | float | None = None, y: float | None = None
    ) -> None:
        """
        Point - base class to represent point

        Point()
            generic constructor, creates a Point with zero coordinates
        Point(Point)
            copy constructor
        Point(x, y)
            creates a Point and assigns coordinates. x and y may be integer or float

        Args:
            p_or_x (Point | float | None, optional): The `Point` to copy coordinates
                from, or the x coordinate. Defaults to None.
            y (float | None, optional): The y coordinate. Defaults to None.
        """
        # From the binary:
        """
        Possible errors:

        Incorrect # of args to:
        Point()
        Point(number x, number y)
        Point(Point p)

        Number is expected in arg 2:
        Point(number x, number y)

        Number is expected in arg 1:
        Point(number x, number y)

        Point type is expected in arg 1:
        Point(Point p)

        class Point has no attribute %s or it is read-only
        """
        self._parent = None
        self.x = 0
        self.y = 0
        if p_or_x is not None:
            self.Assign(p_or_x, y)

    def __repr__(self) -> str:
        parent = "orphan" if self._parent is None else "active refernce"
        return f"<Point: x={self.x:g}, y={self.y:g}, {parent}>"

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
        """
        compares two points, both coordinates must be equal
        """
        # Point expected to compare
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    def __coerce__(self, other: Point | float | Matrix | Rect) -> Point:
        """
        can be operated on Point, float value, Matrix and Rect
        """
        raise NotImplementedError

    def __add__(self, other: Point) -> Point:
        """
        Point must be second operand, both coordinates are added
        """
        if not isinstance(other, Point):
            raise RuntimeError("Point is expected as right operand of Point.operator+")
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point) -> Point:
        """
        Point must be second operand, both coordinates are subtracted
        """
        if not isinstance(other, Point):
            raise RuntimeError("Point is expected as right operand of Point.operator-")
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other: Point | float | Matrix) -> Point | float:
        """
        Second operand may be `Point`, `float` or `Matrix`. If second operand is
        `Point`, then result of scalar product is returned
        """
        # Point is expected as left operand of Point.operator*
        if isinstance(other, Point):
            # Scalar product
            return self.x * other.x + self.y * other.y

        elif isinstance(other, Matrix):
            # Transform the point with the matrix
            p = Point(self)
            p.Transform(other)
            return p

        elif isinstance(other, (float, int)):
            return Point(self.x * other, self.y * other)

        raise RuntimeError(
            "Point, Matrix or Number is expected as right operand of Point.operator*"
        )

    # Methods

    def Assign(self, p_or_x: Point | float, y: float | None = None) -> None:
        """
        Assigns new values to a Point
        """

        """
        Possible errors:

        Incorrect # of args to:
        Point.Assign(number x, number y)
        Point.Assign(Point p)

        Point is expected in arg 1:
        Point.Assign(Point p)
        """
        if isinstance(p_or_x, Point):
            # copy
            if y is not None:
                raise RuntimeError

            self._copy_constructor(p_or_x)
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

        """
        Possible errors:

        Incorrect # of args to:
        Point.Shift(number x, number y)
        Point.Shift(Point p)

        Point is expected in arg 1:
        Point.Shift(Point p)
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

        """
        Possible errors:

        Incorrect # of args to:
        Point.Add(Point p)

        Point is expected in arg 1:
        Point.Add(Point p)
        """
        self.Shift(p)

    def Sub(self, p: Point) -> None:
        """
        Subtracts p coordinates from the current Point
        """

        """
        Possible errors:

        Incorrect # of args to:
        Point.Sub(Point p).

        Point is expected in arg 1:
        Point.Sub(Point p)
        """
        self.x -= p.x
        self.y -= p.y

    def Mul(self, s: float) -> None:
        """
        Multiplies Point's position to s value
        """

        """
        Possible errors:

        Incorrect # of args to:
        Point.Mul(number n).

        Number is expected in arg 1:
        Point.Mul(number n)
        """
        self.x *= s
        self.y *= s

    def Transform(self, m: Matrix) -> None:
        """
        Applies Matrix transformation to the Point
        """

        """
        Possible errors:

        Incorrect # of args to:
        Point.Transform(Matrix m).

        Matrix is expected in arg 1:
        Point.Transform(Matrix m)
        """
        m.fake_transform_point(self)
