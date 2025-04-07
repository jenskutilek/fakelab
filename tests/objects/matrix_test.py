import unittest

import pytest

from FL.objects.Matrix import Matrix


class MatrixTests(unittest.TestCase):
    def test_instantiation(self):
        m = Matrix()
        assert m.a == 1.0
        assert m.b == 0.0
        assert m.c == 0.0
        assert m.d == 1.0
        assert m.e == 0.0
        assert m.f == 0.0

    def test_Mul_float(self):
        m1 = Matrix(2, 2, 2, 2, 2, 2)
        m1.Mul(3)
        assert m1.a == 6
        assert m1.b == 6
        assert m1.c == 6
        assert m1.d == 6
        assert m1.e == 6
        assert m1.f == 6

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
        m2 = Matrix(3, 3, 3, 3, 3, 3)
        m1 = m1 * m2
        assert m1.a == 30
        assert m1.b == 60
        assert m1.c == 30
        assert m1.d == 60
        assert m1.e == 291
        assert m1.f == 291
