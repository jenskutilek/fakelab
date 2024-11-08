from __future__ import annotations

from FL.objects.Link import Link
from FL.objects.Matrix import Matrix


class Hint:
    def __init__(
        self, hint_or_position: Hint | int | None, width: int | None = None
    ) -> None:
        self.parent = None
        self.position = 0
        self.width = 21

        if isinstance(hint_or_position, Hint):
            self.position = hint_or_position.position
            self.width = hint_or_position.width

        else:
            self.position = hint_or_position
            self.width = width

    def ToLink(self) -> Link:
        raise NotImplementedError

    def Transform(self, m: Matrix) -> None:
        raise NotImplementedError

    def TransformLayer(self, m: Matrix, layernum: int) -> None:
        raise NotImplementedError
