import unittest

from FL.objects.Node import Node, nCURVE, nLINE
from FL.objects.Point import Point


class NodeTests(unittest.TestCase):
    def test_instantiation(self) -> None:
        n = Node()
        assert n.parent is None
        assert n.type == nLINE
        assert n.x == 0
        assert n.y == 0
        # assert n.point.parent == n

    def test_instantiation_curve(self) -> None:
        n = Node(nCURVE, Point(1, 2))
        assert n.parent is None
        assert n.type == nCURVE
        assert n.x == 1
        assert n.y == 2
        assert len(n.points) == 3
        # assert n.point.parent == n

    def test_instantiation_float_point(self) -> None:
        p = Point(1.8, 1.2)
        n = Node(nLINE, p)
        assert n.type == 1
        assert n.x == 1
        assert n.y == 1
        assert n.point.x == 1.0

    def test_fake_add_axis(self) -> None:
        n = Node()
        assert n._masters_count == 1
        n.fake_add_axis()
        assert n._points == [[Point()], [Point()]]
        assert n._masters_count == 2

    def test_fake_remove_axis(self) -> None:
        n = Node()
        assert n._masters_count == 1
        n.fake_add_axis()
        assert n._points == [[Point()], [Point()]]
        assert n._masters_count == 2
        n.fake_remove_axis(0.5)
        assert n._points == [[Point()]]
        assert n._masters_count == 1
