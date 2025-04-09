from __future__ import annotations

from collections import UserList
from copy import copy
from typing import Any, Iterable, TypeVar

T = TypeVar("T")


class ListParent(UserList[T]):
    """
    Like a list, but set the _parent attribute for each item.
    """

    def __init__(self, iterable: Iterable[T] = [], parent: Any | None = None) -> None:
        super().__init__(copy(iterable))
        self._parent = parent

    def __add__(self, item: Any) -> ListParent:
        # Makes scripting unresponsive in FL5
        # We raise an error that is not used otherwise
        raise ReferenceError

    def __iadd__(self, item: Any) -> ListParent:
        # Makes scripting unresponsive in FL5
        # We raise an error that is not used otherwise
        raise ReferenceError

    # def __radd__(self, item: Any) -> None:
    #     item._parent = self._parent
    #     self.data.__radd__(item)

    def __setitem__(self, index: int, item: Any) -> None:
        item._parent = self._parent
        self.data[index] = item

    def append(self, item: Any) -> None:
        item._parent = self._parent
        self.data.append(item)

    def clear(self) -> None:
        # Not implemented, probably a mix-up with clean()?
        # Raise AttributeError as in FL5
        raise AttributeError

    def extend(self, iterable: Iterable) -> None:
        # Not implemented
        # Raise AttributeError as in FL5
        raise AttributeError

    def insert(self, index: int, item: Any) -> None:
        item._parent = self._parent
        self.data.insert(index, item)

    # FontLab-specific

    def clean(self) -> None:
        """
        Remove all items from the list.
        """
        self.data = []
