from __future__ import annotations

from FL.objects.Font import Font
from FL.objects.Point import Point


class FakeLab:
    """
    The main class. It is used via the pre-instantiated object `fl`.
    """

    def __init__(self):
        self._font = None

        # (integer)  - index of currently active font
        self._ifont = -1

        self.fonts = []

        # (integer) - index of currently selected font in the fonts list panel
        self.ifontslist = 0

        self._glyph = None

        # (integer)  - index of currently active glyph
        self.iglyph = -1

        # (integer)  - read-only - type of the currently selected object in the
        # Glyph Window
        self._tobject = None

        # (integer)  - read-only - index of currently selected object in the
        # Glyph Window
        self._iobject = None

        # (<a href="Point.xml.html">Point</a>)  - delta value of current
        # coordinate translation in the active Glyph Window
        self.delta = None

        # (<a href="Point.xml.html">Point</a>(float))      - scale value of
        # current coordinate translation in the active Glyph Window
        self.scale = None

        # (boolean)   - True if tablet is present and active
        self._tablet_active = False

        # (integer) - current tablet's pen pressure
        self._tablet_pressure = 0

        # (string)          - contents of the preview panel <font color="red">
        # (not reported by docstring)</font>
        self.preview = ""

        self._layer = None

    # Operations

    def __len__(self):
        """
        returns number of opened fonts
        """
        return len(self.fonts)

    def __getitem__(self, index):
        """
        returns Font by index
        """
        return self.fonts[index]

    # Attributes

    @property
    def font(self):
        """
        Return the currently active font or None.
        """
        return self._font

    @property
    def ifont(self):
        """
        index of currently active font
        """
        return self._ifont

    @ifont.setter
    def ifont(self, value):
        self._ifont = value
        if self._ifont == -1:
            self._font = None
        else:
            self._font = self.fonts[self._ifont]

    @property
    def glyph(self):
        """
        Return the currently active glyph in Font, Glyph or Metrics windows.
        """
        return self._glyph

    @property
    def tobject(self):
        """
        Return the type of the currently selected object in the Glyph Window
        as int.
        """
        raise SystemError

    @property
    def iobject(self):
        """
        Return the index of currently selected object in the Glyph Window.
        """
        raise SystemError

    @property
    def mainwindow(self):
        """
        reference to FontLab's main window
        """
        return 0

    @property
    def path(self):
        """
        full path to directory where running application is located
        """
        return "/Library/Application Support/FontLab/Studio 5"

    @property
    def filename(self):
        """
        application filename
        """
        return "FontLab Studio 5 5730.app"

    @property
    def version(self):
        """
        application version
        """
        return "5.1.6/Mac(Build 7030)"

    @property
    def productnumber(self):
        """
        product number
        """
        return 0

    @property
    def serialnumber(self):
        """
        serial number as appears in the About window
        """
        return ""

    @property
    def username(self):
        """
        user name as appears in the About window
        """
        return "FontLab User"

    @property
    def count(self):
        """
        number of opened fonts (fast operation)
        """
        return self.__len__()

    @property
    def count_selected(self):
        """
        number of the selected glyphs
        in the Font Window (fast operation)
        """
        # FIXME
        return 0

    @property
    def window(self):
        """
        reference to the currently active Glyph, Font or Metrics window
        """
        # FIXME
        return 0

    # Properties not reported in the docs

    @property
    def layer(self):
        """
        Return the index of the currently active layer (master) in Glyph or
        Metrics windows.
        """
        return self._layer

    # Methods

    def Close(self, fontindex=None):
        """
        () | (fontindex)      - closes the current or 'fontindex' font
        """
        if fontindex is None:
            del self.fonts[self._ifont]
        else:
            del self.fonts[fontindex]
        if self.count == 0:
            self.ifont = -1
        else:
            self.ifont = self.count - 1

    def Open(self, filename: str, addtolist: bool = True) -> Font:
        """
        (string filename) | (string filename, boolean addtolist)

        Open the font from file using current opening options.

        If 'addtolist' is True, font is added to FontLab's font list
        """
        font = Font()
        font.Open(filename)
        if addtolist:
            self.Add(font)
        return font

    def Save(self, filename_or_fontindex, filename=None):
        """
        (string filename) | (int fontindex, string filename)

        Save the current or selected font using standard FontLab's Save
        routine.
        """
        if isinstance(filename_or_fontindex, int):
            # Save the font fontindex
            fontindex = filename_or_fontindex
            if 0 <= fontindex < self.count:
                self._fonts[fontindex].Save(filename)
        else:
            # Save the current font
            if self.font is not None:
                filename = filename_or_fontindex
                self.font.Save(filename)

    def GenerateFont(self, fontType, filename):
        """
        (fontType, filename)

        - generates Font, available font types:

          - ftFONTLAB            - FontLab VFB font
          - ftTYPE1              - PC Type 1 font (binary/PFB)
          - ftTYPE1_MM           - PC MultipleMaster font (PFB)
          - ftTYPE1ASCII         - PC Type 1 font (ASCII/PFA)
          - ftTYPE1ASCII_MM      - PC MultipleMaster font (ASCII/PFA)
          - ftTRUETYPE           - PC TrueType/TT OpenType font (TTF)
          - ftOPENTYPE           - PS OpenType (CFF-based) font (OTF)
          - ftMACTYPE1           - Mac Type 1 font (generates suitcase
            and LWFN file, optionally AFM)
          - ftMACTRUETYPE        - Mac TrueType font (generates suitcase)
          - ftMACTRUETYPE_DFONT  - Mac TrueType font (generates suitcase with
            resources in data fork)
        """
        # We cannot generate a font at the moment, let's fake it.
        # Check if the current font has a fake_binary.
        binary = self.font.fake_binary_get(fontType)
        if binary:
            with open(filename, "wb") as f:
                f.write(binary)
        else:
            raise NotImplementedError
        # TODO: What should be the return value?

    def Add(self, font):
        """
        Add 'font' to list of opened fonts and opens the Font Window for it.
        """
        self.fonts.append(font)
        self.ifont = len(self.fonts) - 1
        # As long as no glyph window is open,
        # delta and scale will be points at (0, 0)
        self.delta = Point()
        self.scale = Point()
        self._layer = 0

    def UpdateFont(self, fontindex=None):
        """
        () | (fontindex)

        - updates current font or 'fontindex' (slow operation)
        """
        if fontindex is None:
            fontindex = self.ifont
        self.fonts[fontindex].fake_update()

    def SetFontWindow(self, fontindex, position, state):
        """
        (fontindex, Rect position, state)

        - sets window size and style for Font Window
          here font 'fontindex' is presented
        """
        raise NotImplementedError

    def UpdateGlyph(self, glyphindex=None):
        """
        () | (glyphindex)

        - updates current or 'glyphindex' glyph of the current font
        """
        raise NotImplementedError

    def EditGlyph(self, glyphindex=None):
        """
        () | (glyphindex)

        - opens the Glyph window for the 'glyphindex' glyph
          in the current font
        """
        raise NotImplementedError

    def CallCommand(self, commandcode):
        """
        (commandcode)

        - simulates the menu or toolbar command.
          Check WS_* constants for list of available commands
        """
        raise NotImplementedError

    def Selected(self, glyphindex=None):
        """
        () | (glyphindex)

        Return 1 if current glyph or 'glyphindex' glyph is selected.
        """
        if glyphindex is None:
            raise NotImplementedError
            # return 1 if fl.glyph.selected

        if glyphindex in self.font._selection:
            return 1

        return 0

    def Select(self, glyphid, value=None):
        """
        (glyphid) | (glyphid, value)

        - changes glyph's selection state.
          'glyphid' may be string (glyph name),
          Uni (Unicode index) or integer (glyph index)
        """
        if isinstance(glyphid, str):
            glyphid = self.font.FindGlyph(glyphid)
        if value is None:
            value = True
        self.font.fake_select(glyphid, value)

    def Unselect(self):
        """
        Deselect all glyphs in the current font (fast operation).
        """
        self.font.fake_deselect_all()

    def Message(self, message, question=None, okstring=None, cancelstring=None):
        """
        (string message, string question, string OKstring, string Cancelstring)
        - shows the alert message dialog box,
          all parameters but first can be omitted
        """
        raise NotImplementedError

    def ScreenToGlyph(self, position):
        """
        (:py:class:`FL.Point` position)
        - converts screen coordinates to glyph
          coordinates in the current Glyph Window
        """
        raise NotImplementedError

    def GlyphToScreen(self, position):
        """
        (:py:class:`FL.Point` position)
        - converts glyph coordinates to screen
          coordinates in the current Glyph Window
        """
        raise NotImplementedError

    def UpdateRect(self, r):
        """
        (:py:class:`FL.Rect` r)
        - updates rectangle in the current Glyph Window
        """
        raise NotImplementedError

    def HitContour(self, p):
        """
        (:py:class:`FL.Point` p)
        - contour hit detection in the current Glyph Window -
          returns tuple of (nodeindex, nodesubindex, hit_time)
        """
        raise NotImplementedError

    def GetCanvas(self):
        """
        Return a :py:class:`Canvas` for the current Glyph Window.
        """
        raise NotImplementedError

    def GetConvert(self, c):
        """
        (:py:class:`Canvas` c)

        - copies conversion parameters from the current Glyph Window to the
        :py:class:`Canvas` c.
        """
        raise NotImplementedError

    def BeginProgress(self, title, counts):
        """
        (string title, counts)

        - opens the Progress dialog box with. 'counts' - number of 'ticks'
        """
        raise NotImplementedError

    def TickProgress(self, tick):
        """
        (tick)

        - updates the Progress bar,
          returns False if Cancel button was pressed.
          This is relatively 'expensive' operation
        """
        raise NotImplementedError

    def EndProgress(self):
        """
        Close the Progress dialog box.
        """
        raise NotImplementedError

    def Random(self, lovalue, hivalue=None):
        """
        (hivalue) | (lovalue, hivalue)

        - returns random value (fast operation)
        """
        raise NotImplementedError

    def TransformGlyph(self, glyph, code, text):
        """
        (:py:class:`Glyph` glyph, code, text)

        - transforms the glyph using one of the Transform actions.
          Save one of Transform Range programs for reference to
          format of the command string
        """
        raise NotImplementedError

    def ForSelected(self, function_name):
        """
        (string function_name)
        - calls 'function_name' for each selected glyph in the current
          font. Function has following format:
          function(:py:class:`Font` font, :py:class:`Glyph` glyph, glyphindex)
        """
        raise NotImplementedError

    def SetUndo(self):
        """
        Save current state to undo buffer.

        (this method is not reported by the docstring)
        """
        raise NotImplementedError
