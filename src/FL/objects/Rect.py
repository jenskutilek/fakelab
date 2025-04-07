from __future__ import annotations

from typing import TYPE_CHECKING

from FL.objects.Point import Point

if TYPE_CHECKING:
    from FL.objects.Matrix import Matrix


class Rect:
    """
    Rect()                   - generic constructor, creates a Rect with zero coordinates
    Rect(Rect r)             - copy constructor
    Rect(Point p)            - creates rectangle with one corner at (0, 0) and another
                               at coordinates defined by p
    Rect(Point p0, Point p1) - creates rectangle defined by the corner points
    Rect(x0, y0, x1, y1)     - creates a rectangle defined by the coordinates of the
                               corner points
    """

    __slots__ = ["_x0", "_y0", "_x1", "_y1"]

    # Constructor

    def __init__(
        self,
        r_or_p0_or_x0: Rect | Point | float | None = None,
        p1_or_x0: Point | float | None = None,
        x1: float | None = None,
        y1: float | None = None,
    ) -> None:
        self._x0 = 0.0
        self._y0 = 0.0
        self._x1 = 0.0
        self._y1 = 0.0

        if r_or_p0_or_x0 is not None:
            self.Assign(r_or_p0_or_x0, p1_or_x0, x1, y1)

    def __repr__(self) -> str:
        return "<Rect: %g,%g,%g,%g>" % (self._x0, self._y0, self._x1, self._y1)

    # Attributes

    @property
    def ll(self) -> Point:
        """
        position of the left/bottom corner
        """
        return Point(self._x0, self._y0)

    @property
    def ur(self) -> Point:
        """
        position of the right/top corner
        """
        return Point(self._x1, self._y1)

    @property
    def x(self) -> float:
        return self._x0

    @x.setter
    def x(self, value: float) -> None:
        self._x0 = float(value)

    @property
    def y(self) -> float:
        return self._y0

    @y.setter
    def y(self, value: float) -> None:
        self._y0 = float(value)

    @property
    def width(self) -> float:
        return self._x1 - self._x0

    @width.setter
    def width(self, value: float) -> None:
        self._x1 = self._x0 + value

    @property
    def height(self) -> float:
        return self._y1 - self._y0

    @height.setter
    def height(self, value: float) -> None:
        self._y1 = self._y0 + value

    # Operations

    def __add__(self, other: Point | Rect) -> Rect:
        """
        Point or Rect must be second operand, rectangle is expanded to include this
        point or rectangle

        Args:
            other (Point | Rect): The point or rectangle to add.

        Returns:
            Rect: The enclosing rectangle.
        """
        if isinstance(other, Point):
            # This again doesn't check that the corner points are normalized.
            if other.x < self._x0:
                self._x0 = other.x
            if other.y < self._y0:
                self._y0 = other.y
            if other.x > self._x1:
                self._x1 = other.x
            if other.y > self._y1:
                self._y1 = other.y
        elif isinstance(other, Rect):
            raise NotImplementedError
        else:
            raise TypeError
        return self

    def __mul__(self, other: Matrix) -> Rect:
        """
        Second operand must be `Matrix`. Matrix transformation is applied to the
        rectangle.
        """
        raise NotImplementedError

    # Methods

    def Assign(
        self,
        r_or_p0_or_x0: Rect | Point | float | None = None,
        p1_or_x0: Point | float | None = None,
        x1: float | None = None,
        y1: float | None = None,
    ) -> None:
        """
        Assigns new values to a Rect, the same as constructor

        Args:
            r_or_p0_or_x0 (Rect | Point | float | None, optional): _description_. Defaults to None.
            p1_or_x0 (Point | float | None, optional): _description_. Defaults to None.
            x1 (float | None, optional): _description_. Defaults to None.
            y1 (float | None, optional): _description_. Defaults to None.
        """
        if isinstance(r_or_p0_or_x0, Rect):
            # Copy constructor
            self._x0 = r_or_p0_or_x0._x0
            self._y0 = r_or_p0_or_x0._y0
            self._x1 = r_or_p0_or_x0._x1
            self._y1 = r_or_p0_or_x0._y1
        elif isinstance(r_or_p0_or_x0, Point):
            if isinstance(p1_or_x0, Point):
                self._x0 = r_or_p0_or_x0.x
                self._y0 = r_or_p0_or_x0.y
                self._x1 = p1_or_x0.x
                self._y1 = p1_or_x0.y
            else:
                # The doc is not correct, x/y don't stay at 0,
                # but the point is used for all coords
                self._x0 = r_or_p0_or_x0.x
                self._y0 = r_or_p0_or_x0.y
                self._x1 = r_or_p0_or_x0.x
                self._y1 = r_or_p0_or_x0.y
        elif isinstance(r_or_p0_or_x0, int) or isinstance(r_or_p0_or_x0, float):
            assert isinstance(p1_or_x0, int) or isinstance(p1_or_x0, float)
            assert x1 is not None
            assert y1 is not None
            self._x0 = float(r_or_p0_or_x0)
            self._y0 = float(p1_or_x0)
            self._x1 = float(x1)
            self._y1 = float(y1)

    def Shift(self, p_or_x: Point | float, y: float | None = None) -> None:
        # (Point p) | (x, y) - shifts Rect on a position defined by p or x
        # and y values
        raise NotImplementedError

    def Transform(self, m: Matrix) -> None:
        # (Matrix m) - applies Matrix transformation to the Rect (see Matrix().__doc__)
        raise NotImplementedError

    def Resize(self) -> None:
        # (width, height) - resizes rectangle to new width and height
        raise NotImplementedError

    def Include(
        self, r_or_p_or_x: Rect | Point | float, y: float | None = None
    ) -> None:
        # Expands rectangle to include new rectangle or point
        if isinstance(r_or_p_or_x, Point):
            # This again doesn't check that the corner points are normalized.
            if r_or_p_or_x.x < self._x0:
                self._x0 = r_or_p_or_x.x
            if r_or_p_or_x.y < self._y0:
                self._y0 = r_or_p_or_x.y
            if r_or_p_or_x.x > self._x1:
                self._x1 = r_or_p_or_x.x
            if r_or_p_or_x.y > self._y1:
                self._y1 = r_or_p_or_x.y
        elif isinstance(r_or_p_or_x, Rect):
            raise NotImplementedError
        else:
            # floats
            if not isinstance(y, float):
                raise RuntimeError

            raise NotImplementedError

    def Check(self, r_or_p: Rect | Point) -> bool:
        # (Rect r) - returns True if r overlaps current rectangle
        # (Point p) - returns True if p is inside current rectangle
        raise NotImplementedError

    def Validate(self) -> None:
        """
        Corrects rectangle's orientation
        """
        self._x0, self._x1 = sorted([self._x0, self._x1])
        self._y0, self._y1 = sorted([self._y0, self._y1])
