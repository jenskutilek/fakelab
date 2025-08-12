import unittest

import pytest

from FL.objects.Matrix import Matrix
from FL.objects.Point import Point


class PointTests(unittest.TestCase):
    def test_instantiation(self):
        p = Point()
        assert p.x == 0.0
        assert p.y == 0.0

    def test_instantiation_coords(self):
        p = Point(-200, 0)
        assert p.x == -200.0
        assert p.y == 0.0

    def test_instantiation_coords_invalid(self):
        with pytest.raises(RuntimeError):
            Point(-200)

    def test_instantiation_copy(self):
        p = Point(-200, 0)
        p2 = Point(p)
        assert p.x == -200.0
        assert p.y == 0.0
        assert p2 == p
        p.x += 1
        assert p.x == -199.0
        # Make sure the points are independent objects
        assert p != p2

    def test_instantiation_copy_invalid(self):
        p = Point()
        with pytest.raises(RuntimeError):
            Point(p, 5)

    def test_addition(self):
        p = Point(-199, 0)
        p2 = Point(-200, 0)
        p2.Add(p)
        assert p2.x == -399.0
        assert p2.y == 0.0

    # Multiplication

    def test_mul_Point(self):
        p = Point(44, 55)
        p2 = Point(2, 3)
        assert p * p2 == 253.0

    def test_mul_Matrix(self):
        m1 = Matrix(2, 4, 8, 16, 32, 64)
        p = Point(44, 55)
        p *= m1
        assert (p.x, p.y) == (340, 1296)

    def test_mul_float(self):
        p = Point(44, 55)
        p *= 2
        assert (p.x, p.y) == (88, 110)

    # Transform

    def test_Transform_Point(self):
        m1 = Matrix(2, 4, 8, 16, 32, 64)
        p = Point(44, 55)
        p.Transform(m1)
        assert (p.x, p.y) == (340, 1296)

    def test_Transform_Point_float(self):
        m1 = Matrix(2, 4, 8, 16, 32, 64)
        p = Point(44.2, 55.5)
        p.Transform(m1)
        assert (p.x, p.y) == (342.4, 1305.6)
