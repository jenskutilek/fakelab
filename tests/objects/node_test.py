import unittest


from FL.objects.Node import Node, nLINE
from FL.objects.Point import Point


class NodeTests(unittest.TestCase):
    def test_instantiation(self) -> None:
        n = Node()
        assert n.parent is None
        assert n.type == nLINE
        assert n.x == 0
        assert n.y == 0

    def test_instantiation_float_point(self) -> None:
        p = Point(1.8, 1.2)
        n = Node(nLINE, p)
        assert n.type == 1
        assert n.x == 1
        assert n.y == 1
        assert n.point.x == 1.0
