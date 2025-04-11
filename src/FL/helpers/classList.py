from __future__ import annotations

from collections import UserList
from copy import copy
from typing import Any, Iterable


class ClassList(UserList[str]):
    """
    A list of OpenType classes as strings. It keeps track of the class flags.
    """

    __slots__ = ["_flags", "_kerning_flags", "_metrics_flags", "_names"]

    def __init__(
        self,
        iterable: Iterable[str] | None = None,
        old_list: ClassList | None = None,
    ) -> None:
        super().__init__(iterable)
        self._flags = [0 for _ in iterable or []]
        self._kerning_flags: dict[str, list[int]] = {}
        self._metrics_flags: dict[str, list[int]] = {}
        self._names: list[str] = []
        self._update_flags()

    # Internal

    def _get_class_name(self, class_string: str) -> str:
        if ":" not in class_string:
            raise ValueError
        name, _contents = class_string.split(":", 1)
        return name.strip()

    def _update_names(self) -> None:
        # Mapping from name to class index?
        self._names = [
            name
            for name in [
                self._get_class_name(class_string) for class_string in self.data
            ]
        ]

    def _update_flags(self) -> None:
        # Match classes from the old list so they can keep their flags
        # for cur_index, class_string in enumerate(self.data):
        #     try:
        #         old_index = old_list.data.index(class_string)
        #     except ValueError:
        #         continue

        #     self._flags[cur_index] = old_list._flags[old_index]

        print("_update_flags")

        # Reset flags
        self._flags = [0] * len(self.data)

        if not self._flags:
            return

        # Make a list of all class types
        self._update_names()

        # Set kerning flags
        for name, flags in self._kerning_flags.items():
            class_index = self._names.index(name)
            self._flags[class_index] = flags[0]

        # Set metrics flags
        for name, flags in self._metrics_flags.items():
            class_index = self._names.index(name)
            self._flags[class_index] = flags[1]

    @property
    def fake_metrics_flags(self) -> dict[str, list[int]]:
        # Called from FL.vfb.writer
        # Serialize
        pass

    @fake_metrics_flags.setter
    def fake_metrics_flags(self, value: dict[str, list[int]]) -> None:
        # Called from FL.vfb.reader
        self._metrics_flags = value

    @property
    def fake_kerning_flags(self) -> dict[str, list[int]]:
        # Called from FL.vfb.writer
        pass

    @fake_kerning_flags.setter
    def fake_kerning_flags(self, value: dict[str, list[int]]) -> None:
        # Called from FL.vfb.reader
        self._kerning_flags = value

    def fake_set_classes(self, classes: list[str]) -> None:
        # Called from FL.vfb.reader
        self.data = classes
        print("fake_set_classes:", self.data)
        self._update_flags()

    # Operations

    def __add__(self, item: Any) -> ClassList:
        result = ClassList(self.data)
        result._kerning_flags = copy(self._kerning_flags)
        result._metrics_flags = copy(self._metrics_flags)
        result += item
        return result

    def __iadd__(self, item: Any) -> ClassList:
        # self._flags.append(0)
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

        flags = self._flags[class_index]
        if flags & 1:
            # Metrics class
            return 0

        return int(bool(flags & 1024))

    def GetClassRight(self, class_index: int) -> int | None:
        if class_index >= len(self.data) or class_index < 0:
            return None

        flags = self._flags[class_index]
        if flags & 1:
            # Metrics class
            return 0

        return int(bool(flags & 2048))

    def GetClassMetricsFlags(self, class_index: int) -> tuple | None:
        if class_index >= len(self.data) or class_index < 0:
            return None

        flags = self._flags[class_index]
        if not flags & 1:
            return (0, 0, 0)
        return (
            int(bool(flags & 1024)),  # L
            int(bool(flags & 2048)),  # R
            int(bool(flags & 4096)),  # W
        )

    def SetClassFlags(
        self,
        class_index: int,
        left_lsb: bool | int,
        right_rsb: bool | int,
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
