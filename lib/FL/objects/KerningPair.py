from __future__ import annotations

class KerningPair(object):
    def __init__(self, kerningpair_or_index=None, value=0):
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
            other = kerningpair_or_index
            self.key = other.key
            self.values = other.values.copy()
        elif isinstance(kerningpair_or_index, int):
            self.key = kerningpair_or_index
            self.value = value
        else:
            raise TypeError

    @property
    def parent(self):
        """
        KerningPair's parent object, Glyph.
        """
        return self._parent

    @property
    def key(self):
        """
        index of right glyph of the pair
        """
        return self._key

    @key.setter
    def key(self, value):
        self._key = value

    @property
    def value(self):
        """
        value of the pair
        """
        return self._values[0]

    @value.setter
    def value(self, value):
        self._values = [value] * len(self._values)

    @property
    def values(self):
        """
        list of values for each master
        """
        return self._values

    @values.setter
    def values(self, value):
        self._values = value


if __name__ == "__main__":
    import doctest
    doctest.testmod()
