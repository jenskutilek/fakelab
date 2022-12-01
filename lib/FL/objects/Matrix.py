from __future__ import annotations

from typing import List


class Matrix(object):
    """
    ===============================================
    Matrix - class to represent planar transformations
    ===============================================
    Matrix is used to perform following transformations:
    x1 = x * a + y * b + e
    y1 = x * c + y * d + f
    """

    def __init__(
        self,
        a: "Matrix" | List[float] | float | None,
        b: float | None = None,
        c: float | None = None,
        d: float | None = None,
        e: float | None = None,
        f: float | None = None,
    ) -> None:
        """
        Matrix() - generic constructor, creates a Matrix that makes no change to coordinates
        Matrix(Matrix) - copy constructor
        Matrix([a, b, c, d, e, f]) - creates a Matrix and assigns coordinates from the list of float numbers
        Matrix(a, b, c, d, e, f) - creates a Matrix and assigns coordinates from float numbers
        """
        if a is None:
            self.a = 1
            self.b = 0
            self.c = 0
            self.d = 1
            self.e = 0
            self.f = 0
        elif isinstance(a, "Matrix"):
            self.a = a.a
            self.b = a.b
            self.c = a.c
            self.d = a.d
            self.e = a.e
            self.f = a.f
        else:
            assert isinstance(a, float)
            self.a = a
            self.b = b
            self.c = c
            self.d = d
            self.e = e
            self.f = f

    # Operations

    def __add__(self, other: "Matrix"):
        """
        Matrix must be second operand, all parameters are added
        """
        raise NotImplementedError

    def __sub__(self, other: "Matrix"):
        """
        Matrix must be second operand, all parameters are subtracted
        """
        raise NotImplementedError

    def __mul__(self, other: "Matrix" | float):
        """
        multiply (with Matrix) - matrixes are multiplied
        multiply (with float number) - all parameters are scaled by the operand
        """
        raise NotImplementedError

    # Methods

    def Assign(
        self,
        a: "Matrix" | List[float] | float | None,
        b: float | None = None,
        c: float | None = None,
        d: float | None = None,
        e: float | None = None,
        f: float | None = None,
    ):
        """
        assigns new values to a Matrix, uses the same syntax as in constructors
        """
        raise NotImplementedError

    def Add(self, m: "Matrix") -> None:
        """
        adds values of the Matrix m to current matrix
        """
        raise NotImplementedError

    def Sub(self, m: "Matrix") -> None:
        """
        subtracts values of the Matrix m from current matrix
        """
        raise NotImplementedError

    def Mul(self, s: float) -> None:
        """
        mutiplies Matrix's parameters to s value
        """
        raise NotImplementedError

    def Transform(self, m: "Matrix") -> None:
        """
        applies Matrix m transformation to the current Matrix
        """
        raise NotImplementedError
