from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from FL.fake.Base import Copyable
from FL.helpers.ListParent import ListParent
from FL.objects.Image import Image
from FL.objects.KerningPair import KerningPair
from FL.objects.Node import Node
from FL.objects.Point import Point
from FL.objects.Rect import Rect

if TYPE_CHECKING:
    from collections.abc import Iterable

    from FL.objects.Anchor import Anchor
    from FL.objects.AuditRecord import AuditRecord
    from FL.objects.Component import Component
    from FL.objects.Font import Font
    from FL.objects.Guide import Guide
    from FL.objects.Hint import Hint
    from FL.objects.Link import Link
    from FL.objects.Matrix import Matrix
    from FL.objects.Replace import Replace
    from FL.objects.TTPoint import TTPoint


logger = logging.getLogger(__name__)


class Glyph(Copyable):
    """
    A glyph
    """

    __slots__ = [
        "_anchors",
        "_components",
        "_height",
        "_hguides",
        "_hhints",
        "_hlinks",
        "_index",
        "_kerning",
        "_layers_number",
        "_mask",
        "_nodes",
        "_replace_table",
        "_vguides",
        "_vhints",
        "_vlinks",
        "_width",
        "advance_height",
        "advance_width",
        "customdata",
        "end_points",
        "flags",
        "hdmx",
        "image",
        "instructions",
        "left_side_bearing",
        "mark",
        "note",
        "number_of_contours",
        "points",
        "top_side_bearing",
        "unicodes",
        "y_pels",
        # Non-API
        "_glyph_hinting_options",
        "_glyph_origin",
        "_metrics",
        "_parent",
        "name",
    ]

    # Constructor

    def __init__(
        self, glyph_or_masterscount: Glyph | int = 1, nodes: list[Node] | None = None
    ) -> None:
        self.set_defaults()

        # Process params

        if isinstance(glyph_or_masterscount, Glyph):
            self._copy_constructor(glyph_or_masterscount)

        elif isinstance(glyph_or_masterscount, int):
            self._layers_number: int = glyph_or_masterscount
            if nodes is not None:
                # Assign nodes
                for node in nodes:
                    self.nodes.append(node)
        # else: Empty Glyph

    def __repr__(self) -> str:
        return "<Glyph: '%s', %i nodes, orphan>" % (self.name, len(self))

    # Additions for FakeLab

    def fake_update(self, font: Font | None = None, index: int = -1) -> None:
        """
        Is called from FontLab.UpdateFont()
        """
        self._parent: Font | None = font
        self._index: int = index
        if font is None:
            self._index = -1
        for n in self.nodes:
            n.fake_update(self)

    def fake_deserialize(self, name: str, data: Any) -> None:
        """
        Add data from a VFB entry

        Args:
            name (str): The name of the entry.
            data (_type_): The entry data.
        """
        if name == "Glyph":
            self.name: str = data["name"]
            self._layers_number = data["num_masters"]
            for node_data in data["nodes"]:
                node = Node()
                node.fake_deserialize(self._layers_number, node_data)
                self.nodes.append(node)
            self._metrics = [Point(x, y) for x, y in data["metrics"]]
            for index, values in data.get("kerning", {}).items():
                pair = KerningPair(int(index))
                pair._values = values
                self.kerning.append(pair)
            for component_data in data.get("components", []):
                component = Component()
                component.fake_deserialize(self._layers_number, component_data)
                self.components.append(component)

        elif name == "Links":
            for axis, target in (("x", self.vlinks), ("y", self.hlinks)):
                axis_links = data.get(axis, [])
                for axis_link in axis_links:
                    target.append(Link(*axis_link))

        elif name == "image":
            pass
        elif name == "Glyph Bitmaps":
            pass
        elif name == "2023":
            pass
        elif name == "Glyph Sketch":
            pass
        elif name == "Glyph Hinting Options":
            self._glyph_hinting_options = data
        elif name == "mask":
            pass
        elif name == "mask.metrics":
            pass
        elif name == "mask.metrics_mm":
            pass
        elif name == "Glyph Origin":
            self._glyph_origin = data
        elif name == "unicodes":
            self.unicodes.extend(data)
        elif name == "Glyph Unicode Non-BMP":
            self.unicodes.extend(data)
        elif name == "mark":
            self.mark: int = data
        elif name == "glyph.customdata":
            self.customdata: str | None = data
        elif name == "glyph.note":
            self.note: str | None = data
        elif name == "Glyph GDEF Data":
            pass
        elif name == "Glyph Anchors Supplemental":
            pass
        elif name == "Glyph Anchors MM":
            pass
        elif name == "Glyph Guide Properties":
            pass
        else:
            logger.warning(f"Unhandled glyph entry: {name}")

    def fake_serialize(self) -> dict[str, Any]:
        """
        Serialize the glyph to a dict which resembles the low-level VFB structure

        Returns:
            dict[str, Any]: The serialized glyph.
        """
        # TODO: Which entries are required? Leave out the other ones.
        s: dict[str, Any] = {
            "Glyph": {
                # Minimum wage, yeah!
                "name": self.name,
                "num_masters": self.layers_number,
                "nodes": [
                    node.fake_serialize(self.layers_number) for node in self.nodes
                ],
                "metrics": [
                    [int(p.x), int(p.y)]
                    for p in [self.GetMetrics(i) for i in range(self.layers_number)]
                ],
                "components": [comp.fake_serialize() for comp in self.components],
            },
            "Links": {
                "x": [[link.node1, link.node2] for link in self.vlinks],
                "y": [[link.node1, link.node2] for link in self.hlinks],
            },
            # "image"
            # "Glyph Bitmaps"
            # "2023"
            # "Glyph Sketch"
            "Glyph Hinting Options": self._glyph_hinting_options,
            # "mask"
            # "mask.metrics"
            # "mask.metrics_mm"
            "Glyph Origin": self._glyph_origin,
            "unicodes": [u for u in self.unicodes if u <= 0xFFFF],
            "Glyph Unicode Non-BMP": [u for u in self.unicodes if u > 0xFFFF],
            "mark": self.mark,
        }
        if self.kerning:
            s["Glyph"]["kerning"] = {
                str(pair.key): pair.values for pair in self.kerning
            }
        if self.customdata:
            s["glyph.customdata"] = self.customdata
        if self.note:
            s["glyph.note"] = self.note
        return s

    # Attributes

    @property
    def parent(self) -> Font | None:
        """
        The glyph's parent object.

        Returns:
            Font | None: The parent :py:class:`Font` or None.
        """
        return self._parent

    @property
    def nodes(self) -> ListParent[Node]:
        """
        The list of the glyph's nodes.

        Returns:
            ListParent[Node]: The nodes.
        """
        return self._nodes

    # customdata
    # note
    # mark

    @property
    def anchors(self) -> list[Anchor]:
        """
        The list of the glyph's anchos.

        Returns:
            list[Anchor]: The anchors.
        """
        return self._anchors

    @property
    def hhints(self) -> ListParent[Hint]:
        """
        The list of the glyph's horizontal stem hints.

        Returns:
            ListParent[Hint]: The list of hints.
        """
        return self._hhints

    @property
    def vhints(self) -> ListParent[Hint]:
        """
        The list of the glyph's vertical stem hints.

        Returns:
            ListParent[Hint]: The list of hints.
        """
        return self._vhints

    @property
    def hlinks(self) -> ListParent[Link]:
        """
        The list of the glyph's horizontal stem links.

        Returns:
            ListParent[Link]: The list of links.
        """
        return self._hlinks

    @property
    def vlinks(self) -> ListParent[Link]:
        """
        The list of the glyph's vertical stem links.

        Returns:
            ListParent[Link]: The list of links.
        """
        return self._vlinks

    @property
    def hguides(self) -> ListParent[Guide]:
        """
        The list of the glyph's horizontal guides.

        Returns:
            ListParent[Guide]: The list of guides.
        """
        return self._hguides

    @property
    def vguides(self) -> ListParent[Guide]:
        """
        The list of the glyph's vertical guides.

        Returns:
            ListParent[Guide]: The list of guides.
        """
        return self._vguides

    @property
    def components(self) -> ListParent[Component]:
        """
        The list of the glyph's components.

        Returns:
            ListParent[Component]: The list of components.
        """
        return self._components

    @property
    def replace_table(self) -> list[Replace]:
        """
        The hint replacement program, a list of :py:class:`Replace` objects.

        Returns:
            list[Replace]: The list of replace objects.
        """
        return self._replace_table

    @property
    def kerning(self) -> ListParent[KerningPair]:
        """
        The list of the glyph's kerning pairs.

        Returns:
            ListParent[KerningPair]: The list of kerning pairs.
        """
        return self._kerning

    @property
    def layers_number(self) -> int:
        """
        The number of masters for the glyph.

        Returns:
            int: The number of masters.
        """
        return self._layers_number

    @property
    def mask(self) -> Glyph | None:
        """
        The mask (background layer) of the glyph.

        Returns:
            Glyph | None: The mask glyph if present.
        """
        return self._mask

    # flags

    @property
    def nodes_number(self) -> int:
        """
        The number of nodes in the glyph, same as 'len(Glyph)'.

        Returns:
            int: The number of nodes.
        """
        return len(self._nodes)

    @property
    def width(self) -> int:
        """
        The advance width for the first master.

        Returns:
            int: _description_
        """
        return int(self.GetMetrics().x)

    @width.setter
    def width(self, value: int) -> None:
        # TODO: Does this set the first master only?
        self._width = value

    @property
    def height(self) -> int:
        """
        advance height for the first master

        Returns:
            int: _description_
        """
        return int(self.GetMetrics().y)

    @height.setter
    def height(self, value: int) -> None:
        # TODO: Does this set the first master only?
        self._height = value

    @property
    def unicode(self) -> int | None:
        """
        The first Unicode index as integer.

        Returns:
            int | None: The Unicode codepoint.
        """
        if self.unicodes:
            return self.unicodes[0]
        else:
            return None

    @unicode.setter
    def unicode(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError
        if value == -1:
            return
        if not self.unicodes:
            self.unicodes.append(value)
        else:
            self.unicodes[0] = value

    # unicodes
    # name
    # image

    @property
    def index(self) -> int:
        """
        The glyph index in the font.

        Returns:
            int: The glyph index or -1 if the glyph has no parent font.
        """
        if self.parent is None:
            return -1
        return self._index

    # TrueType Data:

    # advance_width
    # advance_height
    # left_side_bearing
    # top_side_bearing
    # y_pels

    @property
    def bounding_box(self) -> Rect:
        return self.GetBoundingRect(0)

    # number_of_contours
    # end_points
    # points
    # instructions
    # hdmx

    # Operations

    def __len__(self) -> int:
        """
        The number of nodes in the glyph.

        Returns:
            int: The number of nodes
        """
        return len(self._nodes)

    def __getitem__(self, index: int) -> Node:
        """
        Access the nodes list

        Args:
            index (int): The node index.

        Returns:
            Node: The node at index.
        """
        return self._nodes[index]

    def __slice__(self, a: int, b: int) -> list[Node]:
        """
        Access a slice of the glyph's nodes list.

        Args:
            a (int): The first node index.
            b (int): The last node index.

        Returns:
            list[Node]: The slice of nodes.
        """
        raise NotImplementedError

    def __add__(self, glyph_node_nodelist: Glyph | Node | Iterable[Node]) -> Glyph:
        """
        Append a :py:class:`Glyph`, a :py:class:`Node`, or a sequence of
        :py:class:`Node`s.

        Args:
            glyph_node_nodelist (Glyph | Node | Iterable[Node]): The objects to append.

        Returns:
            Glyph: The resulting glyph.
        """
        raise NotImplementedError

    def __mul__(self, matrix: Matrix) -> Glyph:
        """
        Apply a matrix transformation to the glyph.

        Args:
            matrix (Matrix): The transformation to apply.

        Returns:
            Glyph: The transformed glyph.
        """
        raise NotImplementedError

    # Methods

    def Assign(self, g: Glyph) -> None:
        """
        Copy all information from a glyph.

        Args:
            g (Glyph): The source glyph.
        """
        raise NotImplementedError

    def Transform(self, matrix: Matrix) -> None:
        """
        Apply a matrix transformation to the glyph.

        Args:
            matrix (Matrix): The transformation to apply.
        """
        raise NotImplementedError

    def SetLayersNumber(self, mastersnumber: int) -> None:
        """
        Change the number of masters. Only applicable to glyphs that have no parent.

        Args:
            mastersnumber (int): The new number of masters.
        """
        raise NotImplementedError

    def Clear(self) -> None:
        """
        Remove all nodes.
        """
        raise NotImplementedError

    def Add(self, glyph_node_nodelist: Glyph | Node | Iterable[Node]) -> None:
        """
        Append a glyph, a node, or a sequence of nodes.

        Args:
            glyph_node_nodelist (Glyph | Node | Iterable[Node]): The objects to append.
        """
        raise NotImplementedError

    def Insert(
        self, node_or_glyph_or_nodelist: Node | Glyph | list[Node], nodeindex: int = 0
    ) -> None:
        """
        Insert a node, a glyph, or a sequence of nodes at the beginning of the glyph's
        nodes, or at the specified node index.

        Args:
            node_or_glyph_or_nodelist (Node | Glyph | list[Node]): The nodes to insert.
            nodeindex (int, optional): The place to insert. Defaults to 0.
        """
        raise NotImplementedError

    def Present(self, style) -> bool:
        """
        Return True if a layer or a combination of layers are present in the glyph.

        Args:
            style (_type_): _description_

        Returns:
            bool: Whether the specified combination of layers is present.
        """
        raise NotImplementedError

    def Delete(self, index0: int, index1: int | None = None) -> None:
        """
        Remove a node or a range of nodes.

        Args:
            index0 (int): The first node index
            index1 (int | None, optional): The last node index. Defaults to None.
        """
        raise NotImplementedError

    def ExpandLayer(self, masterindex: int) -> None:
        """
        Expand the specified master to all other masters.

        Args:
            masterindex (int): The master index.
        """
        raise NotImplementedError

    def Shift(self, point: Point, masterindex: int = 0) -> None:
        """
        Shift the positions of all nodes in the specified master.

        Args:
            point (Point): The point specifying the x and y shift.
            masterindex (int, optional): The master to shift. Defaults to 0.
        """
        raise NotImplementedError

    def Scale(self, scale: Point, center: Point, masterindex: int = 0) -> None:
        """
        Scale the glyph.

        Args:
            scale (Point): The point specifying the x and y scale factor.
            center (Point): The center of the scale transformation.
            masterindex (int, optional): The master to scale. Defaults to 0.
        """
        raise NotImplementedError

    def Layer(self, masterindex: int) -> list[Point]:
        """
        Return a list of :py:class:`Points` for all nodes for the selected master.

        Args:
            masterindex (int): The master index

        Returns:
            list[Point]: The list of each node's last point.
        """
        raise NotImplementedError

    def Section(self, masterindex: int, pointindex: int, nodetype: int) -> list[Point]:
        """
        Return a list of points matching the specified options.

        Args:
            masterindex (int): The master index.
            pointindex (int): The point index.
            nodetype (int): The node type (nLINE, nMOVE, nCURVE, nOFF).

        Returns:
            list[Point]: The list of points.
        """
        raise NotImplementedError

    def MoveNode(self, options) -> None:
        """
        Moves the node copying Edit tool behavior (see User manual for details).
        """
        raise NotImplementedError

    def DeleteNode(self, nodeindex: int) -> None:
        """
        Remove the specified Node.

        Args:
            nodeindex (int): The node index.
        """
        raise NotImplementedError

    def InsertNode(
        self, nodeindex: int, time: float = 0.0, masterindex: int = 0
    ) -> None:
        """
        Insert a new node on a contour.

        Args:
            nodeindex (int): _description_
            time (float, optional): The time on the segment. Start is 0.0, end is 1.0.
                Defaults to 0.0.
            masterindex (int, optional): The master index used for measuring. Defaults
                to 0.
        """
        raise NotImplementedError

    # SELECTION-METHODS

    def Selection(self) -> list[Node]:
        """
        Return a list of selected nodes.

        Returns:
            list[Node]: The list of nodes.
        """
        raise NotImplementedError

    def SelectAll(self) -> None:
        """
        Select all nodes.
        """
        raise NotImplementedError

    def UnselectAll(self) -> None:
        """
        Deselect all nodes.
        """
        raise NotImplementedError

    def InvertSelection(self) -> None:
        """
        Select unselected nodes and deselect selected nodes.
        """
        raise NotImplementedError

    def isAnySelected(self) -> bool:
        """
        Return True if at least one node is selected.
        """
        raise NotImplementedError

    def SelectedCount(self) -> int:
        """
        Return the number of selected nodes.
        """
        raise NotImplementedError

    def SelectRect(self, r: Rect, masterindex: int = 0) -> None:
        """
        Select all nodes that are inside a rectangle.

        Args:
            r (Rect): The rectangle.
            masterindex (int, optional): The master index used for measuring. Defaults
                to 0.
        """
        raise NotImplementedError

    def UnselectRect(self, r: Rect, masterindex: int = 0) -> None:
        """
        Deselect all nodes that are inside a rectangle.

        Args:
            r (Rect): The rectangle.
            masterindex (int, optional): The master index used for measuring. Defaults
                to 0.
        """
        raise NotImplementedError

    def DeleteSelected(self) -> None:
        """
        Delete all selected nodes.
        """
        raise NotImplementedError

    # METRICS-METHODS

    def GetBoundingRect(self, masterindex: int = 0) -> Rect:
        """
        Return the glyph's bounding box.

        Args:
            masterindex (int, optional): The master index used for measuring. Defaults
                to 0.

        Returns:
            Rect: The bounding box of the glyph.
        """
        if masterindex != 0:
            raise NotImplementedError

        rect = Rect(32767, 32767, -32767, -32767)
        for n in self._nodes:
            for p in n.points:
                rect += p

        return rect

    def GetMetrics(self, masterindex: int = 0) -> Point:
        """
        Return the glyph's advance width and advance height as a point.

        Args:
            masterindex (int, optional): The master index used for measuring. Defaults
                to 0.

        Returns:
            Point: The point containing the advance width (x) and heigh (y).
        """
        return self._metrics[masterindex]

    def SetMetrics(self, p: Point, masterindex: int = 0) -> None:
        """
        Assign new values to the advance width and advance height of the glyph.

        Args:
            p (Point): The point containing the advance width (x) and heigh (y).
            masterindex (int, optional): The master index. Defaults to 0.
        """
        raise NotImplementedError

    def GetVSB(self, masterindex: int = 0) -> int:  # TODO: Is it int?
        """
        Return the glyph' bottom sidebearing position.

        Args:
            masterindex (int, optional): The master index used for measuring. Defaults
                to 0.

        Returns:
            int: The bottom sidebearing.
        """
        raise NotImplementedError

    def SetVSB(self, value: int, masterindex: int = 0) -> None:  # TODO: Is it int?
        """
        Assign new values to the bottom sidebearing of the glyph.

        Args:
            value (int): The bottom sidebearing.
            masterindex (int, optional): The master index. Defaults to 0.
        """
        raise NotImplementedError

    # OVERLAP-METHODS

    def RemoveOverlap(self, masterindex: int = 0) -> None:
        """
        Remove overlaps from the glyph's contours.

        Args:
            masterindex (int, optional): The master index. Defaults to 0.
        """
        raise NotImplementedError

    def Badd(self, glyph_nodelist: Glyph | list[Node], masterindex: int = 0) -> None:
        """
        Perform a boolean _Add_ operation with the glyph or list of nodes.

        Args:
            glyph_nodelist (Glyph | list[Node]): _description_
            masterindex (int, optional): The master index. Defaults to 0.
        """
        raise NotImplementedError

    def Bsubtract(
        self, glyph_nodelist: Glyph | list[Node], masterindex: int = 0
    ) -> None:
        """
        Perform boolean _Subtract_ operation with the glyph or list of nodes.

        Args:
            glyph_nodelist (Glyph | list[Node]): _description_
            masterindex (int, optional): The master index. Defaults to 0.
        """
        raise NotImplementedError

    def Bintersect(
        self, glyph_nodelist: Glyph | list[Node], masterindex: int = 0
    ) -> None:
        """
        Perform a boolean _Intersect_ operation with the glyph or list of nodes.

        Args:
            glyph_nodelist (Glyph | list[Node]): _description_
            masterindex (int, optional): The master index. Defaults to 0.
        """
        raise NotImplementedError

    # CONTOUR-METHODS

    def GetContoursNumber(self) -> int:
        """
        Return the number of contours in the glyph.
        """
        raise NotImplementedError

    def GetContourBegin(self, contourindex: int) -> int:
        """
        Return the index of the first node of the speficied contour.

        Args:
            contourindex (int): The contour index.

        Returns:
            int: The node index.
        """
        raise NotImplementedError

    def GetContourLength(self, contourindex: int) -> int:
        """
        Return the number of nodes in the specified contour.

        Args:
            contourindex (int): The contour index.

        Returns:
            int: The number of nodes.
        """
        raise NotImplementedError

    def SelectContour(self, contourindex: int) -> None:
        """
        Select all nodes in the specified contour.

        Args:
            contourindex (int): The contour index.
        """
        raise NotImplementedError

    def DeleteContour(self, contourindex: int) -> None:
        """
        Remove in the specified contour.

        Args:
            contourindex (int): The contour index.
        """
        raise NotImplementedError

    def ReverseContour(self, contourindex: int) -> None:
        """
        Reverse the specified contour's path direction.

        Args:
            contourindex (int): The contour index.
        """
        raise NotImplementedError

    def ReorderContour(self, contourindex: int, newindex: int) -> None:
        """
        Reorder the contours in the glyph by moving the specified contour to a new
        index.

        Args:
            contourindex (int): The contour index.
            newindex (int): The new contour index.
        """
        raise NotImplementedError

    def isContourClockwise(self, contourindex: int) -> bool:
        """
        Return True if direction of contour is clockwise.

        Args:
            contourindex (int): The contour index.

        Returns:
            bool: True if the path direction is clockwise.
        """
        raise NotImplementedError

    def SetStartNode(self, nodeindex: int) -> None:
        """
        Make the specified node the starting node of its contour.

        Args:
            nodeindex (int): The node index.
        """
        raise NotImplementedError

    def FindContour(self, nodeindex: int) -> int:
        """
        Return number of contour containing the speficied node.

        Args:
            nodeindex (int): The node index

        Returns:
            int: The contour index.
        """
        raise NotImplementedError

    # HINTS-METHODS

    def RemoveHints(self, mode: int) -> None:
        """
        Remove hints and links.

        Args:
            mode (int): _description_
        """
        raise NotImplementedError

    def Autohint(self, masterindex: int = 0) -> None:
        """
        Automatically generate PostScript hints for the glyph.

        Args:
            masterindex (int, optional): The master index. Defaults to 0.
        """
        raise NotImplementedError

    # ANCHOR-METHODS

    def FindAnchor(self, name: str) -> Anchor:  # XXX: does it return an anchor?
        """
        Find an anchor by name.

        Args:
            name (str): The anchor name

        Returns:
            Anchor: _description_
        """
        raise NotImplementedError

    # TRANSFORMATION-METHODS

    def Decompose(self) -> None:
        """
        Paste all components to the glyph outline.
        """
        raise NotImplementedError

    def MakeExtremeNodes(self, masterindex: int = 0) -> None:
        """
        Automatically add nodes at contour extrema.

        Args:
            masterindex (int, optional): The master index. Defaults to 0.
        """
        raise NotImplementedError

    def Audit(self) -> list[AuditRecord]:
        """
        Perform a test of the glyph and return a list of :py:class:`AuditRecord`
        objects.

        Returns:
            list[AuditRecord]: The list of potential contour problems.
        """
        raise NotImplementedError

    def Iterate(self, iterator: Any) -> None:
        """
        Iterate the glyph through an iterator class which must provide the following
        methods:

        - :py:func:`Start()`
        - :py:func:`ClosePath()`
        - :py:func:`StartPath(Node)`
        - :py:func:`LineTo(Node)`
        - :py:func:`CurveTo(Node)`
        - :py:func:`SplineTo(Node)`
        - :py:func:`Finish()`

        Args:
            iterator (Any): The iterator object.
        """
        raise NotImplementedError

    def Rotate3D(self) -> None:
        """
        _summary_
        """
        raise NotImplementedError

    def Extrude3D(self, outlinewidth: int, shift_x: int, shift_y: int) -> None:
        """
        _summary_

        Args:
            outlinewidth (int): _description_
            shift_x (int): _description_
            shift_y (int): _description_
        """
        raise NotImplementedError

    def Shadow(self, outlinewidth: int, shift_x: int, shift_y: int) -> None:
        """
        _summary_

        Args:
            outlinewidth (int): _description_
            shift_x (int): _description_
            shift_y (int): _description_
        """
        raise NotImplementedError

    def College(self, outlinewidth: int, distance: int) -> None:
        """
        _summary_

        Args:
            outlinewidth (int): _description_
            distance (int): _description_
        """
        raise NotImplementedError

    def Gradient(
        self,
        outlinewidth: int,
        direction: int,
        stripes_number: int,
        start_y: int,
        finish_y: int,
    ) -> None:
        """
        _summary_

        Args:
            outlinewidth (int): _description_
            direction (int): _description_
            stripes_number (int): _description_
            start_y (int): _description_
            finish_y (int): _description_
        """
        raise NotImplementedError

    def Distance(
        self, width_x: int, width_y: int, cornermode: int, dest: Glyph | None = None
    ) -> None:
        """
        _summary_

        Args:
            width_x (int): _description_
            width_y (int): _description_
            cornermode (int): _description_
            dest (Glyph | None, optional): _description_. Defaults to None.
        """
        raise NotImplementedError

    def Interpolate(self, nodes: list[tuple[int, Point]]) -> list[tuple[int, Point]]:
        """
        __summary__

        Args:
            nodes (list[tuple[int, Point]]): _description_

        Returns:
            list[tuple[int, Point]]: _description_
        """
        raise NotImplementedError

    def Warp(self, points: list[Point], force: float) -> None:
        """
        _summary_

        Args:
            points (list[Point]): _description_
            force (float): _description_
        """
        raise NotImplementedError

    def Rasterize(self, image: Image) -> None:
        """
        _summary_

        Args:
            image (Image): _description_
        """
        raise NotImplementedError

    def Blend(self, source: Glyph, layer1: int, layer2: int, amount: Point) -> Glyph:
        """
        Return a blend of the glyph and source.

        Args:
            source (Glyph): _description_
            layer1 (int): _description_
            layer2 (int): _description_
            amount (Point): _description_

        Returns:
            Glyph: The blended glyph.
        """
        raise NotImplementedError

    def JoinAll(self) -> None:
        """
        Tries to join all open contours.
        """
        raise NotImplementedError

    def SaveEPS(self, filename: str, layer: int = 0) -> None:
        """
        Write a glyph master into the EPS file named filename.

        Args:
            filename (str): The path and file name.
            layer (int, optional): The master index. Defaults to 0.
        """
        raise NotImplementedError

    def LoadEPS(self, filename: str) -> Glyph:
        """
        Read an EPS file from filename and return it as a Glyph object.

        Use the :py:meth:`Assign` method to replace current the glyph with the
        imported outline.

        Args:
            filename (str): The path and file name.

        Returns:
            Glyph: The imported glyph.
        """
        raise NotImplementedError

    def R(self, points: list[Point], force: float = 0.0) -> None:
        """
        Present in the docstring but raises an :py:class:`AttributeError`.

        Args:
            points (list[Point]): A list of points.
            force (float, optional): The force. Defaults to 0.0.

        Raises:
            AttributeError: Always.
        """
        raise AttributeError

    # Additional methods reported by dir(fl.glyph)

    def EditMask(self) -> None:
        raise NotImplementedError

    def ExchangeMask(self) -> None:
        raise NotImplementedError

    def clear(self) -> None:
        raise NotImplementedError

    # FakeLab Defaults

    def set_defaults(self) -> None:
        self._parent = None
        self._nodes: ListParent[Node] = ListParent([], self)

        # custom data defined for this glyph
        self.customdata = None

        # note defined for this glyph
        self.note = None

        self.mark = 0
        self._anchors: list[Anchor] = []
        self._hhints: ListParent[Hint] = ListParent([], self)
        self._vhints: ListParent[Hint] = ListParent([], self)
        self._hlinks: ListParent[Link] = ListParent([], self)
        self._vlinks: ListParent[Link] = ListParent([], self)
        self._hguides: ListParent[Guide] = ListParent([], self)
        self._vguides: ListParent[Guide] = ListParent([], self)
        self._components: ListParent[Component] = ListParent([], self)
        self._replace_table: list[Replace] = []
        self._kerning: ListParent[KerningPair] = ListParent([], self)
        self._layers_number = 1
        self._mask: Glyph | None = None

        # flags set for this glyph
        self.flags: int = 0

        # list of Unicode indexes
        self.unicodes: list[int] = []

        # glyph name
        self.name = ""

        # [Image]           - background image (new in FL 4.53 Win)
        self.image: Image = Image()

        # glyph index, -1 if orphan glyph (not reported by docstring)
        self._index = -1

        # TrueType data

        self.advance_width: int = 0
        self.advance_height: int = 0
        self.left_side_bearing: int = 0
        self.top_side_bearing: int = 0
        self.y_pels: int = 1
        self.number_of_contours: int = 0
        self.end_points: list[int] = []
        self.points: list[TTPoint] = []
        self.instructions: list[int] = []
        self.hdmx: list[int] = []
