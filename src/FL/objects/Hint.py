from __future__ import annotations

from typing import TYPE_CHECKING

from FL.fake.Base import Copyable
from FL.objects.Link import Link

if TYPE_CHECKING:
    from FL.objects.Glyph import Glyph
    from FL.objects.Matrix import Matrix


class Hint(Copyable):
    """
    Hint - class to represent hint

    This class is Multiple Master - compatible
    """

    __slots__ = ["_parent", "_position", "_width", "_positions", "_widths"]

    # Constructor

    def __init__(
        self, hint_or_position: Hint | int | None = None, width: int | None = None
    ) -> None:
        """
        Hint()                - generic constructor,
                                creates a Hint with zero coordinates
        Hint(Hint)            - copy constructor
        Hint(position, width) - creates a Hint and assigns position and width values

        Args:
            hint_or_position (Hint | int | None): _description_
            width (int | None, optional): _description_. Defaults to None.
        """
        self._parent: Glyph | None = None
        self._positions = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self._widths = [21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21]
        self.position = 0
        self.width = 21

        arg1 = hint_or_position

        # FIXME:
        # If the second argument is present, it determines what is expected as the
        # first argument:
        # h = Hint()
        # b = Hint(h, 1)
        # TypeError: int() argument must be a string or a number, not 'Hint'
        #
        # We have it backwards at the moment: If the first argument is a Hint, the
        # second argument is ignored.

        if arg1 is not None:
            if isinstance(arg1, Hint):
                self._copy_constructor(arg1)
            elif isinstance(arg1, int):
                self.position = arg1
                if width is not None:
                    self.width = width
            else:
                raise RuntimeError("Hint type is expected in arg 1: Hint(Hint)")

    # Attributes

    @property
    def parent(self) -> Glyph | None:
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
            int: _description_
        """
        return self._position

    @position.setter
    def position(self, value: int) -> None:
        self._position = value
        # Sets the position for all masters
        # TODO: Must we keep the list, or could we just replace it?
        for i in range(16):
            self._positions[i] = value

    @property
    def width(self) -> int:
        """
        width of the hint

        Returns:
            int: _description_
        """
        return self._width

    @width.setter
    def width(self, value: int) -> None:
        self._width = value
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
        raise NotImplementedError

    def Transform(self, m: Matrix) -> None:
        """
        Apply Matrix transformation to the Hint (see Matrix().__doc__)

        Args:
            m (Matrix): _description_
        """
        raise NotImplementedError

    def TransformLayer(self, m: Matrix, layernum: int) -> None:
        """
        Apply Matrix transformation to the selected layer of the Hint

        Args:
            m (Matrix): _description_
            layernum (int): _description_
        """
        raise NotImplementedError
