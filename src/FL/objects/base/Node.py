from typing import TYPE_CHECKING

from FL.constants import nLINE, nSHARP
from FL.helpers.ListParent import ListParent
from FL.objects.Point import Point

if TYPE_CHECKING:
    from FL.objects.Glyph import Glyph
    from FL.objects.Matrix import Matrix
    from FL.objects.Node import Node


class BaseNode:
    __slots__ = [
        "alignment",
        "selected",
        "type",
        "_masters_count",
        "_parent",
        "_points",
    ]

    def __getitem__(self, index: int) -> "Point":
        """
        Accesses points array of the first master
        """
        return self._points[0][index]

    def __init__(self) -> None:
        self._parent = None
        self._masters_count = 1

        # type of the node, values are: nMOVE, nLINE, nCURVE or nOFF
        self.type = nLINE

        # type of primitive connection, possible values are:
        # nSHARP, nSMOOTH, nFIXED
        self.alignment = nSHARP

        # 1 if node is selected
        self.selected = 0
        self._points: "list[ListParent[Point]]" = [
            ListParent() for _ in range(self._masters_count)
        ]
        for master_index in range(self._masters_count):
            self._points[master_index].append(Point())

    def __len__(self) -> int:
        """
        Return the number of points.
        """
        return len(self._points[0])

    def __mul__(self, matrix: "Matrix") -> "Node":
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"<Node: type=0x{self.type:x}, x={self.x:g}, y={self.y:g}>"

    @property
    def parent(self) -> "Glyph | None":
        """
        Nodes's parent object, Glyph
        """
        return self._parent

    @property
    def count(self) -> int:
        return len(self)

    @property
    def point(self) -> "Point":
        """
        position of the final point of the first master
        """
        return self._points[0][0]

    @property
    def points(self) -> "ListParent[Point]":
        """
        positions of all points of the first master
        """
        return self._points[0]

    @property
    def x(self) -> int:
        return int(self.point.x)

    @property
    def y(self) -> int:
        return int(self.point.y)
