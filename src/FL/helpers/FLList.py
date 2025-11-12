from __future__ import annotations

from typing import Any, Iterable

from FL.objects.Point import Point


def adjust_list(seq: list[Any], new_length: int, value: Any = None) -> None:
    """
    Adjust the length of a list in place.

    Args:
        seq (list[Any]): The list to be adjusted
        new_length (int): The desired length
        value (Any): The default value for added list elements. If value is Point, the
            point will be instantiated with coordinates 0, 0.
    """
    old_length = len(seq)
    diff = new_length - old_length
    if diff == 0:
        return

    if diff > 0:
        # Add elements
        if value is None:
            if seq:
                value = seq[0]
            seq.extend([value] * diff)
        elif value is Point:
            for _ in range(diff):
                seq.append(Point())
        else:
            seq.extend([value] * diff)
    else:
        # Take away elements
        for _ in range(abs(diff)):
            seq.pop()


class FLList(list[Any]):
    def __init__(self, iterable: Iterable[Any] | None = None) -> None:
        if iterable is None:
            iterable = []
        super().__init__(iterable)

    # FontLab-specific

    def clean(self) -> None:
        super().clear()
