from __future__ import annotations

from collections import UserList
from copy import copy
from typing import Any, Iterable, List


class ClassList(UserList):
    """
    A list of OpenType classes as strings. It keeps track of the class flags.
    """

    def __init__(
        self, iterable: Iterable[str] | None = None, flags: List[int] | None = None
    ) -> None:
        super().__init__(iterable)
        if flags is None:
            self._flags = [0 for _ in iterable or []]
        else:
            self._flags = flags
            # Make sure the _flags list is as long as the data list
            len_f = len(self._flags)
            len_i = len(self.data)
            if len_f != len_i:
                self._flags = self._flags[:len_i] + [0] * (len_i - len_f)

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
