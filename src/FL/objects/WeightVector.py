from __future__ import annotations

from typing import TYPE_CHECKING

from FL.fake.Base import Copyable

if TYPE_CHECKING:
    from FL.objects.Font import Font


__doc__ = "Class to represent a weight vector"


class WeightVector(Copyable):
    """This class is completely undocumented.

    Apparently: A list of 16 floats that represent the interpolation factors for all
    possible masters.
    """

    __slots__ = ["_parent", "_weights"]

    # Constructor

    def __init__(self, weight_vector: WeightVector | None = None) -> None:
        self._parent: Font | None = None
        self._weights = [
            1.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ]
        if weight_vector is not None:
            self._copy_constructor(weight_vector)

    # Attributes

    @property
    def parent(self) -> Font | None:
        return self._parent

    def __getitem__(self, index: int) -> float:
        return self._weights[index]
