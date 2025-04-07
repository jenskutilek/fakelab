from __future__ import annotations

from typing import TYPE_CHECKING

from FL.objects.Point import Point

if TYPE_CHECKING:
    from FL import Glyph, Matrix


class Anchor:
    """
    Anchor - class to represent Anchor point
    """

    __slots__ = ["_parent", "_name", "_x", "_y", "_p", "_mark"]

    # Constructor

    def __init__(
        self, anchor_or_name: Anchor | str | None = None, x: int = 0, y: int = 0
    ) -> None:
        """
        Integer values are accepted as coordinates.

        Args:
            anchor_or_name (Anchor | str | None, optional): An `Anchor` to copy data
                from, or the anchor's name as a string. Defaults to None.
            x (int, optional): Horizontal position of the anchor. Defaults to 0.
            y (int, optional): Vertical position of the anchor. Defaults to 0.
        """
        self._set_defaults()

        # Process params

        if isinstance(anchor_or_name, Anchor):
            # Copy constructor
            raise NotImplementedError

        elif isinstance(anchor_or_name, str):
            self.name = anchor_or_name
            self.x = x
            self.y = y

    def __repr__(self) -> str:
        return f"<Anchor: name={self.name}, x={self.x}, y={self.y}, orphan>"

    def _set_defaults(self) -> None:
        self._name = ""
        self._x = 0
        self._y = 0

        self._mark = 1
        self._parent = None

    # Attributes

    @property
    def parent(self) -> Glyph | None:
        """
        Anchors's parent object, `Glyph`
        """
        return self._parent

    @property
    def name(self) -> str:
        """
        Anchor's name as a string

        Returns:
            str: The name
        """
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def x(self) -> int:
        """
        Horizontal position of the anchor

        Returns:
            int: The x coordinate
        """
        return self._x

    @x.setter
    def x(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError
        self._x = value

    @property
    def y(self) -> int:
        """
        Vertical position of the anchor

        Returns:
            int: The y coordinate
        """
        return self._y

    @y.setter
    def y(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError
        self._y = value

    @property
    def p(self) -> Point:
        """
        Position of the anchor as a `Point` object

        Returns:
            Point: The point
        """
        return Point(self.x, self.y)

    @p.setter
    def p(self, value: Point) -> None:
        self._x = int(value.x)
        self._y = int(value.y)

    @property
    def mark(self) -> int:
        """
        Behaves like the `mark` attribute of the `Glyph` object

        Returns:
            int: The hue in degrees of the mark color
        """
        return self._mark

    @mark.setter
    def mark(self, value: int) -> None:
        self._mark = value

    # Operations

    # Anchor has no operations

    # Methods

    def Transform(self, m: Matrix) -> None:
        """
        Applies Matrix transformation to the Anchor (see `Matrix`)

        Args:
            m (Matrix): The transformation matrix
        """
        p = self.p
        m.fake_transform_point(p)
        self.x = int(p.x)  # TODO: Is truncation to int correct?
        self.y = int(p.y)  # TODO: Is truncation to int correct?
