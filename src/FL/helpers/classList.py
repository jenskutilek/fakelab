from __future__ import annotations

from collections import UserList
from copy import copy
from typing import Any, Iterable, SupportsIndex


class ClassList(UserList[str]):
    """
    A list of OpenType classes as strings. It keeps track of the class flags.
    """

    __slots__ = ["_kerning_flags", "_metrics_flags"]

    def __init__(self, iterable: Iterable[str] | None = None) -> None:
        super().__init__(iterable)
        self._kerning_flags: dict[str, tuple[int, int]] = {}
        self._metrics_flags: dict[str, tuple[int, int, int]] = {}

    # Internal

    def _get_class_name(self, class_string: str) -> str:
        if ":" not in class_string:
            raise ValueError
        name, _contents = class_string.split(":", 1)
        return name.strip()

    def fake_deserialize_class(self, data: str) -> None:
        # Deserialize a class without minding the flags.
        # Called from FL.vfb.reader
        self.data.append(data)

    def fake_deserialize_kerning_class_flags(
        self, data: dict[str, tuple[int, int]]
    ) -> None:
        # Called from FL.vfb.reader
        self._kerning_flags = data

    def fake_serialize_kerning_class_flags(self) -> dict[str, tuple[int, int]]:
        # Called from FL.vfb.writer, this even includes entries that have been deleted
        # from the font.
        return self._kerning_flags

    def fake_deserialize_metrics_class_flags(
        self, data: dict[str, tuple[int, int, int]]
    ) -> None:
        # Deserialize a class without minding the flags.
        # Called from FL.vfb.reader
        self._metrics_flags = data

    def fake_serialize_metrics_class_flags(self) -> dict[str, tuple[int, int, int]]:
        # Called from FL.vfb.writer, this even includes entries that have been deleted
        # from the font.
        return self._metrics_flags

    def fake_set_classes(self, classes: list[str]) -> None:
        # Called from Font.classes = [...]
        self.data = classes

    # Operations

    def __add__(self, item: Iterable[str]) -> ClassList:
        result = ClassList(self.data)
        result._kerning_flags = copy(self._kerning_flags)
        result._metrics_flags = copy(self._metrics_flags)
        result += item
        return result

    def __iadd__(self, item: Iterable[str]) -> ClassList:
        self.data.__iadd__(item)
        return self

    def __setitem__(self, index: SupportsIndex | int | Any, item: Any) -> None:
        # Does nothing
        pass

    def append(self, item: str) -> None:
        self.data.append(item)

    def extend(self, other: Iterable[str]) -> None:
        self.data.extend(other)

    def insert(self, i: int, item: str) -> None:
        # Does nothing
        pass

    # Methods called by the Font

    def GetClassLeft(self, class_index: int) -> int | None:
        if class_index >= len(self.data) or class_index < 0:
            return None

        contents = self.data[class_index]
        name = self._get_class_name(contents)
        if name in self._kerning_flags:
            flags = self._kerning_flags[name][0]
            return int(bool(flags & 2**10))
        return 0

    def GetClassRight(self, class_index: int) -> int | None:
        if class_index >= len(self.data) or class_index < 0:
            return None

        contents = self.data[class_index]
        name = self._get_class_name(contents)
        if name in self._kerning_flags:
            flags = self._kerning_flags[name][0]
            return int(bool(flags & 2**11))
        return 0

    def GetClassMetricsFlags(self, class_index: int) -> tuple[int, int, int] | None:
        if class_index >= len(self.data) or class_index < 0:
            return None

        contents = self.data[class_index]
        name = self._get_class_name(contents)
        if name in self._metrics_flags:
            flags = self._metrics_flags[name][1]
            return (
                int(bool(flags & 2**10)),  # L
                int(bool(flags & 2**11)),  # R
                int(bool(flags & 2**12)),  # W
            )
        return (0, 0, 0)

    def SetClassFlags(
        self,
        class_index: int,
        left_lsb: bool | int,
        right_rsb: bool | int,
        width: bool | int | None = None,
    ) -> None:
        if class_index >= len(self.data) or class_index < 0:
            return None

        contents = self.data[class_index]
        name = self._get_class_name(contents)

        value = 0

        if left_lsb:
            value += 2**10
        if right_rsb:
            value += 2**11
        if width:
            value += 2**12

        if name in self._metrics_flags:
            self._metrics_flags[name] = (0, value + 1, 0)
        if name in self._kerning_flags:
            self._kerning_flags[name] = (value, 0)
