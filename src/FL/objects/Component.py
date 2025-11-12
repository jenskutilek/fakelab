from __future__ import annotations

from typing import TYPE_CHECKING

from FL.fake.Base import Copyable
from FL.helpers.interpolation import add_axis_to_list, remove_axis_from_point_list
from FL.objects.Point import Point

if TYPE_CHECKING:
    from FL.objects.Font import Font
    from FL.objects.Glyph import Glyph


__doc__ = "Class to represent a glyph component"


class Component(Copyable):
    """
    Component - class to represent glyph component

    Components are defined by the glyph index which they reference,
    Shift of components origin point and scale factor of a component
    Scale is measured in relation to 1.0, so 100% scale is 1.0 and 60% - 0.6
    This class is Multiple Master - compatible
    """

    __slots__ = ["_deltas", "_scales", "_index", "_parent"]

    # Constructor

    def __init__(
        self,
        component_or_index: Component | int | None = None,
        delta: Point | None = None,
        scale: Point | None = None,
    ) -> None:
        """
        Component()
            generic constructor, creates an empty Component
        Component(Component)
            copy constructor
        Component(index)
            creates component referencing glyph index with zero shift and 100% scale
        Component(index, Point(integer) delta)
            creates component referencing glyph index with delta shift and 100% scale
        Component(index, Point(integer) delta, Point(float) scale)
            creates component referencing glyph index with delta shift and scale factor
            defined by scale

        Args:
            component_or_index (Component | int | None, optional): _description_. Defaults to None.
            delta (Point | None, optional): _description_. Defaults to None.
            scale (Point | None, optional): _description_. Defaults to None.
        """
        # Init with max num masters and -1 reference glyph
        self._deltas = [Point(0, 0)] * 16
        self._scales = [Point(1.0, 1.0)] * 16
        self._index = -1
        self._parent: Glyph | None = None

        if isinstance(component_or_index, Component):
            self._copy_constructor(component_or_index)

        elif isinstance(component_or_index, int):
            self._index = component_or_index
            if delta is not None:
                self.delta = delta
                if scale is not None:
                    self.scale = scale
        # else: Empty Component

    # Additions for FakeLab

    def fake_deserialize(
        self, num_masters: int, data: dict[str, int | list[float]]
    ) -> None:
        self.index = data.get("gid", -1)
        self._deltas = [
            Point(data["offsetX"][i], data["offsetY"][i]) for i in range(num_masters)
        ]
        self._scales = [
            Point(data["scaleX"][i], data["scaleY"][i]) for i in range(num_masters)
        ]

    def fake_serialize(self) -> dict[str, int | list[int | float]]:
        d = {
            "gid": self.index,
            "offsetX": [int(p.x) for p in self.deltas],  # FIXME: Round or int?
            "offsetY": [int(p.y) for p in self.deltas],  # FIXME: Round or int?
            "scaleX": [p.x for p in self.scales],
            "scaleY": [p.y for p in self.scales],
        }
        return d

    def fake_add_axis(self) -> None:
        add_axis_to_list(self._deltas)
        add_axis_to_list(self._scales)

    def fake_remove_axis(self, interpolation: float) -> None:
        remove_axis_from_point_list(self._deltas, interpolation)
        remove_axis_from_point_list(self._scales, interpolation)

    # Attributes

    @property
    def parent(self) -> Glyph | None:
        """
        parent object, Glyph
        """
        return self._parent

    @property
    def index(self) -> int:
        """
        referencing glyph index
        """
        return self._index

    @index.setter
    def index(self, value: int) -> None:
        self._index = value

    @property
    def delta(self) -> Point:
        # TODO: What is the point's parent?
        return self._deltas[0]

    @delta.setter
    def delta(self, value: Point) -> None:
        """
        Shift value

        When setting the shift through this method, the value is used for all masters.

        Args:
            value (Point): _description_
        """
        self._deltas = [Point(int(value.x), int(value.y))] * len(self._deltas)

    @property
    def scale(self) -> Point:
        """
        scale factor
        """
        # TODO: What is the point's parent?
        return self._scales[0]

    @scale.setter
    def scale(self, value: Point) -> None:
        """
        scale factor

        Args:
            value (Point): _description_

        When setting the scale through this method, the value is used for all masters.
        """
        # TODO: What is the point's parent?
        self._scales = [Point(value.x, value.y)] * len(self._scales)

    @property
    def deltas(self) -> list[Point]:
        """
        list of shift values for each master

        Setting the list, or only one item of the list doesn't work in FL.
        You need to get one of the points and modify it directly
        """
        # TODO: parent of the points must be the deltas list
        return self._deltas

    @deltas.setter
    def deltas(self, value: list[Point]) -> None:
        # Setting the list, or only one item of the list doesn't work in FL.
        # You need to get one of the points and modify it directly
        raise RuntimeError(
            'Attempt to write read only attribute "deltas" of class Component'
        )

    @property
    def scales(self) -> list[Point]:
        """
        list of scale values for each master

        Setting the list, or only one item of the list doesn't work in FL.
        You need to get one of the points and modify it directly
        """
        # TODO: parent of the points must be the scales list
        return self._scales

    @scales.setter
    def scales(self, value: list[Point]) -> None:
        raise RuntimeError(
            'Attempt to write read only attribute "scales" of class Component'
        )

    # Operations: none

    # Methods

    def Get(self, f: Font | None = None) -> Glyph:
        """
        Creates a glyph from component applying delta and scale transformations.

        Font parameter is not needed when component has a parent
        FIXME: Apparently, the font parameter is always needed

        Args:
            f (Font | None, optional): _description_. Defaults to None.
        """
        if f is None:
            raise RuntimeError(
                "In order to get glyph using component created from orphan glyph "
                "specify source font"
            )
        raise NotImplementedError

    def Paste(self) -> None:
        """
        Appends component to a parent glyph as a set of outlines.

        Component must have a parent
        """
        raise NotImplementedError
