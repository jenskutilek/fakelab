from __future__ import annotations

from collections import UserList
from copy import copy
from typing import Any, Iterable


class ClassList(UserList):
    """
    A list of OpenType classes as strings. It keeps track of the class flags.
    """

    # List methods
    def __init__(self, iterable: Iterable | None = None) -> None:
        super().__init__(iterable)
        self._flags = [0 for _ in iterable]

    def __add__(self, item: Any) -> ClassList:
        result = ClassList(self.data)
        result._flags = copy(self._flags)
        result += item
        return result

    def __iadd__(self, item: Any) -> ClassList:
        self._flags.append(0)
        self.data.__iadd__(item)
        return self

    def __setitem__(self, index: int, item: Any) -> None:
        # Not implemented, it does nothing
        pass

    def append(self, item: Any) -> None:
        # WTF ... append does not work on the classes list
        pass

    def extend(self, iterable: Iterable) -> None:
        # extend does not work either
        pass

    def insert(self, index: int, item: Any) -> None:
        # You guessed it
        pass

    # Methods called by the Font

    def GetClassLeft(self, class_index: int) -> int | None:
        if class_index >= len(self.data) or class_index < 0:
            return None

        return int(bool(self._flags[class_index] & 1024))

    def GetClassRight(self, class_index: int) -> int | None:
        if class_index >= len(self.data) or class_index < 0:
            return None

        return int(bool(self._flags[class_index] & 2048))

    def GetClassMetricsFlags(self, class_index: int) -> tuple | None:
        raise NotImplementedError

    def SetClassFlags(
        self,
        class_index: int,
        left_lsb: bool,
        right_rsb: bool,
        width: bool | None = None,
    ) -> None:
        if width is not None:
            # Applies to metrics classes
            raise NotImplementedError

        if class_index >= len(self.data) or class_index < 0:
            return

        value = 0
        if left_lsb:
            value += 1024
        if right_rsb:
            value += 2048
        self._flags[class_index] = value
