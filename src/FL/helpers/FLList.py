from typing import Iterable


class FLList(list):
    def __init__(self, iterable: Iterable | None = None) -> None:
        if iterable is None:
            iterable = []
        super().__init__(iterable)

    def clean(self) -> None:
        super().clear()
