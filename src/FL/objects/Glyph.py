from __future__ import annotations

from typing import TYPE_CHECKING, Any

from FL.helpers.ListParent import ListParent
from FL.objects.Rect import Rect

if TYPE_CHECKING:
    from FL import (
        Anchor,
        AuditRecord,
        Component,
        Font,
        Guide,
        Hint,
        Image,
        KerningPair,
        Link,
        Matrix,
        Node,
        Point,
        Replace,
        TTPoint,
    )


class Glyph:

    # Constructor

    def __init__(
        self, glyph_or_masterscount: Glyph | int = 1, nodes: list[Node] | None = None
    ) -> None:
        self.set_defaults()

        # Process params

        if isinstance(glyph_or_masterscount, Glyph):
            # Copy constructor
            raise NotImplementedError

        elif isinstance(glyph_or_masterscount, int):
            self._layers_number = glyph_or_masterscount
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
        self._parent = font
        self._index = index
        if font is None:
            self._index = -1
        for n in self.nodes:
            n.fake_update(self)

    def fake_deserialize(self, name: str, data: Any) -> None:
        """Add data from a VFB entry

        Args:
            name (str): The name of the entry
            data (_type_): The entry data
        """
        if name == "Glyph":
            self.name = data["name"]
            self._layers_number = data["num_masters"]
            for node_data in data["nodes"]:
                node = Node()
                node.fake_deserialize(node_data)
                self.nodes.append(node)
        elif name == "Links":
            pass
        elif name == "image":
            pass
        elif name == "Glyph Bitmaps":
            pass
        elif name == "2023":
            pass
        elif name == "Glyph Sketch":
            pass
        elif name == "2010":
            pass
        elif name == "mask":
            pass
        elif name == "2011":
            pass
        elif name == "2028":
            pass
        elif name == "Glyph Origin":
            pass
        elif name == "unicodes":
            self.unicodes.extend(data)
        elif name == "Glyph Unicode Non-BMP":
            self.unicodes.extend(data)
        elif name == "mark":
            self.mark: int = data
        elif name == "glyph.customdata":
            self.customdata = data
        elif name == "glyph.note":
            self.note = data
        elif name == "Glyph GDEF Data":
            pass
        elif name == "Glyph Anchors Supplemental":
            pass
        elif name == "Glyph Anchors MM":
            pass
        elif name == "Glyph Guide Properties":
            pass

    # Attributes

    @property
    def parent(self) -> Font | None:
        """
        Glyph's parent object, Font
        """
        return self._parent

    @property
    def nodes(self) -> ListParent[Node]:
        """
        list of Nodes
        """
        return self._nodes

    @property
    def anchors(self) -> list[Anchor]:
        """
        list of anchors
        """
        return self._anchors

    @property
    def hhints(self) -> ListParent[Hint]:
        """
        list of horizontal hints
        """
        return self._hhints

    @property
    def vhints(self) -> ListParent[Hint]:
        """
        list of vertical hints
        """
        return self._vhints

    @property
    def hlinks(self) -> ListParent[Link]:
        """
        list of horizontal links
        """
        return self._hlinks

    @property
    def vlinks(self) -> ListParent[Link]:
        """
        list of vertical links
        """
        return self._vlinks

    @property
    def hguides(self) -> ListParent[Guide]:
        """
        list of horizontal guides
        """
        return self._hguides

    @property
    def vguides(self) -> ListParent[Guide]:
        """
        list of vertical guides
        """
        return self._vguides

    @property
    def components(self) -> ListParent[Component]:
        """
        list of components
        """
        return self._components

    @property
    def replace_table(self) -> list[Replace]:
        """
        hint replacing program, list of Replace objects
        """
        return self._replace_table

    @property
    def kerning(self) -> ListParent[KerningPair]:
        """
        list of kerning pairs
        """
        return self._kerning

    @property
    def layers_number(self) -> int:
        """
        number of masters
        """
        return self._layers_number

    @property
    def mask(self) -> Glyph | None:
        """Return the mask of the glyph or None.

        Returns:
            Glyph | None: The mask glyph if present, otherwise None.
        """
        return self._mask

    @property
    def nodes_number(self) -> int:
        return len(self._nodes)

    @property
    def index(self) -> int:
        if self.parent is None:
            return -1
        return self._index

    # Operations

    def __len__(self) -> int:
        """
        Return the number of nodes.
        """
        return len(self._nodes)

    def __getitem__(self, index: int) -> Node:
        """
        Accesses nodes array
        """
        return self._nodes[index]

    def __slice__(self, a, b):
        raise NotImplementedError

    def __plus__(self, glyph_node_nodelist):
        raise NotImplementedError

    def __mul__(self, matrix):
        raise NotImplementedError

    # Methods

    def Assign(self, g: Glyph) -> None:
        """
        (Glyph)
        - copies all information from the assigned glyph
        """
        raise NotImplementedError

    def Transform(self, m: Matrix) -> None:
        """
        Applies Matrix transformation to the Glyph (see Matrix().__doc__)
        """
        raise NotImplementedError

    def SetLayersNumber(self, mastersnumber: int) -> None:
        """
        Change the number of masters, is applicable only to glyphs that have no
        parent
        """
        raise NotImplementedError

    def Clear(self) -> None:
        """
        Remove all nodes
        """
        raise NotImplementedError

    def Add(self, obj) -> None:
        """
        - refer to '+' operator
        """
        raise NotImplementedError

    def Insert(
        self, node_or_glyph_or_nodelist: Node | Glyph | list[Node], nodeindex: int = 0
    ) -> None:
        """
        (Node | Glyph | [Node]) | (Node | Glyph | [Node], nodeindex)

        Insert Node, Glyph or sequence of Nodes at the begining of glyph's
        nodes or at specified node index
        """
        raise NotImplementedError

    def Present(self, style) -> bool:
        """
        (style)

        Return True if a layer or a combination of layers are present in the
        glyph.
        """
        raise NotImplementedError

    def Delete(self, index0: int, index1: int | None = None) -> None:
        """
        (index) | (index0, index1)

        Remove node or range of nodes.
        """
        raise NotImplementedError

    def ExpandLayer(self, masterindex: int) -> None:
        """
        (masterindex)

        Expand selected master to all other masters.
        """
        raise NotImplementedError

    def Shift(self, point: Point, masterindex: int = 0) -> None:
        """
        (Point) | (Point, masterindex)

        Shift positions of all nodes at first or specified master.
        """
        raise NotImplementedError

    def Scale(self, scale: Point, center: Point, masterindex: int = 0) -> None:
        """
        (Point(float) scale) | (Point(float) scale, Point center) |
        (Point(float) scale, Point center, masterindex)

        Scale the glyph.
        """
        raise NotImplementedError

    def Layer(self, masterindex: int) -> list[Point]:
        """
        (masterindex)

        Return a list of Points for all nodes for the selected master.
        """
        raise NotImplementedError

    def Section(self, masterindex: int, pointindex: int, nodetype: int) -> list[Point]:
        """
        (masterindex, pointindex, nodetype)

        Return a list of Points that conform to selected options.
        """
        raise NotImplementedError

    def MoveNode(self, options) -> None:
        """
        Moves the node copying Edit tool behavior (see User manual for details).
        """
        raise NotImplementedError

    def DeleteNode(self, nodeindex) -> None:
        """
        Remove the Node.
        """
        raise NotImplementedError

    def InsertNode(self, nodeindex, time=0.0, masterindex=0) -> None:
        """
        (nodeindex) | (nodeindex, float time) |
        (nodeindex, float time, masterindex)

        Insert a new node on a contour.
        """
        raise NotImplementedError

    # SELECTION-METHODS

    def Selection(self) -> list[Node]:
        """
        Return a list of selected Nodes.
        """
        raise NotImplementedError

    def SelectAll(self) -> None:
        """
        Select all Nodes.
        """
        raise NotImplementedError

    def UnselectAll(self) -> None:
        """
        Deselect all Nodes.
        """
        raise NotImplementedError

    def InvertSelection(self) -> None:
        """
        Select unselected Nodes and deselects selected Nodes.
        """
        raise NotImplementedError

    def isAnySelected(self) -> bool:
        """
        Return True if at least one Node is selected.
        """
        raise NotImplementedError

    def SelectedCount(self) -> int:
        """
        Return the number of selected Nodes.
        """
        raise NotImplementedError

    def SelectRect(self, r, masterindex=0) -> None:
        """
        (Rect r) | (Rect r, masterindex)

        Select all Nodes that are inside the rectangle.
        """
        raise NotImplementedError

    def UnselectRect(self, r, masterindex=0) -> None:
        """
        (Rect r) | (Rect r, masterindex)

        Deselect all Nodes that are inside the rectangle.
        """
        raise NotImplementedError

    def DeleteSelected(self) -> None:
        """
        Delete all selected Nodes.
        """
        raise NotImplementedError

    # METRICS-METHODS

    def GetBoundingRect(self, masterindex: int = 0) -> Rect:
        """
        () | (masterindex)

        Return Rect - bounding box of the glyph.
        """
        if masterindex != 0:
            raise NotImplementedError

        rect = None
        for n in self._nodes:
            if rect is None:
                rect = Rect(n.point)
            else:
                rect += n.point
        return rect

    def GetMetrics(self, masterindex: int = 0) -> Point:
        """
        () | (masterindex)

        Return the glyph advance width and advance height in a form of Point.
        """
        raise NotImplementedError

    def SetMetrics(self, p: Point, masterindex: int = 0) -> None:
        """
        (Point p) | (Point p, masterindex)

        Assign new values to the width and height of the glyph.
        """
        raise NotImplementedError

    def GetVSB(self, masterindex: int = 0) -> int:  # TODO: Is it int?
        """
        () | (masterindex)

        Return glyph bottom sidebearing position.
        """
        raise NotImplementedError

    def SetVSB(self, value: int, masterindex: int = 0) -> int:  # TODO: Is it int?
        """
        (value) | (value, masterindex)

        Assign new values to the bottom sidebearing of the glyph.
        """
        raise NotImplementedError

    # OVERLAP-METHODS

    def RemoveOverlap(self, masterindex: int = 0) -> None:
        """
        () | (masterindex)

        Remove overlap.
        """
        raise NotImplementedError

    def Badd(self, glyph_nodelist: Glyph | list[Node], masterindex: int = 0) -> None:
        """
        (Glyph g) | ([Node]) | (Glyph g, masterindex) | ([Node], masterindex)

        Perform boolean Add operation with the glyph or list of nodes.
        """
        raise NotImplementedError

    def Bsubtract(
        self, glyph_nodelist: Glyph | list[Node], masterindex: int = 0
    ) -> None:
        """
        (Glyph g) | ([Node]) | (Glyph g, masterindex) | ([Node], masterindex)

        Perform boolean Subtract operation with the glyph or list of nodes.
        """
        raise NotImplementedError

    def Bintersect(
        self, glyph_nodelist: Glyph | list[Node], masterindex: int = 0
    ) -> None:
        """
        (Glyph g) | ([Node]) | (Glyph g, masterindex) | ([Node], masterindex)
        - performs bollean Insersect operation with the glyph or list of nodes
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
        (contourindex)

        Return the index of the first node for a contour.
        """
        raise NotImplementedError

    def GetContourLength(self, contourindex: int) -> int:
        """
        (contourindex)

        Return the number of nodes in a contour.
        """
        raise NotImplementedError

    def SelectContour(self, contourindex: int) -> None:
        """
        (contourindex)

        Select all nodes in the contour.
        """
        raise NotImplementedError

    def DeleteContour(self, contourindex: int) -> None:
        """
        (contourindex)

        Remove contour.
        """
        raise NotImplementedError

    def ReverseContour(self, contourindex: int) -> None:
        """
        (contourindex)

        Reverse contour's direction
        """
        raise NotImplementedError

    def ReorderContour(self, contourindex: int, newindex: int) -> None:
        """
        (contourindex, newindex)

        Reorder contours in the glyph.
        """
        raise NotImplementedError

    def isContourClockwise(self, contourindex: int) -> bool:
        """
        (contourindex)

        Return True if direction of contour is clockwise.
        """
        raise NotImplementedError

    def SetStartNode(self, nodeindex: int) -> None:
        """
        (nodeindex)

        Make the node a starting node of the contour.
        """
        raise NotImplementedError

    def FindContour(self, nodeindex: int) -> int:
        """
        (nodeindex)

        Return number of contour containing the 'nodeindex'.
        """
        raise NotImplementedError

    # HINTS-METHODS

    def RemoveHints(self, mode: int) -> None:
        """
        (integer mode)

        Remove hints and links.
        """
        raise NotImplementedError

    def Autohint(self, masterindex: int = 0) -> None:
        """
        () | (masterindex)

        Automatically generates Type 1 hints
        """
        raise NotImplementedError

    # ANCHOR-METHODS

    def FindAnchor(self, name: str) -> Anchor:  # XXX: does it return an anchor?
        """
        (string name)

        Finds Anchor by name
        """
        raise NotImplementedError

    # TRANSFORMATION-METHODS

    def Decompose(self) -> None:
        """
        Paste all components to the glyph outline.
        """
        raise NotImplementedError

    def MakeExtremeNodes(self, masterindex: int) -> None:
        """
        () | (masterindex)

        Automatically detect and adds extreme nodes.
        """
        raise NotImplementedError

    def Audit(self) -> list[AuditRecord]:
        """
        () | (masterindex)
        Perform test of the glyph and returns list of AuditRecord objects.
        """
        raise NotImplementedError

    def Iterate(self):
        """
        (Iterator)

        Iterate glyph trough iterator class which must include following
        methods:

        * Start()
        * ClosePath()
        * StartPath(Node)
        * LineTo(Node)
        * CurveTo(Node)
        * SplineTo(Node)
        * Finish()
        """
        raise NotImplementedError

    def Rotate3D(self):
        raise NotImplementedError

    def Extrude3D(self, outlinewidth, shift_x, shift_y):
        raise NotImplementedError

    def Shadow(self, outlinewidth, shift_x, shift_y):
        raise NotImplementedError

    def College(self, outlinewidth, distance):
        raise NotImplementedError

    def Gradient(self, outlinewidth, direction, stripes_number, start_y, finish_y):
        raise NotImplementedError

    def Distance(self, width_x, width_y, cornermode, dest=None):
        """
        (width_x, width_y, cornermode) |
        (width_x, width_y, cornermode, Glyph dest)
        """
        raise NotImplementedError

    def Interpolate(self, nodes) -> list[tuple[int, Point]]:
        """
        ([(nodeindex, Point newposition)])
        """
        raise NotImplementedError

    def Warp(self, points: list[Point], force: float) -> None:
        """
        ([Point], float force)
        """
        raise NotImplementedError

    def Rasterize(self) -> Image:
        """
        (Image)
        """
        raise NotImplementedError

    def Blend(self, source: Glyph, layer1: int, layer2: int, amount: Point) -> Glyph:
        """
        (Glyph source, integer layer1, integer layer2, Point amount)

        Return blend of the glyph and source.
        """
        raise NotImplementedError

    def JoinAll(self) -> None:
        """
        Tries to join all open contours.
        """
        raise NotImplementedError

    def SaveEPS(self, filename: str, layer: int = 0) -> None:
        """
        (string filename) | (string filename, layer)

        Write layer into the EPS file named filename.
        """
        raise NotImplementedError

    def LoadEPS(self, filename: str) -> None:
        """
        (string filename)

        Read EPS from filename and returns Glyph object.

        Use Assign method to replace current glyph with the loaded outline.
        """
        raise NotImplementedError

    def R(self, points: list[Point], force: float = 0.0) -> None:
        """
        ([Point], float force)

        - (?? comes from the __doc__-string but raises an AttributeError)
        """
        raise AttributeError

    # Additional methods reported by dir(fl.glyph)

    def EditMask(self) -> None:
        raise NotImplementedError

    def ExchangeMask(self) -> None:
        raise NotImplementedError

    def clear(self) -> None:
        raise NotImplementedError

    # Defaults

    def set_defaults(self) -> None:
        self._parent = None
        self._nodes: ListParent[Node] = ListParent([], self)

        # custom data defined for this glyph
        self.customdata: str | None = None

        # note defined for this glyph
        self.note: str | None = None

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

        # (integer)         - flags set for this glyph
        self.flags: int = 0

        # (integer)         - advance width for the first master
        self.width: int = 0

        # (integer)        - advance height for the first master
        self.height: int = 0

        # (integer)       - first Unicode index in integer form
        self.unicode: int | None = None

        # [integer]      - list of Unicode indexes
        self.unicodes: list[int] = []

        # (string)           - glyph name
        self.name: str = ""

        # [Image]           - background image (new in FL 4.53 Win)
        self.image: Image = Image()

        # glyph index, -1 if orphan glyph (not reported by docstring)
        self._index: int = -1

        # TrueType data

        self.advance_width: int = 0  # (integer)
        self.advance_height: int = 0  # (integer)
        self.left_side_bearing: int = 0  # (integer)
        self.top_side_bearing: int = 0  # (integer)
        self.y_pels: int = 1  # (integer)
        self.bounding_box: Rect = Rect(32767, 32767, -32767, -32767)  # (Rect)
        self.number_of_contours: int = 0  # (integer)
        self.end_points: list[int] = []  # [integer]
        self.points: list[TTPoint] = []  # [TTPoint]
        self.instructions: list[int] = []  # [Byte]
        self.hdmx: list[int] = []  # [Byte]
