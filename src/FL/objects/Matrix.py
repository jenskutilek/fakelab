from __future__ import annotations

from typing import TYPE_CHECKING

from FL.helpers.transform import Transform

if TYPE_CHECKING:
    from FL.objects.Point import Point


class Matrix:
    """
    ===============================================
    Matrix - class to represent planar transformations
    ===============================================
    Matrix is used to perform following transformations:
    x1 = x * a + y * b + e
    y1 = x * c + y * d + f
    """

    __slots__ = ["_transform"]

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
        Matrix()                   - generic constructor, creates a Matrix that makes no
                                     change to coordinates
        Matrix(Matrix)             - copy constructor
        Matrix([a, b, c, d, e, f]) - creates a Matrix and assigns coordinates from the
                                     list of float numbers
        Matrix(a, b, c, d, e, f)   - creates a Matrix and assigns coordinates from float
                                     numbers

        Args:
            a (Matrix | list[float] | float | None, optional): xx. Defaults to None.
            b (float | None, optional): xy. Defaults to None.
            c (float | None, optional): yx. Defaults to None.
            d (float | None, optional): yy. Defaults to None.
            e (float | None, optional): dx. Defaults to None.
            f (float | None, optional): dy. Defaults to None.
        """
        self._transform = Transform(1, 0, 0, 1, 0, 0)
        if a is not None:
            self.Assign(a, b, c, d, e, f)

    def __repr__(self) -> str:
        return (
            f"FL.Matrix({self.a:g}, {self.b:g}, {self.c:g}, "
            f"{self.d:g}, {self.e:g}, {self.f:g})"
        )

    # FakeLab additions

    def fake_transform_point(self, p: Point) -> None:
        p.x, p.y = self._transform.transformPoint((p.x, p.y))

    # Attributes

    @property
    def a(self) -> float:
        return self._transform.xx

    @a.setter
    def a(self, value: float) -> None:
        self._transform = Transform(
            float(value),
            self._transform.xy,
            self._transform.yx,
            self._transform.yy,
            self._transform.dx,
            self._transform.dy,
        )

    @property
    def b(self) -> float:
        return self._transform.xy

    @b.setter
    def b(self, value: float) -> None:
        self._transform = Transform(
            self._transform.xx,
            float(value),
            self._transform.yx,
            self._transform.yy,
            self._transform.dx,
            self._transform.dy,
        )

    @property
    def c(self) -> float:
        return self._transform.yx

    @c.setter
    def c(self, value: float) -> None:
        self._transform = Transform(
            self._transform.xx,
            self._transform.xy,
            float(value),
            self._transform.yy,
            self._transform.dx,
            self._transform.dy,
        )

    @property
    def d(self) -> float:
        return self._transform.yy

    @d.setter
    def d(self, value: float) -> None:
        self._transform = Transform(
            self._transform.xx,
            self._transform.xy,
            self._transform.yx,
            float(value),
            self._transform.dx,
            self._transform.dy,
        )

    @property
    def e(self) -> float:
        return self._transform.dx

    @e.setter
    def e(self, value: float) -> None:
        self._transform = Transform(
            self._transform.xx,
            self._transform.xy,
            self._transform.yx,
            self._transform.yy,
            float(value),
            self._transform.dy,
        )

    @property
    def f(self) -> float:
        return self._transform.dy

    @f.setter
    def f(self, value: float) -> None:
        self._transform = Transform(
            self._transform.xx,
            self._transform.xy,
            self._transform.yx,
            self._transform.yy,
            self._transform.dx,
            float(value),
        )

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
            self._transform = Transform(
                a._transform.xx,
                a._transform.xy,
                a._transform.yx,
                a._transform.yy,
                a._transform.dx,
                a._transform.dy,
            )
        elif isinstance(a, list):
            assert len(a) == 6
            self._transform = Transform(*a)
        else:
            for v in (a, b, c, d, e, f):
                if not (isinstance(v, float) or isinstance(v, int)):
                    raise RuntimeError
            self._transform = Transform(a, b, c, d, e, f)

    def Add(self, m: Matrix) -> None:
        """
        Adds values of the Matrix m to current matrix
        """
        self._transform = Transform(
            self.a + m.a,
            self.b + m.b,
            self.c + m.c,
            self.d + m.d,
            self.e + m.e,
            self.f + m.f,
        )

    def Sub(self, m: Matrix) -> None:
        """
        Subtracts values of the Matrix m from current matrix
        """
        self._transform = Transform(
            self.a - m.a,
            self.b - m.b,
            self.c - m.c,
            self.d - m.d,
            self.e - m.e,
            self.f - m.f,
        )

    def Mul(self, s: float) -> None:
        """
        Mutiplies Matrix's parameters to s value
        """
        self._transform = Transform(
            self.a * s,
            self.b * s,
            self.c * s,
            self.d * s,
            self.e * s,
            self.f * s,
        )

    def Transform(self, m: Matrix) -> None:
        """
        applies Matrix m transformation to the current Matrix
        """
        dx = self.e
        dy = self.f
        self._transform = self._transform.transform(m._transform)
        xx, xy, yx, yy, dx2, dy2 = self._transform
        self._transform = Transform(xx, xy, yx, yy, dx2, dy2)
