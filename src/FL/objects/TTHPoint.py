from __future__ import annotations

from FL.objects.Point import Point


class TTHPoint:
    """
    ===============================================
    TTHPoint - class to represent visual TrueType points
    ===============================================
    All coordinates in TTHPoint class are set in 10.6 fixed-point format
    ??? ^ I think this only applies to TTPoint, not TTHPoint

        >>> tp = TTHPoint()
    """

    def __init__(self, pt_or_x=None, mode_or_y=None):
    # Constructor

        self.x = 0.0
        self.y = 0.0
        self.mode = 1
        self.state = 1

        if isinstance(pt_or_x, TTHPoint):
            # copy
            self.x = pt_or_x.x
            self.y = pt_or_x.y
            self.mode = pt_or_x.mode
            self.state = pt_or_x.state
            if mode_or_y is not None:
                self.mode = mode_or_y
        elif isinstance(pt_or_x, Point):
            # Set from Point
            self.x = pt_or_x.x
            self.y = pt_or_x.y
            if mode_or_y is not None:
                self.mode = mode_or_y
        elif isinstance(pt_or_x, int) or isinstance(pt_or_x, float):
            self.x = float(pt_or_x)
            if isinstance(mode_or_y, int) or isinstance(mode_or_y, float):
                self.y = float(mode_or_y)
            else:
                raise TypeError

    def __repr__(self):
        return '<TTHPoint x="%g" y="%g", mode="%i">' % (self.x, self.y, self.mode)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
