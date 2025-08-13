from __future__ import annotations

from typing import TYPE_CHECKING

from FL.fake.Base import Copyable

if TYPE_CHECKING:
    from FL.objects.Point import Point


class Matrix(Copyable):
    """
    Matrix - class to represent planar transformations
    """

    __slots__ = ["_a", "_b", "_c", "_d", "_e", "_f"]

    # Constructor

    def __init__(
        self,
        a: Matrix | list[float] | float | None = None,
        b: float | None = None,
        c: float | None = None,
        d: float | None = None,
        e: float | None = None,
        f: float | None = None,
    ) -> None:
        """
        Matrix()
            generic constructor, creates a Matrix that makes no change to coordinates
        Matrix(Matrix)
            copy constructor
        Matrix([a, b, c, d, e, f])
            creates a Matrix and assigns coordinates from the list of float numbers
        Matrix(a, b, c, d, e, f)
            creates a Matrix and assigns coordinates from float numbers

        Args:
            a (Matrix | list[float] | float | None, optional): xx. Defaults to None.
            b (float | None, optional): xy. Defaults to None.
            c (float | None, optional): yx. Defaults to None.
            d (float | None, optional): yy. Defaults to None.
            e (float | None, optional): dx. Defaults to None.
            f (float | None, optional): dy. Defaults to None.
        """
        self._a: float = 1
        self._b: float = 0
        self._c: float = 0
        self._d: float = 1
        self._e: float = 0
        self._f: float = 0
        if a is not None:
            if isinstance(a, Matrix):
                self._copy_constructor(a)
            else:
                self.Assign(a, b, c, d, e, f)

    def __repr__(self) -> str:
        return (
            f"FL.Matrix({self.a:g}, {self.b:g}, {self.c:g}, "
            f"{self.d:g}, {self.e:g}, {self.f:g})"
        )

    # FakeLab additions

    def fake_transform_point(self, p: Point) -> None:
        """
        Matrix is used to perform following transformations:

            x1 = x * a + y * b + e
            y1 = x * c + y * d + f

        Args:
            p (Point): The point to be transformed
        """
        x = p.x
        y = p.y
        p.x = x * self.a + y * self.b + self.e
        p.y = x * self.c + y * self.d + self.f

    # Attributes

    @property
    def a(self) -> float:
        return self._a

    @a.setter
    def a(self, value: float) -> None:
        self._a = float(value)

    @property
    def b(self) -> float:
        return self._b

    @b.setter
    def b(self, value: float) -> None:
        self._b = float(value)

    @property
    def c(self) -> float:
        return self._c

    @c.setter
    def c(self, value: float) -> None:
        self._c = float(value)

    @property
    def d(self) -> float:
        return self._d

    @d.setter
    def d(self, value: float) -> None:
        self._d = float(value)

    @property
    def e(self) -> float:
        return self._e

    @e.setter
    def e(self, value: float) -> None:
        self._e = float(value)

    @property
    def f(self) -> float:
        return self._f

    @f.setter
    def f(self, value: float) -> None:
        self._f = float(value)

    # Operations

    def __add__(self, other: Matrix) -> Matrix:
        """
        Matrix must be second operand, all parameters are added
        """
        return Matrix(
            self.a + other.a,
            self.b + other.b,
            self.c + other.c,
            self.d + other.d,
            self.e + other.e,
            self.f + other.f,
        )

    def __sub__(self, other: Matrix) -> Matrix:
        """
        Matrix must be second operand, all parameters are subtracted
        """
        return Matrix(
            self.a - other.a,
            self.b - other.b,
            self.c - other.c,
            self.d - other.d,
            self.e - other.e,
            self.f - other.f,
        )

    def __mul__(self, other: Matrix | float) -> Matrix:
        """
        multiply (with Matrix) - matrixes are multiplied
        multiply (with float number) - all parameters are scaled by the operand
        """
        if isinstance(other, Matrix):
            m = Matrix(self)
            m.Transform(other)
            return m
        else:
            # float
            return Matrix(
                self.a * other,
                self.b * other,
                self.c * other,
                self.d * other,
                self.e * other,
                self.f * other,
            )

    # Methods

    def Assign(
        self,
        a: Matrix | list[float] | float | None,
        b: float | None = None,
        c: float | None = None,
        d: float | None = None,
        e: float | None = None,
        f: float | None = None,
    ) -> None:
        """
        assigns new values to a Matrix, uses the same syntax as in constructors
        """
        if isinstance(a, Matrix):
            self._a = a.a
            self._b = a.b
            self._c = a.c
            self._d = a.d
            self._e = a.e
            self._f = a.f
        elif isinstance(a, list):
            assert len(a) == 6
            self._a, self._b, self._c, self._d, self._e, self._f = a
        else:
            for v in (a, b, c, d, e, f):
                if not (isinstance(v, float) or isinstance(v, int)):
                    raise RuntimeError
            self._a = a
            self._b = b
            self._c = c
            self._d = d
            self._e = e
            self._f = f

    def Add(self, m: Matrix) -> None:
        """
        Adds values of the Matrix m to current matrix
        """
        self.a += m.a
        self.b += m.b
        self.c += m.c
        self.d += m.d
        self.e += m.e
        self.f += m.f

    def Sub(self, m: Matrix) -> None:
        """
        Subtracts values of the Matrix m from current matrix
        """
        self.a -= m.a
        self.b -= m.b
        self.c -= m.c
        self.d -= m.d
        self.e -= m.e
        self.f -= m.f

    def Mul(self, s: float) -> None:
        """
        Mutiplies Matrix's parameters to s value
        """
        self.a *= s
        self.b *= s
        self.c *= s
        self.d *= s
        self.e *= s
        self.f *= s

    def Transform(self, m: Matrix) -> None:
        """
        Applies Matrix m transformation to the current Matrix
        """
        A = [[self.a, self.c], [self.b, self.d], [self.e, self.f]]
        B = [[m.a, m.c], [m.b, m.d]]
        result = [
            [sum(a * b for a, b in zip(A_row, B_col)) for B_col in zip(*B)]
            for A_row in A
        ]
        (a, c), (b, d), (e, f) = result
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e + m.e
        self.f = f + m.f
