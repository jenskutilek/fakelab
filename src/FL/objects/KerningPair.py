from __future__ import annotations

from typing import TYPE_CHECKING

from FL.fake.Base import Copyable

if TYPE_CHECKING:
    from FL.objects.Glyph import Glyph


class KerningPair(Copyable):

    # Constructor

    def __init__(
        self, kerningpair_or_index: KerningPair | int | None = None, value: int = 0
    ) -> None:
        """
        Class to represent kerning pair. This class is Multiple
        Master-compatible.

        >>> k = KerningPair()
        >>> print(k.key)
        0
        >>> print(k.value)
        0
        >>> print(k.values)
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        """
        self._parent = None
        self._key = 0
        self._values = [0] * 16
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
        self._values = value
