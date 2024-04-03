from __future__ import annotations

from copy import copy


class ClassList(list):
    """
    A list of OpenType classes. It keeps track of the class flags.
    """
    # List methods
    def __init__(self, iterable) -> None:
        # Start with empty string
        super().__init__(copy(iterable))
        self._flags = [0 for _ in self]
    
    def __setitem__(self, index, item) -> None:
        super().__setitem__(index, item)
        # self._flags[index] = 0  # ???
    
    def append(self, item) -> None:
        super().append(item)
        self._flags.append(0)
    
    def extend(self, other) -> None:
        super().extend(item for item in other)
        self._flags.extend([0 for _ in range(len(other))])
    
    def insert(self, index, item) -> None:
        super().insert(index, item)
        self._flags.insert(index, 0)
    
    # Methods called by the Font

    def GetClassLeft(self, class_index: int) -> int | None:
        if class_index >= len(self) or class_index < 0:
            return None

        return int(bool(self._flags[class_index] & 1024))

    def GetClassRight(self, class_index: int) -> int | None:
        if class_index >= len(self) or class_index < 0:
            return None

        return int(bool(self._flags[class_index] & 2048))

    def GetClassMetricsFlags(self, class_index: int) -> tuple | None:
        raise NotImplementedError

    def SetClassFlags(self, class_index: int, left: int, right: int, width=None) -> None:
        if width is not None:
            raise NotImplementedError

        if class_index >= len(self) or class_index < 0:
            return

        value = 0
        if left != 0:
            value += 1024
        if right != 0:
            value += 2048
        self._flags[class_index] = value
