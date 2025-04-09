from __future__ import annotations

from typing import TYPE_CHECKING

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
nSMOOTH = 4096
nFIXED = 12288

vfb2json_node_types = {"line": 1, "move": 17, "curve": 35, "qcurve": 65}
vfb2json_node_conns = {0: nSHARP, 1: nFIXED, 3: nSMOOTH}  # ?


class Node(Copyable):
    """
    Node() - generic constructor, creates an empty node
    Node(Node) - copy constructor
    Node(integer type, Point p) - creates a Node and assigns type and
    coordinates of the final point
    """

    __slots__ = ["_parent", "_points", "type", "alignment", "selected"]

    # Constructor

    def __init__(
        self, node_or_type: Node | int | None = None, p: Point | None = None
    ) -> None:
        """
        # No args
        >>> n = Node()
        >>> print(n)
        <Node: type=0x1, x=0, y=0>
        >>> print(n.x)
        0.0
        >>> print(n.y)
        0.0

        # Node with float point
        >>> p = Point(1.8, 1.2)
        >>> n = Node(nLINE, p)
        >>> print(n)
        <Node: type=0x1, x=1, y=1>

        # The original point's float is truncated
        >>> print(n.point.x)
        1.0
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
            self._points = [p]
        # else: Empty node

    def __repr__(self) -> str:
        return "<Node: type=0x%x, x=%g, y=%g>" % (self.type, self.x, self.y)

    # Additions for FakeLab

    def fake_deserialize(self, data) -> None:
        x, y = data["points"][0]
        n = Node(vfb2json_node_types[data["type"]])
        n.alignment = vfb2json_node_conns[data["flags"]]
        # if n.type in ()

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
        return len(self._points)

    @property
    def point(self) -> Point:
        """
        position of the final point of the first master
        """
        return self._points[-1]

    @property
    def points(self) -> list[Point]:
        """
        positions of all points of the first master
        """
        return self._points

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
        return len(self._points)

    def __getitem__(self, index: int) -> Point:
        """
        Accesses points array of the first master
        """
        return self._points[index]

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
        raise NotImplementedError

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

        # type of the node, values are: nMOVE, nLINE, nCURVE or nOFF
        self.type = nLINE

        # type of primitive connection, possible values are:
        # nSHARP, nSMOOTH, nFIXED
        self.alignment = nSHARP

        # True if node is selected
        self.selected = 0
        self._points = [Point()]
