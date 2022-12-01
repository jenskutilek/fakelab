from __future__ import annotations

from .Point import Point


class Rect(object):
    """
    Rect() - generic constructor, creates a Rect with zero coordinates
    Rect(Rect r) - copy constructor
    Rect(Point p) - creates rectangle with one corner at (0, 0) and
                           another - at coordinates defined by p
    Rect(Point p0, Point p1) - creates rectangle defined by the corner points
    Rect(x0, y0, x1, y1) - creates a rectangle defined by the coordinates of
       the corner points
    """

    def __init__(
        self, rect_or_point_or_x0=None, point_or_y0=None, x1=None, y1=None
    ):
        """
        # No args
        >>> r = Rect()
        >>> print(r)
        <Rect: 0,0,0,0>
        >>> print(r.x)
        0.0
        >>> print(r.y)
        0.0

        # Documentation for Rect from Point is wrong
        >>> r = Rect(Point(100, 100))
        >>> print(r)
        <Rect: 100,100,100,100>

        # Floats are preserved
        >>> r = Rect(0.0, 0.0, 10.5, 10.5)
        >>> print(r)
        <Rect: 0,0,10.5,10.5>

        # Points are not normalized
        >>> r = Rect(10.5, 10.5, 0.0, 0.0)
        >>> print(r)
        <Rect: 10.5,10.5,0,0>
        >>> print(r.width, r.height)
        """
        self._x0 = 0.0
        self._y0 = 0.0
        self._x1 = 0.0
        self._y1 = 0.0

        if isinstance(rect_or_point_or_x0, Rect):
            # Copy constructor
            self._x0 = rect_or_point_or_x0._x0
            self._y0 = rect_or_point_or_x0._y0
            self._x1 = rect_or_point_or_x0._x1
            self._y1 = rect_or_point_or_x0._y1
        elif isinstance(rect_or_point_or_x0, Point):
            if isinstance(point_or_y0, Point):
                self._x0 = rect_or_point_or_x0.x
                self._y0 = rect_or_point_or_x0.y
                self._x1 = point_or_y0.x
                self._y1 = point_or_y0.y
            else:
                # The doc is not correct, x/y don't stay at 0,
                # but the point is used for all coords
                self._x0 = rect_or_point_or_x0.x
                self._y0 = rect_or_point_or_x0.y
                self._x1 = rect_or_point_or_x0.x
                self._y1 = rect_or_point_or_x0.y
        elif isinstance(rect_or_point_or_x0, int) or isinstance(
            rect_or_point_or_x0, float
        ):
            assert point_or_y0 is not None
            assert x1 is not None
            assert y1 is not None
            self._x0 = float(rect_or_point_or_x0)
            self._y0 = float(point_or_y0)
            self._x1 = float(x1)
            self._y1 = float(y1)
        # else: zero rect

    def __repr__(self):
        return "<Rect: %g,%g,%g,%g>" % (self._x0, self._y0, self._x1, self._y1)

    # Attributes

    @property
    def ll(self):
        """
        position of the left/bottom corner
        """
        return Point(self._x0, self._y0)

    @property
    def ur(self):
        """
        position of the right/top corner
        """
        return Point(self._x1, self._y1)

    @property
    def x(self):
        return self._x0

    @property
    def y(self):
        return self._y0

    @property
    def width(self):
        return self._x1 - self._x0

    @property
    def height(self):
        return self._y1 - self._y0

    # Operations

    def __add__(self, other):
        """
        Point or Rect must be second operand, rectangle is expanded to include
        this point or rectangle

        # In-place addition
        >>> r = Rect(0.0, 0.0, 10.5, 10.5)
        >>> print(r)
        <Rect: 0,0,10.5,10.5>
        >>> r += Point(-1, -1)
        >>> print(r)
        <Rect: -1,-1,10.5,10.5>

        >>> r = Rect(Point(0, -200))
        >>> print(r)
        <Rect: 0,-200,0,-200>
        >>> r += Point(500, -200)
        >>> print(r)
        <Rect: 0,-200,500,-200>
        >>> r += Point(490, -102)
        >>> print(r)
        <Rect: 0,-200,500,-102>
        >>> r += Point(-10, -102)
        >>> print(r)
        <Rect: -10,-200,500,-102>
        >>> print(r.width)
        510.0
        >>> print(r.height)
        98.0

        # External addition
        >>> print(Rect(0.0, 0.0, 10.5, 10.5) + Point(-1, -1))
        <Rect: -1,-1,10.5,10.5>

        # This again doesn't check that the corner points are normalized.
        >>> r = Rect(10.5, 10.5, 0.0, 0.0)
        >>> print(r)
        <Rect: 10.5,10.5,0,0>
        >>> r += Point(-1, -1)
        >>> print(r)
        <Rect: -1,-1,0,0>
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

    def __mul__(self, other):
        """
        Second operand must be Matrix. Matrix transformation is applied to the
        rectangle.
        """
        raise NotImplementedError


if __name__ == "__main__":
    import doctest

    doctest.testmod()
