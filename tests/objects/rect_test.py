import unittest


from FL.objects.Point import Point
from FL.objects.Rect import Rect


class RectTests(unittest.TestCase):
    def test_instantiation(self):
        # No args
        r = Rect()
        assert r.x == 0
        assert r.y == 0
        assert r.width == 0
        assert r.height == 0
        assert r.ll == Point(0, 0)
        assert r.ur == Point(0, 0)

    def test_instantiation_point(self):
        # Documentation for Rect from Point is wrong: It says the rect will be from
        # (0, 0) to the point, but it is at the point with width = 0 and height = 0.
        r = Rect(Point(100, 100))
        assert r.x == 100
        assert r.y == 100
        assert r.width == 0
        assert r.height == 0

    def test_instantiation_coords(self):
        # Floats are preserved
        r = Rect(0.0, 0.0, 10.5, 10.5)
        assert r.x == 0
        assert r.y == 0
        assert r.width == 10.5
        assert r.height == 10.5

    def test_instantiation_normalization(self):
        # Points are not normalized
        r = Rect(10.5, 10.5, 0.0, 0.0)
        assert r.x == 10.5
        assert r.y == 10.5
        assert r.width == -10.5
        assert r.height == -10.5

    def test_various(self):
        # Directly from FL5, wtf is happening here?
        # FIXME
        r = Rect(1, 2, 3, 4)
        r.x = 5
        assert r.x == 5
        assert r.width == -2
        r.width = 100
        assert r.x == 105
        assert r.ll == Point(105, 2)
        assert r.width == -102

    # Addition

    def test_add(self):
        r = Rect(0.0, 0.0, 10.5, 10.5)
        r2 = r + Point(-1, -1)
        assert r.ll == Point(-1, -1)
        assert r.ur == Point(10.5, 10.5)
        assert r2.width == 11.5
        assert r2.height == 11.5

        # No normalization again:
        r = Rect(10.5, 10.5, 0.0, 0.0)
        r2 = r + Point(-1, -1)
        assert r.ll == Point(-1, -1)
        assert r.ur == Point(0, 0)

    def test_iadd_point(self):
        r = Rect(0.0, 0.0, 10.5, 10.5)
        r += Point(-1, -1)
        assert r.x == -1
        assert r.y == -1
        assert r.width == 11.5
        assert r.height == 11.5

        r = Rect(Point(0, -200))
        assert r.x == 0
        assert r.y == -200
        assert r.width == 0
        assert r.height == 0
        r += Point(500, -200)
        assert r.x == 0
        assert r.y == -200
        assert r.width == 500
        assert r.height == 0
        r += Point(490, -102)
        assert r.ll == Point(0, -200)
        assert r.ur == Point(500, -102)
        r += Point(-10, -102)
        assert r.ll == Point(-10, -200)
        assert r.ur == Point(500, -102)
        assert r.width == 510
        assert r.height == 98

    def test_Validate(self):
        r = Rect(105, 2, 3, 4)
        r.Validate()
        assert r.ll == Point(3, 2)
        assert r.ur == Point(105, 4)
        assert r.width == 102
        assert r.height == 2
