from __future__ import annotations

from typing import TYPE_CHECKING, Any

from FL.fake.Base import Copyable
from FL.objects.Point import Point

if TYPE_CHECKING:
    from FL.objects.Glyph import Glyph
    from FL.objects.Matrix import Matrix

# Node type
nLINE = 1
nMOVE = 17
nCURVE = 35
nOFF = 65

# Alignment
nSHARP = 0
nSMOOTH = 4096  # tangent
nCLOSEPATH = 8192  # ? Undocumented: Closepath follows after node
nFIXED = 12288  # curve to curve smooth

vfb2json_node_types = {"line": 1, "move": 17, "curve": 35, "qcurve": 65}
json2vfb_node_types = {nLINE: "line", nMOVE: "move", nCURVE: "curve", nOFF: "qcurve"}

vfb2json_node_conns = {0: nSHARP, 1: nSMOOTH, 2: nCLOSEPATH, 3: nFIXED}
json2vfb_node_conns = {nSHARP: 0, nSMOOTH: 1, nCLOSEPATH: 2, nFIXED: 3}


__doc__ = "Class to represent a node"


class Node(Copyable):
    __slots__ = [
        "alignment",
        "selected",
        "type",
        "_masters_count",
        "_parent",
        "_points",
    ]

    # Constructor

    def __init__(
        self, node_or_type: Node | int | None = None, p: Point | None = None
    ) -> None:
        """
        Node()
            generic constructor, creates an empty node
        Node(Node)
            copy constructor
        Node(integer type, Point p)
            creates a Node and assigns type and coordinates of the final point

        Args:
            node_or_type (Node | int | None, optional): _description_. Defaults to None.
            p (Point | None, optional): _description_. Defaults to None.
        """
        # Remove float when setting coords
        self._set_defaults()

        # Process params

        if isinstance(node_or_type, Node):
            assert p is None
            self._copy_constructor(node_or_type)
        elif isinstance(node_or_type, int):
            assert isinstance(p, Point)

            self.type = node_or_type
            p = Point(int(p.x), int(p.y))
            p._parent = self
            self._points = [[p] for _ in range(self._masters_count)]
        # else: Empty node

    def __repr__(self) -> str:
        return f"<Node: type=0x{self.type:x}, x={self.x:g}, y={self.y:g}>"

    # Additions for FakeLab

    def fake_deserialize(self, num_masters: int, data: dict[str, Any]) -> None:
        self._masters_count = num_masters
        self.type = vfb2json_node_types[data["type"]]
        self.alignment = vfb2json_node_conns[data["flags"]]
        self._points = [[] for _ in range(self._masters_count)]
        points = data.get("points", [])
        for master_index in range(num_masters):
            master_points = points[master_index]
            if self.type in (nMOVE, nLINE, nOFF):
                assert len(master_points) == 1
            elif self.type == nCURVE:
                assert len(master_points) == 3
            else:
                raise ValueError(f"Unknown Node type: {self.type}")
            for x, y in master_points:
                self._points[master_index].append(Point(x, y))
        if self.type in (nMOVE, nLINE, nOFF):
            assert len(self.points) == 1
        elif self.type == nCURVE:
            assert len(self.points) == 3
        else:
            raise ValueError(f"Unknown Node type: {self.type}")

    def fake_serialize(self, num_masters: int) -> dict[str, Any]:
        d = {
            "type": json2vfb_node_types[self.type],
            "flags": json2vfb_node_conns[self.alignment],
            "points": [],
        }
        points: list[list[tuple[int, int]]] = [[] for _ in range(num_masters)]
        for master_index, master_points in enumerate(self._points):
            for p in master_points:
                points[master_index].append((int(p.x), int(p.y)))
        d["points"] = points
        return d

    def fake_update(self, glyph: Glyph | None = None) -> None:
        """
        Is called from FontLab.UpdateFont()
        """
        self._parent: Glyph | None = glyph
        for p in self.points:
            p.fake_update(self)

    # Attributes

    @property
    def parent(self) -> Glyph | None:
        """
        Nodes's parent object, Glyph
        """
        return self._parent

    @property
    def count(self) -> int:
        return len(self)

    @property
    def point(self) -> Point:
        """
        position of the final point of the first master
        """
        return self._points[0][-1]

    @property
    def points(self) -> list[Point]:
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

    # Operations

    def __len__(self) -> int:
        """
        Return the number of points.
        """
        return len(self._points[0])

    def __getitem__(self, index: int) -> Point:
        """
        Accesses points array of the first master
        """
        return self._points[0][index]

    def __mul__(self, matrix: Matrix) -> Node:
        raise NotImplementedError

    # Methods

    def Assign(
        self, node_or_type: Node | int | None = None, p: Point | None = None
    ) -> None:
        """
        Assigns new values to a Node, refer to constructor for a description of
        possible options
        """
        raise NotImplementedError

    def SetAllLayers(self, pointindex: int, p: Point) -> None:
        """
        Assigns position of the point p to all masters of the point number
        'pointindex'
        """
        raise NotImplementedError

    def Layer(self, masterindex: int) -> list[Point]:
        """
        Returns list of points for the master 'masterindex'
        """
        return self._points[masterindex]

    def Section(self, pointindex: int) -> list[Point]:
        """
        Returns list of points for all layers and point number 'pointindex'
        """
        raise NotImplementedError

    def Shift(self, p: Point, masterindex: int = 0) -> None:
        """
        shifts position of all points for the master 'masterindex'
        """
        raise NotImplementedError

    def ExpandLayer(self, masterindex: int) -> None:
        """
        copies positions of all points in the master 'masterindex' to other masters
        """
        raise NotImplementedError

    def Transform(self, m: Matrix) -> None:
        """
        Applies Matrix transformation to the Node
        """
        raise NotImplementedError

    # Defaults

    def _set_defaults(self) -> None:
        self._parent = None
        self._masters_count = 1

        # type of the node, values are: nMOVE, nLINE, nCURVE or nOFF
        self.type = nLINE

        # type of primitive connection, possible values are:
        # nSHARP, nSMOOTH, nFIXED
        self.alignment = nSHARP

        # True if node is selected
        self.selected = 0
        self._points = [[Point()] for _ in range(self._masters_count)]
