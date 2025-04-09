from __future__ import annotations

from typing import Any


class Copyable:
    __slots__: list[str] = []

    def _copy_constructor(self, other: Any) -> None:
        from copy import deepcopy

        tmp = deepcopy(other)
        for attr in self.__slots__:
            # TODO: Is parent copied?
            setattr(self, attr, getattr(tmp, attr))
