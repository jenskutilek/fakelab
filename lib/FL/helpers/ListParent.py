from collections import UserList


class ListParent(UserList):
    """
    Like a list, but sets child element's parent attribute when appending.
    """
    def __init__(self, value=[], parent=None):
        """
        >>> pl = ListParent([1, 2, 3], 4)
        >>> print(pl)
        [1, 2, 3]
        >>> print(pl._parent)
        4
        """
        super(UserList, self).__init__()
        self._parent = parent
        self.data = value

    def __add__(self, value):
        value.parent = self._parent
        return self.data.__add__(value)

    def __iadd__(self, value):
        value.parent = self._parent
        self.data.__iadd__(value)

    def __setitem__(self, index, value):
        value.parent = self._parent
        self.data[index] = value

    def __setslice__(self, i, j, value):
        raise NotImplementedError

    def append(self, obj):
        obj.parent = self._parent
        self.data.append(obj)

    def extend(self, iterable):
        for obj in iterable:
            self.data.append(obj)

    def insert(self, index, obj):
        """
        >>> pl = ListParent([1, 3])
        """
        obj.parent = self._parent
        self.data.insert(obj)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
