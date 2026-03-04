from __future__ import annotations

from typing import TYPE_CHECKING

from FL.constants import nCURVE
from FL.fake.copy import copy_fl_object
from FL.fake.Node import FakeNode
from FL.helpers.ListParent import ListParent
from FL.objects.Point import Point

if TYPE_CHECKING:
    from FL.objects.Matrix import Matrix


__doc__ = "Class to represent a node"


class Node(FakeNode):
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
        super(FakeNode, self).__init__()
        if isinstance(node_or_type, Node):
            assert p is None
            copy_fl_object(node_or_type, self)
        elif isinstance(node_or_type, int):
            assert isinstance(p, Point)

            self.type = node_or_type
            p = Point(int(p.x), int(p.y))
            p._parent = self
            if self.type == nCURVE:
                self._points = [
                    ListParent([Point(p), Point(), Point()])
                    for _ in range(self._masters_count)
                ]
            else:
                self._points = [
                    ListParent([Point(p)]) for _ in range(self._masters_count)
                ]

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

    def Layer(self, masterindex: int) -> ListParent[Point]:
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

    def Transform(self, m: "Matrix") -> None:
        """
        Applies Matrix transformation to the Node
        """
        raise NotImplementedError
