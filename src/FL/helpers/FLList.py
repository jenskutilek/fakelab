from typing import Any, Iterable


class FLList(list[Any]):
    def __init__(self, iterable: Iterable[Any] | None = None) -> None:
        if iterable is None:
            iterable = []
        super().__init__(iterable)

    # FontLab-specific

    def clean(self) -> None:
        super().clear()
