import logging
from typing import TYPE_CHECKING

from vfbLib.typing import HintDict

from FL.constants import DIR_HORIZONTAL, DIR_UNDEFINED, DIR_VERTICAL
from FL.fake.Base import Copyable
from FL.helpers.interpolation import add_axis_to_list, remove_axis_from_list
from FL.objects.Link import Link
from FL.objects.Point import Point

if TYPE_CHECKING:
    from FL.objects.Glyph import Glyph
    from FL.objects.Matrix import Matrix


__doc__ = "Class to represent a PostScript hint"


logger = logging.getLogger(__name__)


class Hint(Copyable):
    """
    Hint - class to represent hint

    This class is Multiple Master - compatible
    """

    __slots__ = ["_parent", "_positions", "_widths", "_stem_direction"]

    # Constructor

    def __init__(
        self, hint_or_position: "Hint | int | None" = None, width: int | None = None
    ) -> None:
        """
        Hint()
            generic constructor, creates a Hint with zero coordinates
        Hint(Hint)
            copy constructor
        Hint(position, width)
            creates a Hint and assigns position and width values

        Args:
            hint_or_position (Hint | int | None): _description_
            width (int | None, optional): _description_. Defaults to None.
        """
        self._parent: "Glyph | None" = None
        self._positions: list[int] = [0] * 16
        self._widths: list[int] = [21] * 16
        self._stem_direction = DIR_UNDEFINED

        arg1 = hint_or_position
        arg2 = width

        if arg1 is not None:
            if isinstance(arg1, Hint):
                if arg2 is None:
                    self._copy_constructor(arg1)
                else:
                    raise TypeError(
                        "TypeError: int() argument must be a string or a number, "
                        "not 'Hint'"
                    )
            elif isinstance(arg1, int):
                self.position = arg1
                if arg2 is not None:
                    self.width = arg2
            else:
                raise RuntimeError("Hint type is expected in arg 1: Hint(Hint)")

    def _transform_horizontal(self, matrix: "Matrix") -> None:
        # FIXME: Does this handle MM?
        p0 = Point(0, self.position)
        p1 = Point(0, self.position + self.width)
        p0.Transform(matrix)
        p1.Transform(matrix)
        pos0, pos1 = sorted([p0.y, p1.y])
        if self.width in (-20, -21):
            if matrix.d < 0:
                # Vertically flipped
                if self.width == -21:
                    # Handle inverted bottom ghost hint, now top
                    self.position = int(pos1)
                    self.width = -20
                elif self.width == -20:
                    # Handle inverted top ghost hint, now bottom
                    self.position = int(pos1)
                    self.width = -21
                else:
                    logger.error(f"Can't handle transformed hint: {self}, {matrix}")
            elif self.width == -21:
                # Handle normal bottom ghost hint
                self.position = int(pos0 + 21)
            elif self.width == -20:
                # Handle normal top ghost hint
                self.position = int(pos0 + 20)
            else:
                logger.error(f"Can't handle transformed hint: {self}, {matrix}")
        else:
            self.position = int(pos0)
            self.width = int(pos1 - pos0)

    def _transform_vertical(self, matrix: "Matrix") -> None:
        # FIXME: Does this handle MM?
        p0 = Point(self.position, 0)
        p1 = Point(self.position + self.width, 0)
        p0.Transform(matrix)
        p1.Transform(matrix)
        pos0, pos1 = sorted([p0.x, p1.x])
        self.position = int(pos0)
        self.width = int(pos1 - pos0)

    def __repr__(self) -> str:
        if self._parent is None:
            return f"<Hint: p={self.position}, w={self.width}, orphan>"
        if self._stem_direction == DIR_HORIZONTAL:
            name = "HHint"
        elif self._stem_direction == DIR_VERTICAL:
            name = "VHint"
        else:
            name = "Hint"
        return f'<{name}: p={self.position}, w={self.width}, parent: "{self._parent.name}">'

    def _copy_constructor(self, other: "Hint") -> None:
        self._stem_direction = other._stem_direction
        self._positions = other._positions[:]
        self._widths = other._widths[:]

    # Additions for FakeLab

    def fake_deserialize(self, data: list[HintDict]) -> None:
        self._positions = []
        self._widths = []
        for hint_dict in data:
            self._positions.append(hint_dict["pos"])
            self._widths.append(hint_dict["width"])

    def fake_serialize(self) -> list[HintDict]:
        # TODO: Unused, move logic from Glyph.fake_serialize_hints here
        hint_dicts = []
        hint_dict = HintDict()
        hint_dicts.append(hint_dict)
        return hint_dicts

    def fake_add_axis(self) -> None:
        add_axis_to_list(self._positions)
        add_axis_to_list(self._widths)

    def fake_remove_axis(
        self,
        index: int,
        interpolation: float,
        round_values: bool,
        num_masters: int = -1,
    ) -> None:
        remove_axis_from_list(
            self._positions, index, interpolation, round_values, num_masters
        )
        remove_axis_from_list(
            self._widths, index, interpolation, round_values, num_masters
        )

    # Attributes

    @property
    def parent(self) -> "Glyph | None":
        """
        Hint's parent object, `Glyph`

        Returns:
            Glyph | None: _description_
        """
        return self._parent

    @property
    def position(self) -> int:
        """
        Position of the hint

        Returns:
            int: The position of the hint in the first master
        """
        return self._positions[0]

    @position.setter
    def position(self, value: int) -> None:
        # Sets the position for all masters
        # TODO: Must we keep the list, or could we just replace it?
        for i in range(16):
            self._positions[i] = value

    @property
    def width(self) -> int:
        """
        Width of the hint

        Returns:
            int: The width of the hint in the first master
        """
        return self._widths[0]

    @width.setter
    def width(self, value: int) -> None:
        # Sets the width for all masters
        # TODO: Must we keep the list, or could we just replace it?
        for i in range(16):
            self._widths[i] = value

    @property
    def positions(self) -> list[int]:
        """
        List of positions for each master

        Returns:
            list[int]: _description_
        """
        return self._positions

    @positions.setter
    def positions(self, value: list[int]) -> None:
        raise RuntimeError(
            'Attempt to write read only attribute "positions" of class Hint'
        )

    @property
    def widths(self) -> list[int]:
        """
        List of widths for each master

        Returns:
            list[int]: _description_
        """
        return self._widths

    @widths.setter
    def widths(self, value: list[int]) -> None:
        raise RuntimeError(
            'Attempt to write read only attribute "widths" of class Hint'
        )

    # Operations: none

    # Methods

    def ToLink(self) -> Link:
        """
        Transforms hint to Link (and returns it as a result) using parent as a source of
        node coordinates. Parent must exist

        Returns:
            Link: The Link.
        """
        # TODO: If this works at all in FontLab, I haven't managed to get it working
        raise RuntimeError(
            "In order to be converted to a Link, Hint must not be an orphan"
        )

    def Transform(self, m: "Matrix") -> None:
        """
        Apply Matrix transformation to the Hint (see Matrix().__doc__)

        Args:
            m (Matrix): The transformation matrix
        """
        if self._stem_direction == DIR_HORIZONTAL:
            self._transform_horizontal(m)
        elif self._stem_direction == DIR_VERTICAL:
            self._transform_vertical(m)
        else:
            raise NotImplementedError(
                "Don't know how to transform hint without specified direction"
            )

    def TransformLayer(self, m: "Matrix", layernum: int) -> None:
        """
        Apply Matrix transformation to the selected layer of the Hint

        Args:
            m (Matrix): _description_
            layernum (int): _description_
        """
        raise NotImplementedError
