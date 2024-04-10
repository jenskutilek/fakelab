from __future__ import annotations

from FL.objects.Point import Point

# Node type
nLINE = 1
nMOVE = 17
nCURVE = 35
nOFF = 65

# Alignment
nSHARP = 0
nSMOOTH = 4096
nFIXED = 12288


class Node:
    """
    Node() - generic constructor, creates an empty node
    Node(Node) - copy constructor
    Node(integer type, Point p) - creates a Node and assigns type and
    coordinates of the final point
    """

    def __init__(self, node_or_type=None, p=None):
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
        self.set_defaults()

        # Process params

        if isinstance(node_or_type, Node):
            if p is None:
                # Copy constructor
                raise NotImplementedError
        elif isinstance(node_or_type, int):
            assert isinstance(p, Point)

            self.type = node_or_type
            p = Point(int(p.x), int(p.y))
            p._parent = self
            self._points = [p]
        # else: Empty node

    def __repr__(self):
        return "<Node: type=0x%x, x=%g, y=%g>" % (self.type, self.x, self.y)

    # Additions for FakeLab

    def fake_update(self, glyph=None):
        """
        Is called from FontLab.UpdateFont()
        """
        self._parent = glyph
        for p in self.points:
            p.fake_update(self)

    # Attributes

    @property
    def parent(self):
        """
        Nodes's parent object, Glyph
        """
        return self._parent

    @property
    def count(self):
        return len(self._points)

    @property
    def point(self):
        """
        position of the final point of the first master
        """
        return self._points[-1]

    @property
    def points(self):
        """
        positions of all points of the first master
        """
        return self._points

    @property
    def x(self):
        return self.point.x

    @property
    def y(self):
        return self.point.y

    # Operations

    def __len__(self):
        """
        Return the number of points.
        """
        return len(self._points)

    def __getitem__(self, index):
        """
        Accesses points array of the first master
        """
        return self._points[index]

    def __mul__(self, matrix):
        raise NotImplementedError

    # Methods

    def Assign(self, n):
        """
        (Node)

        assigns new values to a Node, refer to constructor for a description of
        possible options
        """
        raise NotImplementedError

    def SetAllLayers(self, pointindex, p):
        """
        assigns position of the point p to all masters of the point number
        'pointindex'
        """
        raise NotImplementedError

    def Layer(self, masterindex):
        """
        returns list of points for the master 'masterindex'
        """
        raise NotImplementedError

    def Section(self, pointindex):
        """
        returns list of points for all layers and point number 'pointindex'
        """
        raise NotImplementedError

    def Shift(self, p, masterindex=0):
        """
        shifts position of all points for the master 'masterindex'
        """
        raise NotImplementedError

    def ExpandLayer(self, masterindex):
        """
        copies positions of all points in the master 'masterindex' to other masters
        """
        raise NotImplementedError

    def Transform(self, m):
        """
        (Matrix m)

        applies Matrix transformation to the Node
        """
        raise NotImplementedError

    # Defaults

    def set_defaults(self):
        self._parent = None

        # type of the node, values are: nMOVE, nLINE, nCURVE or nOFF
        self.type = nLINE

        # type of primitive connection, possible values are:
        # nSHARP, nSMOOTH, nFIXED
        self.alignment = nSHARP

        # True if node is selected
        self.selected = 0
        self._points = [Point()]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
