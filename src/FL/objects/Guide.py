from __future__ import annotations

from math import atan2, degrees, radians, tan
from typing import TYPE_CHECKING

from FL.fake.Base import Copyable
from FL.helpers.interpolation import add_axis_to_list, remove_axis_from_list

if TYPE_CHECKING:
    from FL.objects.Glyph import Glyph
    from FL.objects.Matrix import Matrix


__doc__ = "Class to represent a guideline"


class Guide(Copyable):
    # Constructor

    __slots__ = ["_angles", "_color", "_name", "_parent", "_positions", "_widths"]

    def __init__(
        self, guide_or_position: Guide | int | None = None, angle: float = 0.0
    ) -> None:
        """
        Guide - class to represent guideline

        Guide()
            generic constructor, creates a Guide with zero coordinates
        Guide(Guide)
            copy constructor
        Guide(position)
            creates a Guide and assigns position
        Guide(position, angle)
            creates a Guide and assigns position and width values

        Args:
            guide_or_position (Guide | int | None, optional): The guide to be copied,
                or the position of the guide. Defaults to None.
            angle (float, optional): The width. Defaults to 0.0.
        """
        self._parent: Glyph | None = None
        self._positions: list[int] = [0] * 16
        self._widths: list[int] = [21] * 16  # WTF

        # Without API:
        self._color: str | None = None
        self._name: str | None = None

        # Process params

        if isinstance(guide_or_position, Guide):
            self._copy_constructor(guide_or_position)

        elif isinstance(guide_or_position, int):
            self.position = guide_or_position
            if angle is not None:
                self.angle = angle
        # else: Empty guide

    def __repr__(self) -> str:
        return f"<Guide pos: {self.position}, angle: {self.angle}>"

    @staticmethod
    def fake_angle_to_width(angle: float) -> int:
        return min(10000, round(tan(radians(angle)) * 10000))

    @staticmethod
    def fake_width_to_angle(width: float) -> float:
        return degrees(atan2(width, 10000))

    def fake_add_axis(self) -> None:
        add_axis_to_list(self._positions)
        add_axis_to_list(self._widths)

    def fake_remove_axis(self, interpolation: float) -> None:
        remove_axis_from_list(self._positions, interpolation)
        remove_axis_from_list(self._widths, interpolation)

    @property
    def angle(self) -> float:
        """The angle of the guideline.

        Returns:
            float: The angle of the guideline in degrees for the first master
        """
        return self.fake_width_to_angle(self.width)

    @angle.setter
    def angle(self, value: float) -> None:
        self.width = self.fake_angle_to_width(value)

    @property
    def parent(self) -> Glyph | None:
        """Guide's parent object, `Glyph`. If the guide is global, parent is an orphan
        `Glyph`.

        Returns:
            Glyph | None: The parent object.
        """
        return self._parent

    @property
    def position(self) -> int:
        """The position of the guideline. Setting the position sets the same value for
        all masters.

        Returns:
            int: Return position of the guideline for the first master
        """
        return self._positions[0]

    @position.setter
    def position(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError

        num_masters = len(self._positions)
        self._positions.clear()
        self._positions.extend([value] * num_masters)

    @property
    def positions(self) -> list[int]:
        return self._positions

    @positions.setter
    def positions(self, value: list[int]) -> None:
        raise RuntimeError(
            'Attempt to write read only attribute "positions" of class Guide'
        )

    @property
    def width(self) -> float:
        """The "width" of the guideline. Setting the width sets the same value for
        all masters. Actually, the width is a representation of the angle:
        `width = round(tan(radians(value)) * 10000)`

        Returns:
            int: Return "width" of the guideline for the first master
        """
        return float(self._widths[0])

    @width.setter
    def width(self, value: float) -> None:
        num_masters = len(self._widths)
        self._widths.clear()
        self._widths.extend([int(value)] * num_masters)

    @property
    def widths(self) -> list[int]:
        """The "widths for each master. Actually, the width is a representation of the
        angle: `width = round(tan(radians(value)) * 10000)`

        Returns:
            list[int]: The list of "widths"
        """
        # The angle for each master
        return self._widths

    @widths.setter
    def widths(self, value: list[float]) -> None:
        raise RuntimeError(
            'Attempt to write read only attribute "widths" of class Guide'
        )

    # Methods

    def Transform(self, m: Matrix) -> None:
        """applies Matrix transformation to the Guide

        Args:
            m (Matrix): _description_
        """
        raise NotImplementedError

    def TransformLayer(self, m: Matrix, layernum: int) -> None:
        """applies Matrix transformation to the selected layer of the Guide

        Args:
            m (Matrix): _description_
        """
        raise NotImplementedError
