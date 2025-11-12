from __future__ import annotations

from typing import TYPE_CHECKING

from FL.fake.Base import Copyable
from FL.helpers.interpolation import add_axis_to_list, remove_axis_from_point_list
from FL.objects.Point import Point

if TYPE_CHECKING:
    from FL.objects.Glyph import Glyph
    from FL.objects.Matrix import Matrix


__doc__ = "Class to represent an anchor point"


class Anchor(Copyable):
    """
    Anchor - class to represent Anchor point
    """

    __slots__ = ["_mark", "_name", "_parent", "_points", "_reserved"]

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
            self._copy_constructor(anchor_or_name)

        elif isinstance(anchor_or_name, str):
            self.name = anchor_or_name
            self.x = x
            self.y = y

    def __repr__(self) -> str:
        if self._parent is None:
            return f"<Anchor: name={self.name}, x={self.x}, y={self.y}, orphan>"
        return f"<Anchor: name={self.name}, x={self.x}, y={self.y}, active refernce>"

    def _set_defaults(self) -> None:
        self._parent = None
        self._name = ""

        self._mark = 1
        self._reserved = 0
        self._points = [Point() for _ in range(16)]

    def fake_add_axis(self) -> None:
        add_axis_to_list(self._points)

    def fake_remove_axis(self, interpolation: float) -> None:
        remove_axis_from_point_list(self._points, interpolation)

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
        return int(self._points[0].x)

    @x.setter
    def x(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError
        for p in self._points:
            p.x = value

    @property
    def y(self) -> int:
        """
        Vertical position of the anchor

        Returns:
            int: The y coordinate
        """
        return int(self._points[0].y)

    @y.setter
    def y(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError
        for p in self._points:
            p.y = value

    @property
    def p(self) -> Point:
        """
        Position of the anchor as a `Point` object

        Returns:
            Point: The point
        """
        return self._points[0]

    @p.setter
    def p(self, value: Point) -> None:
        # Truncates any floats
        x = int(value.x)
        y = int(value.y)
        for p in self._points:
            p.x = x
            p.y = y

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
        # TODO: clamp to 0 to 65535
        # actually: -1 -> 65535, 65536 -> 0 etc.
        self._mark = value

    # Operations

    # Anchor has no operations

    # Methods

    def Layer(self, masterindex: int) -> Point:
        """
        Returns point for the master `masterindex`.
        """
        return self._points[masterindex]

    def SetLayer(self, masterindex: int, point: Point) -> None:
        """
        Set the point for the master `masterindex`.
        """
        pt = self._points[masterindex]
        pt.x = int(point.x)
        pt.y = int(point.y)

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
