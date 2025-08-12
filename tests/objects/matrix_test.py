import unittest

import pytest

from FL.objects.Matrix import Matrix
from FL.objects.Point import Point


class MatrixTests(unittest.TestCase):
    def test_instantiation(self):
        m = Matrix()
        assert m.a == 1
        assert m.b == 0
        assert m.c == 0
        assert m.d == 1
        assert m.e == 0
        assert m.f == 0

    # Addition

    def test_add(self):
        m1 = Matrix(2, 4, 8, 16, 32, 64)
        m2 = Matrix(3, 5, 7, 9, 11, 13)
        mr = m1 + m2
        assert mr.a == 5
        assert mr.b == 9
        assert mr.c == 15
        assert mr.d == 25
        assert mr.e == 43
        assert mr.f == 77

    def test_iadd(self):
        m = Matrix(2, 4, 8, 16, 32, 64)
        m2 = Matrix(3, 5, 7, 9, 11, 13)
        m += m2
        assert m.a == 5
        assert m.b == 9
        assert m.c == 15
        assert m.d == 25
        assert m.e == 43
        assert m.f == 77

    def test_Add(self):
        m = Matrix(2, 4, 8, 16, 32, 64)
        m2 = Matrix(3, 5, 7, 9, 11, 13)
        m.Add(m2)
        assert m.a == 5
        assert m.b == 9
        assert m.c == 15
        assert m.d == 25
        assert m.e == 43
        assert m.f == 77

    # Subtraction

    def test_sub(self):
        m1 = Matrix(2, 4, 8, 16, 32, 64)
        m2 = Matrix(3, 5, 7, 9, 11, 13)
        mr = m1 - m2
        assert mr.a == -1
        assert mr.b == -1
        assert mr.c == 1
        assert mr.d == 7
        assert mr.e == 21
        assert mr.f == 51

    def test_isub(self):
        m = Matrix(2, 4, 8, 16, 32, 64)
        m2 = Matrix(3, 5, 7, 9, 11, 13)
        m -= m2
        assert m.a == -1
        assert m.b == -1
        assert m.c == 1
        assert m.d == 7
        assert m.e == 21
        assert m.f == 51

    def test_Sub(self):
        m = Matrix(2, 4, 8, 16, 32, 64)
        m2 = Matrix(3, 5, 7, 9, 11, 13)
        m.Sub(m2)
        assert m.a == -1
        assert m.b == -1
        assert m.c == 1
        assert m.d == 7
        assert m.e == 21
        assert m.f == 51

    # Multiplication

    def test_mul_float(self):
        m1 = Matrix(2, 2, 2, 2, 2, 2)
        m1 = m1 * 3
        assert m1.a == 6
        assert m1.b == 6
        assert m1.c == 6
        assert m1.d == 6
        assert m1.e == 6
        assert m1.f == 6

    def test_mul_matrix(self):
        m1 = Matrix(2, 2, 2, 2, 2, 2)
        m2 = Matrix(3, 3, 3, 3, 3, 3)
        m1 = m1 * m2
        assert m1.a == 12
        assert m1.b == 12
        assert m1.c == 12
        assert m1.d == 12
        assert m1.e == 15
        assert m1.f == 15

    def test_imul_float(self):
        m1 = Matrix(2, 2, 2, 2, 2, 2)
        m1 *= 3
        assert m1.a == 6
        assert m1.b == 6
        assert m1.c == 6
        assert m1.d == 6
        assert m1.e == 6
        assert m1.f == 6

    def test_imul_matrix(self):
        m1 = Matrix(2, 2, 2, 2, 2, 2)
        m2 = Matrix(3, 3, 3, 3, 3, 3)
        m1 *= m2
        assert m1.a == 12
        assert m1.b == 12
        assert m1.c == 12
        assert m1.d == 12
        assert m1.e == 15
        assert m1.f == 15

    def test_Mul_float(self):
        m1 = Matrix(2, 2, 2, 2, 2, 2)
        m1.Mul(3)
        assert m1.a == 6
        assert m1.b == 6
        assert m1.c == 6
        assert m1.d == 6
        assert m1.e == 6
        assert m1.f == 6

    # Transform

    def test_Transform(self):
        m1 = Matrix(2, 2, 2, 2, 2, 2)
        m2 = Matrix(3, 3, 3, 3, 3, 3)
        m1 = m1 * m2
        assert m1.a == 12
        assert m1.b == 12
        assert m1.c == 12
        assert m1.d == 12
        assert m1.e == 15
        assert m1.f == 15

    def test_Transform_2(self):
        m1 = Matrix(2, 4, 8, 16, 32, 64)
        m2 = Matrix(3, 5, 7, 9, 11, 13)
        m1 = m1 * m2
        assert m1.a == 46
        assert m1.b == 92
        assert m1.c == 86
        assert m1.d == 172
        assert m1.e == 427
        assert m1.f == 813

    # FakeLab addition

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
