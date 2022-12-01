from __future__ import annotations


class Point(object):
    """
    ===============================================
    Point - base class to represent point
    ===============================================
    Integer or float values are accepted as coordinates

    >>> p = Point()
    """

    def __init__(self, pt_or_x=None, y=None):
        """
        # No args
        >>> p = Point()
        >>> print(p.x, p.y)
        0.0 0.0

        # Initialize with coords
        >>> p = Point(-200, 0)
        >>> print(p.x, p.y)
        -200.0 0.0

        # Copy constructor
        >>> p2 = Point(p)
        >>> print(p2.x, p2.y)
        -200.0 0.0
        >>> p == p2
        True
        >>> p.x += 1
        >>> print(p.x, p.y)
        -199.0 0.0
        >>> p == p2
        False

        # Addition
        >>> p2.Add(p)
        >>> print(p2.x, p2.y)
        -399.0 0.0
        """
        self._parent = None
        self.x = 0.0
        self.y = 0.0

        if isinstance(pt_or_x, Point):
            # copy
            self._parent = pt_or_x.parent
            self.x = pt_or_x.x
            self.y = pt_or_x.y
        else:
            # coordinates
            self._parent = None
            if pt_or_x is not None:
                self.x = float(pt_or_x)
            if y is not None:
                self.y = float(y)

    def __repr__(self):
        return '<Point x="%g" y="%g">' % (self.x, self.y)

    # Additions for FakeLab

    def fake_update(self, parent=None):
        """
        Is called from FontLab.UpdateFont()
        """
        self._parent = parent

    # Attributes

    @property
    def parent(self):
        """
        Point's parent object
        """
        return self._parent

    # Operations

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    # coerce?
    def __coerce__(self, other):
        """
        can be operated on Point, float value, Matrix and Rect
        """
        raise NotImplementedError

    def __add__(self, other):
        """
        Point must be second operand, both coordinates are added
        """
        assert isinstance(other, Point)

        self.x += other.x
        self.y += other.y

    def __sub__(self, other):
        """
        Point must be second operand, both coordinates are added
        """
        raise NotImplementedError

    def __mul__(self, other):
        """
        second operand may be Point, float or Matrix. If second operand is Point,
        then result of scalar product is returned
        """
        raise NotImplementedError

    # Methods

    def Assign(self, pt_or_x, y=None):
        """
        assigns new values to a Point
        """
        if y is None:
            self.x = pt_or_x.x
            self.y = pt_or_x.y
        else:
            # coordinates
            self._parent = None
            self.x = pt_or_x
            self.y = y

    def Shift(self, pt_or_x, y=None):
        """
        shifts Point on a position defined by p or x and y values
        """
        if isinstance(pt_or_x, Point):
            self += pt_or_x
        else:
            if isinstance(pt_or_x, int) and isinstance(y, int):
                self.x += pt_or_x
                self.y += y
            else:
                raise TypeError

    def Add(self, point):
        """
        same as Shift(Point p)
        """
        self.Shift(point)

    def Sub(self, point):
        """
        subtracts p coordinates from the current Point
        """
        raise NotImplementedError

    def Mul(self, s):
        """
        mutiplies Point's position to s value
        """
        raise NotImplementedError

    def Transform(self, m):
        """
        applies Matrix transformation to the Point
        """
        raise NotImplementedError


if __name__ == "__main__":
    import doctest

    doctest.testmod()
