from collections import UserList
from copy import copy
from typing import Any, Iterable, SupportsIndex, TypeVar

T = TypeVar("T")


class ListParent(UserList[T]):
    """
    Like a list, but set the _parent attribute for each item.
    """

    def __init__(
        self,
        iterable: Iterable[T] = [],
        parent: Any | None = None,
        only_type: Any = None,
    ) -> None:
        super().__init__(copy(iterable))
        self._parent = parent
        self._type = only_type
        for item in self.data:
            self._item_callback(item)

    def _item_callback(self, item: Any) -> None:
        if hasattr(item, "_parent"):
            item._parent = self._parent

    def __add__(self, item: Any) -> "ListParent[T]":
        # Makes scripting unresponsive in FL5
        # We raise an error that is not used otherwise
        raise ReferenceError

    def __iadd__(self, item: Any) -> "ListParent[T]":
        # Makes scripting unresponsive in FL5
        # We raise an error that is not used otherwise
        raise ReferenceError

    # def __radd__(self, item: Any) -> None:
    #     item._parent = self._parent
    #     self.data.__radd__(item)

    def __setitem__(
        self, index: "SupportsIndex | slice[Any, Any, Any]", item: Any
    ) -> None:
        if not isinstance(item, self._type):
            raise RuntimeError("Element being assigned has inappropriate type")

        self.data[index] = item
        self._item_callback(item)

    def append(self, item: Any) -> None:
        if not isinstance(item, self._type):
            raise RuntimeError("Element being assigned has inappropriate type")

        self.data.append(item)
        self._item_callback(item)

    def clear(self) -> None:
        # Not implemented, probably a mix-up with clean()?
        # Raise AttributeError as in FL5
        raise AttributeError

    def extend(self, other: Iterable[T]) -> None:
        # Not implemented
        # Raise AttributeError as in FL5
        raise AttributeError

    def insert(self, i: int, item: Any) -> None:
        if not isinstance(item, self._type):
            raise RuntimeError("Element being assigned has inappropriate type")

        self.data.insert(i, item)
        self._item_callback(item)

    # FontLab-specific

    def clean(self) -> None:
        """
        Remove all items from the list.
        """
        self.data = []


class DirectionalList(ListParent[T]):
    def __init__(
        self,
        stem_direction: int,
        iterable: Iterable = [],
        parent: Any | None = None,
        only_type: Any = None,
    ) -> None:
        self._stem_direction = stem_direction
        super().__init__(iterable, parent, only_type)

    def _item_callback(self, item: Any) -> None:
        # Set the stem direction from the list to the Hint items
        super()._item_callback(item)
        item._stem_direction = self._stem_direction
