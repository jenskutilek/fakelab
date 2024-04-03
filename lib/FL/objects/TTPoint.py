from __future__ import annotations


class TTPoint(object):
    """
    ===============================================
    TTPoint - class to represent TrueType points
    ===============================================
    All coordinates in TTPoint class are set in 10.6 fixed-point format

    >>> tp = TTPoint()
    """
    def __init__(self):
        self.x = 32767
        self.y = 32767
        self.flag = 255
        # Can I has a parent?
        # self._parent = None

    def __repr__(self):
        return '<TTPoint flags="%i" x="%g" y="%g", Orphan>' % (self.flag, self.x, self.y)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
