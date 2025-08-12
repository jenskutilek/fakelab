from __future__ import annotations

from FL.fake.Base import Copyable


class TTVdmx(Copyable):
    """
    A vdmx table record.

    This class is completely undocumented.
    """

    __slots__ = ["_y_pel_height", "_y_min", "_y_max"]

    def __init__(self, ttvdmx: TTVdmx | None = None) -> None:
        self._y_pel_height = 0
        self._y_min = 0
        self._y_max = 0
        if isinstance(ttvdmx, TTVdmx):
            self._copy_constructor(ttvdmx)

    def __repr__(self) -> str:
        return (
            f"<TTVdmx: PelHeight: {self.y_pel_height}, Min: {self.y_min}, Max: "
            f"{self.y_max}, Orphan>"
        )

    # Additions for FakeLab

    def fake_deserialize(self, data: dict[str, int]) -> None:
        self.y_pel_height = data["pelHeight"]
        self.y_max = data["max"]
        self.y_min = data["min"]

    def fake_serialize(self) -> dict[str, int]:
        return {"pelHeight": self.y_pel_height, "max": self.y_max, "min": self.y_min}

    # Attributes

    @property
    def y_pel_height(self) -> int:
        return self._y_pel_height

    @y_pel_height.setter
    def y_pel_height(self, value: int) -> None:
        self._y_pel_height = value

    @property
    def y_min(self) -> int:
        return self._y_min

    @y_min.setter
    def y_min(self, value: int) -> None:
        self._y_min = value

    @property
    def y_max(self) -> int:
        return self._y_max

    @y_max.setter
    def y_max(self, value: int) -> None:
        self._y_max = value
