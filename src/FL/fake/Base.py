from __future__ import annotations

from typing import Any


class Copyable:
    __slots__: list[str] = ["_parent"]

    def _copy_constructor(self, other: Any) -> None:
        from copy import deepcopy

        assert isinstance(other, type(self))

        tmp = deepcopy(other)
        for attr in self.__slots__:
            if attr == "_parent":
                # Parent is not copied
                self._parent: Any | None = None
            else:
                setattr(self, attr, getattr(tmp, attr))
