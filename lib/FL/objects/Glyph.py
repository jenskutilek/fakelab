from __future__ import annotations

from FL.objects.Rect import Rect

# from FL.helpers.ListParent import ListParent


class Glyph:
    def __init__(self, glyph_or_masterscount=1, nodes=None):
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
                    node._parent = self
                    self._nodes.append(node)
        # else: Empty Glyph

    def __repr__(self):
        return "<Glyph: '%s', %i nodes, orphan>" % (self.name, len(self))

    # Additions for FakeLab

    def fake_update(self, font=None, index=-1):
        """
        Is called from FontLab.UpdateFont()
        """
        self._parent = font
        self._index = index
        if font is None:
            self._index = -1
        for n in self.nodes:
            n.fake_update(self)

    # Attributes

    @property
    def parent(self):
        """
        Glyph's parent object, Font
        """
        return self._parent

    @property
    def nodes(self):
        """
        list of Nodes
        """
        return self._nodes

    @property
    def anchors(self):
        """
        list of anchors
        """
        return self._anchors

    @property
    def hhints(self):
        """
        list of horizontal hints
        """
        return self._hhints

    @property
    def vhints(self):
        """
        list of vertical hints
        """
        return self._vhints

    @property
    def hlinks(self):
        """
        list of horizontal links
        """
        return self._hlinks

    @property
    def vlinks(self):
        """
        list of vertical links
        """
        return self._vlinks

    @property
    def hguides(self):
        """
        list of horizontal guides
        """
        return self._hguides

    @property
    def vguides(self):
        """
        list of vertical guides
        """
        return self._vguides

    @property
    def components(self):
        """
        list of components
        """
        return self._components

    @property
    def replace_table(self):
        """
        hint replacing program, list of Replace objects
        """
        return self._replace_table

    @property
    def kerning(self):
        """
        list of kerning pairs
        """
        return self._kerning

    @property
    def layers_number(self):
        """
        number of masters
        """
        return self._layers_number

    @property
    def nodes_number(self):
        return len(self._nodes)

    @property
    def index(self):
        if self.parent is None:
            return -1
        return self._index

    # Operations

    def __len__(self):
        """
        Return the number of nodes.
        """
        return len(self._nodes)

    def __getitem__(self, index):
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

    def Assign(self, g):
        """
        (Glyph)
        - copies all information from the assigned glyph
        """
        raise NotImplementedError

    def Transform(self, m):
        """
        Applies Matrix transformation to the Glyph (see Matrix().__doc__)
        """
        raise NotImplementedError

    def SetLayersNumber(self, mastersnumber):
        """
        Change the number of masters, is applicable only to glyphs that have no
        parent
        """
        raise NotImplementedError

    def Clear(self):
        """
        Remove all nodes
        """
        raise NotImplementedError

    def Add(self, obj):
        """
        - refer to '+' operator
        """
        raise NotImplementedError

    def Insert(self, node_or_glyph_or_nodelist, nodeindex=0):
        """
        (Node | Glyph | [Node]) | (Node | Glyph | [Node], nodeindex)

        Insert Node, Glyph or sequence of Nodes at the begining of glyph's
        nodes or at specified node index
        """
        raise NotImplementedError

    def Present(self, style):
        """
        (style)

        Return True if a layer or a combination of layers are present in the
        glyph.
        """
        raise NotImplementedError

    def Delete(self, index0, index1=None):
        """
        (index) | (index0, index1)

        Remove node or range of nodes.
        """
        raise NotImplementedError

    def ExpandLayer(self, masterindex):
        """
        (masterindex)

        Expand selected master to all other masters.
        """
        raise NotImplementedError

    def Shift(self, point, masterindex=0):
        """
        (Point) | (Point, masterindex)

        Shift positions of all nodes at first or specified master.
        """
        raise NotImplementedError

    def Scale(self, scale, center, masterindex=0):
        """
        (Point(float) scale) | (Point(float) scale, Point center) |
        (Point(float) scale, Point center, masterindex)

        Scale the glyph.
        """
        raise NotImplementedError

    def Layer(self, masterindex):
        """
        (masterindex)

        Return a list of Points for all nodes for the selected master.
        """
        raise NotImplementedError

    def Section(self, masterindex, pointindex, nodetype):
        """
        (masterindex, pointindex, nodetype)

        Return a list of Points that conform to selected options.
        """
        raise NotImplementedError

    def MoveNode(self, options):
        """
        Moves the node copying Edit tool behavior (see User manual for details).
        """
        raise NotImplementedError

    def DeleteNode(self, nodeindex):
        """
        Remove the Node.
        """
        raise NotImplementedError

    def InsertNode(self, nodeindex, time=0.0, masterindex=0):
        """
        (nodeindex) | (nodeindex, float time) |
        (nodeindex, float time, masterindex)

        Insert a new node on a contour.
        """
        raise NotImplementedError

    # SELECTION-METHODS

    def Selection(self):
        """
        Return a list of selected Nodes.
        """
        raise NotImplementedError

    def SelectAll(self):
        """
        Select all Nodes.
        """
        raise NotImplementedError

    def UnselectAll(self):
        """
        Deselect all Nodes.
        """
        raise NotImplementedError

    def InvertSelection(self):
        """
        Select unselected Nodes and deselects selected Nodes.
        """
        raise NotImplementedError

    def isAnySelected(self):
        """
        Return True if at least one Node is selected.
        """
        raise NotImplementedError

    def SelectedCount(self):
        """
        Return the number of selected Nodes.
        """
        raise NotImplementedError

    def SelectRect(self, r, masterindex=0):
        """
        (Rect r) | (Rect r, masterindex)

        Select all Nodes that are inside the rectangle.
        """
        raise NotImplementedError

    def UnselectRect(self, r, masterindex=0):
        """
        (Rect r) | (Rect r, masterindex)

        Deselect all Nodes that are inside the rectangle.
        """
        raise NotImplementedError

    def DeleteSelected(self):
        """
        Delete all selected Nodes.
        """
        raise NotImplementedError

    # METRICS-METHODS

    def GetBoundingRect(self, masterindex=0):
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

    def GetMetrics(self, masterindex=0):
        """
        () | (masterindex)

        Return the glyph advance width and advance height in a form of Point.
        """
        raise NotImplementedError

    def SetMetrics(self, p, masterindex=0):
        """
        (Point p) | (Point p, masterindex)

        Assign new values to the width and height of the glyph.
        """
        raise NotImplementedError

    def GetVSB(self, masterindex=0):
        """
        () | (masterindex)

        Return glyph bottom sidebearing position.
        """
        raise NotImplementedError

    def SetVSB(self, value, masterindex=0):
        """
        (value) | (value, masterindex)

        Assign new values to the bottom sidebearing of the glyph.
        """
        raise NotImplementedError

    # OVERLAP-METHODS

    def RemoveOverlap(self, masterindex=0):
        """
        () | (masterindex)

        Remove overlap.
        """
        raise NotImplementedError

    def Badd(self, glyph_nodelist, masterindex=0):
        """
        (Glyph g) | ([Node]) | (Glyph g, masterindex) | ([Node], masterindex)

        Perform boolean Add operation with the glyph or list of nodes.
        """
        raise NotImplementedError

    def Bsubtract(self, glyph_nodelist, masterindex=0):
        """
        (Glyph g) | ([Node]) | (Glyph g, masterindex) | ([Node], masterindex)

        Perform boolean Subtract operation with the glyph or list of nodes.
        """
        raise NotImplementedError

    def Bintersect(self, glyph_nodelist, masterindex=0):
        """
        (Glyph g) | ([Node]) | (Glyph g, masterindex) | ([Node], masterindex)
        - performs bollean Insersect operation with the glyph or list of nodes
        """
        raise NotImplementedError

    # CONTOUR-METHODS

    def GetContoursNumber(self):
        """
        Return the number of contours in the glyph.
        """
        raise NotImplementedError

    def GetContourBegin(self, contourindex):
        """
        (contourindex)

        Return the index of the first node for a contour.
        """
        raise NotImplementedError

    def GetContourLength(self, contourindex):
        """
        (contourindex)

        Return the number of nodes in a contour.
        """
        raise NotImplementedError

    def SelectContour(self, contourindex):
        """
        (contourindex)

        Select all nodes in the contour.
        """
        raise NotImplementedError

    def DeleteContour(self, contourindex):
        """
        (contourindex)

        Remove contour.
        """
        raise NotImplementedError

    def ReverseContour(self, contourindex):
        """
        (contourindex)

        Reverse contour's direction
        """
        raise NotImplementedError

    def ReorderContour(self, contourindex, newindex):
        """
        (contourindex, newindex)

        Reorder contours in the glyph.
        """
        raise NotImplementedError

    def isContourClockwise(self, contourindex):
        """
        (contourindex)

        Return True if direction of contour is clockwise.
        """
        raise NotImplementedError

    def SetStartNode(self, nodeindex):
        """
        (nodeindex)

        Make the node a starting node of the contour.
        """
        raise NotImplementedError

    def FindContour(self, nodeindex):
        """
        (nodeindex)

        Return number of contour containing the 'nodeindex'.
        """
        raise NotImplementedError

    # HINTS-METHODS

    def RemoveHints(self, mode):
        """
        (integer mode)

        Remove hints and links.
        """
        raise NotImplementedError

    def Autohint(self, masterindex=0):
        """
        () | (masterindex)

        Automatically generates Type 1 hints
        """
        raise NotImplementedError

    # ANCHOR-METHODS

    def FindAnchor(self, name):
        """
        (string name)

        Finds Anchor by name
        """
        raise NotImplementedError

    # TRANSFORMATION-METHODS

    def Decompose(self):
        """
        Paste all components to the glyph outline.
        """
        raise NotImplementedError

    def MakeExtremeNodes(self, masterindex):
        """
        () | (masterindex)

        Automatically detect and adds extreme nodes.
        """
        raise NotImplementedError

    def Audit(self):
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

    def Interpolate(self, nodes):
        """
        ([(nodeindex, Point newposition)])
        """
        raise NotImplementedError

    def Warp(self, points, force):
        """
        ([Point], float force)
        """
        raise NotImplementedError

    def Rasterize(self):
        """
        (Image)
        """
        raise NotImplementedError

    def Blend(self, source, layer1, layer2, amount):
        """
        (Glyph source, integer layer1, integer layer2, Point amount)

        Return blend of the glyph and source.
        """
        raise NotImplementedError

    def JoinAll(self):
        """
        Tries to join all open contours.
        """
        raise NotImplementedError

    def SaveEPS(self, filename, layer=0):
        """
        (string filename) | (string filename, layer)

        Write layer into the EPS file named filename.
        """
        raise NotImplementedError

    def LoadEPS(self, filename):
        """
        (string filename)

        Read EPS from filename and returns Glyph object.

        Use Assign method to replace current glyph with the loaded outline.
        """
        raise NotImplementedError

    def R(self, points, force=0.0):
        """
        ([Point], float force)

        - (?? comes from the __doc__-string but raises an AttributeError)
        """
        raise AttributeError

    # Additional methods reported by dir(fl.glyph)

    def EditMask(self):
        raise NotImplementedError

    def ExchangeMask(self):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError

    # Defaults

    def set_defaults(self):
        self._parent = None
        self._nodes = []

        # custom data defined for this glyph
        self.customdata = ""

        # note defined for this glyph
        self.note = ""

        self.mark = 0
        self._anchors = []
        self._hhints = []
        self._vhints = []
        self._hlinks = []
        self._vlinks = []
        self._hguides = []
        self._vguides = []
        self._components = []
        self._replace_table = []
        self._kerning = []  # ListParent()
        self._layers_number = 1

        # (integer)         - flags set for this glyph
        self.flags = 0

        # (integer)         - advance width for the first master
        self.width = 0

        # (integer)        - advance height for the first master
        self.height = 0

        # (integer)       - first Unicode index in integer form
        self.unicode = None

        # [integer]      - list of Unicode indexes
        self.unicodes = []

        # (string)           - glyph name
        self.name = ""

        # [Image]           - background image (new in FL 4.53 Win)
        self.image = None

        # glyph index, -1 if orphan glyph (not reported by docstring)
        self._index = -1

        # TrueType data

        self.advance_width = None  # (integer)
        self.advance_height = None  # (integer)
        self.left_side_bearing = None  # (integer)
        self.top_side_bearing = None  # (integer)
        self.y_pels = None  # (integer)
        self.bounding_box = None  # (Rect)
        self.number_of_contours = None  # (integer)
        self.end_points = None  # [integer]
        self.points = None  # [TTPoint]
        self.instructions = None  # [Byte]
        self.hdmx = None  # [Byte]
