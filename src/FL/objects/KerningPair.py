from __future__ import annotations

from typing import TYPE_CHECKING

from FL.fake.Base import Copyable
from FL.helpers.FLList import adjust_list

if TYPE_CHECKING:
    from FL.objects.Glyph import Glyph


class KerningPair(Copyable):
    """
    Class to represent kerning pair. This class is Multiple Master-compatible.
    """

    __slots__ = ["_parent", "_key", "_value", "_values"]

    # Constructor

    def __init__(
        self, kerningpair_or_index: KerningPair | int | None = None, value: int = 0
    ) -> None:
        """
        KerningPair()
            generic constructor, creates an empty KerningPair
        KerningPair(KerningPair)
            copy constructor
        KerningPair(index)
            creates a KerningPair to glyph referenced by index but zero value
        KerningPair(index, value)
            creates a KerningPair to glyph referenced by index and assigns value

        Args:
            kerningpair_or_index (KerningPair | int | None, optional): _description_. Defaults to None.
            value (int, optional): _description_. Defaults to 0.
        """
        self._parent = None
        self._key = 0
        self._values = [0] * 16  # An orphan pair has values for all 16 possible masters
        if kerningpair_or_index is None:
            self.key = 0
            self.value = 0
        elif isinstance(kerningpair_or_index, KerningPair):
            self._copy_constructor(kerningpair_or_index)
        elif isinstance(kerningpair_or_index, int):
            self.key = kerningpair_or_index
            self.value = value
        else:
            raise TypeError

    @property
    def fake_parent(self) -> None:
        raise AttributeError

    @fake_parent.setter
    def fake_parent(self, value: Glyph | None) -> None:
        self._parent = value
        if self._parent is None:
            # Pad values list to 16 masters
            adjust_list(self._values, 16, 0)  # TODO: Check if the default is 0
        else:
            # Adjust list length to new layers number
            adjust_list(self._values, self._parent.layers_number)

    # Attributes

    @property
    def parent(self) -> Glyph | None:
        """
        KerningPair's parent object, Glyph.
        """
        return self._parent

    @property
    def key(self) -> int:
        """
        index of right glyph of the pair
        """
        return self._key

    @key.setter
    def key(self, value: int) -> None:
        self._key = value

    @property
    def value(self) -> int:
        """
        value of the pair
        """
        return self._values[0]

    @value.setter
    def value(self, value: int) -> None:
        self._values = [value] * len(self._values)

    @property
    def values(self) -> list[int]:
        """
        list of values for each master
        """
        return self._values

    @values.setter
    def values(self, value: list[int]) -> None:
        raise RuntimeError(
            'Attempt to write read only attribute "values" of class KerningPair'
        )
