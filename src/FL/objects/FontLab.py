from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable

from FL import ftFONTLAB, ftOPENTYPE, ftTRUETYPE
from FL.fake.FontImporter import FontImporter
from FL.objects.Font import Font
from FL.objects.Options import Options
from FL.objects.Point import Point

if TYPE_CHECKING:
    from FL.objects.Canvas import Canvas
    from FL.objects.Glyph import Glyph
    from FL.objects.Rect import Rect
    from FL.objects.Uni import Uni


__doc__ = "Class to represent the FontLab program interface"


class FakeLab:
    """
    The FontLab program interface

    The main class. It is used via the pre-instantiated object `fl`.

    There is no explicit constructor for this class, use pre-initialized object 'fl'

    Always use "from FL import all" at the beginning of your macro.
    """

    __slots__ = [
        "_font",
        "_ifont",
        "_fonts",
        "ifontslist",
        "_glyph",
        "iglyph",
        "_tobject",
        "_iobject",
        "delta",
        "scale",
        "_tablet_active",
        "_tablet_pressure",
        "preview",
        "_layer",
    ]

    # Constructor

    def __init__(self) -> None:
        self._font: Font | None = None

        # (integer)  - index of currently active font
        self._ifont = -1

        self._fonts: list[Font] = []

        # (integer) - index of currently selected font in the fonts list panel
        self.ifontslist = 0

        self._glyph: Glyph | None = None

        # (integer)  - index of currently active glyph
        self.iglyph = -1

        # (integer)  - read-only - type of the currently selected object in the
        # Glyph Window
        self._tobject: int = -1

        # (integer)  - read-only - index of currently selected object in the
        # Glyph Window
        self._iobject = None

        # (<a href="Point.xml.html">Point</a>)  - delta value of current
        # coordinate translation in the active Glyph Window
        self.delta: Point | None = None

        # (<a href="Point.xml.html">Point</a>(float))      - scale value of
        # current coordinate translation in the active Glyph Window
        self.scale: Point | None = None

        # (boolean)   - True if tablet is present and active
        self._tablet_active = False

        # (integer) - current tablet's pen pressure
        self._tablet_pressure = 0

        # (string)          - contents of the preview panel <font color="red">
        # (not reported by docstring)</font>
        self.preview = ""

        self._layer: int | None = None

    # Operations

    def __len__(self) -> int:
        """
        returns number of opened fonts
        """
        return len(self._fonts)

    def __getitem__(self, index: int) -> Font:
        """
        returns Font by index
        """
        return self._fonts[index]

    # Attributes

    @property
    def font(self) -> Font | None:
        """
        Return the currently active font or None.
        """
        return self._font

    @property
    def ifont(self) -> int:
        """
        Return the index of the currently active font, or -1 if there is no font
        """
        return self._ifont

    @ifont.setter
    def ifont(self, value: int) -> None:
        self._ifont = value
        if self._ifont == -1:
            self._font = None
        else:
            self._font = self._fonts[self._ifont]

    @property
    def glyph(self) -> Glyph | None:
        """
        Return the currently active glyph in Font, Glyph or Metrics windows.
        """
        return self._glyph

    @property
    def tobject(self) -> int:
        """
        Return the type of the currently selected object in the Glyph Window as int.
        """
        # TODO: Actual return values

        # If there is no glyph window, raise:
        raise SystemError

    @property
    def iobject(self) -> int:
        """
        Return the index of currently selected object in the Glyph Window.
        """
        # TODO: Actual return values

        # If there is no glyph window, raise:
        raise SystemError

    @property
    def mainwindow(self) -> int:
        """
        Return a reference to FontLab's main window
        """
        return 0

    @property
    def path(self) -> str:
        """
        full path to directory where running application is located
        """
        return "/Library/Application Support/FontLab/Studio 5"

    @property
    def filename(self) -> str:
        """
        application filename
        """
        return "FontLab Studio 5 5730.app"

    @property
    def version(self) -> str:
        """
        application version
        """
        return "5.1.6/Mac(Build 7030)"

    @property
    def productnumber(self) -> int:
        """
        product number
        """
        return 0

    @property
    def serialnumber(self) -> str:
        """
        serial number as appears in the About window
        """
        return ""

    @property
    def username(self) -> str:
        """
        user name as appears in the About window
        """
        return "FontLab User"

    @property
    def count(self) -> int:
        """
        number of opened fonts (fast operation)
        """
        return self.__len__()

    @property
    def count_selected(self) -> int:
        """
        number of the selected glyphs in the Font Window (fast operation)
        """
        # FIXME
        return 0

    @property
    def window(self) -> int:
        """
        reference to the currently active Glyph, Font or Metrics window
        """
        # FIXME
        return 0

    # Properties not reported in the docs

    @property
    def layer(self) -> int | None:
        """
        Return the index of the currently active layer (master) in Glyph or Metrics
        windows.
        """
        return self._layer

    # Methods

    def Close(self, fontindex: int | None = None) -> None:
        """
        Close the current or `fontindex` font
        """
        if fontindex is None:
            del self._fonts[self._ifont]
        else:
            del self._fonts[fontindex]
        if self.count == 0:
            self.ifont = -1
        else:
            self.ifont = self.count - 1

    def Open(self, filename: str, addtolist: bool = True) -> None:
        """
        Open the font from file using current opening options. If `addtolist` is True,
        the font is added to FontLab's font list. The font is shown in a window.

        Args:
            filename (str): _description_
            addtolist (bool, optional): _description_. Defaults to True.

        `addtolist` seems to be ignored; the font window is always opened.
        If the file at the path is already opened, it will not be opened again.
        """
        open_paths = set([f.file_name for f in self._fonts])
        if filename in open_paths:
            return

        # Try to open the font as VFB:
        font = Font()
        result = font.Open(filename)
        if result == 0:
            # Was not a VFB, try to import it
            fi = FontImporter(Path(filename), options=Options())
            try:
                font = fi.import_font()
            except ValueError:
                return
        self.Add(font)

    def Save(
        self, filename_or_fontindex: str | int, filename: str | None = None
    ) -> None:
        """
        (string filename) | (int fontindex, string filename)

        Save the current or selected font using standard FontLab's Save
        routine.
        """
        if isinstance(filename_or_fontindex, int):
            # Save the font fontindex
            fontindex = filename_or_fontindex
            if 0 <= fontindex < self.count:
                if filename is None:
                    raise RuntimeError
                self._fonts[fontindex].Save(filename)
        else:
            # Save the current font
            if self.font is not None:
                filename = filename_or_fontindex
                self.font.Save(filename)

    def GenerateFont(self, *args: Any) -> int:
        """
        Generate a Font.

        Args:
            fontindex_or_fonttype (int): The index of the font to be generated, or the
                font type, see below.
            fonttype (int): The font type, see below.
            filename (str): The path for the font to be generated.

        Returns:
            int: 0 on success, -1 if the font was not generated.

        Available font types:

        ftFONTLAB
            FontLab VFB font
        ftTYPE1
            PC Type 1 font (binary/PFB)
        ftTYPE1_MM
            PC MultipleMaster font (PFB)
        ftTYPE1ASCII
            PC Type 1 font (ASCII/PFA)
        ftTYPE1ASCII_MM
            PC MultipleMaster font (ASCII/PFA)
        ftTRUETYPE
            PC TrueType/TT OpenType font (TTF)
        ftOPENTYPE
            PS OpenType (CFF-based) font (OTF)
        ftMACTYPE1
            Mac Type 1 font (generates suitcase and LWFN file, optionally AFM)
        ftMACTRUETYPE
            Mac TrueType font (generates suitcase)
        ftMACTRUETYPE_DFONT
            Mac TrueType font (generates suitcase with resources in data fork)
        """
        try:
            from ufo2ft import compileOTF, compileTTF
            from vfbLib.ufo.builder import VfbToUfoBuilder

            can_generate = True
        except ImportError:
            can_generate = False

        if len(args) == 3:
            fontindex, fonttype, filename = args
        elif len(args) == 2:
            fonttype, filename = args
            fontindex = self.ifont
        else:
            raise RuntimeError(
                "Incorrect # of args to:\nFontLab.GenerateFont([Int fontindex,] Int "
                "format, String filename)"
            )

        # An invalid font index was requested, or there is no open font
        if fontindex == -1:
            raise RuntimeError

        font = self._fonts[fontindex]

        if can_generate:
            # At the moment, we jump through some hoops. The font must have been opened
            # from a VFB file, and we need to build an UFO in memory to generate.
            builder = VfbToUfoBuilder(
                font.fake_vfb_object, add_kerning_groups=True, move_groups=True
            )
            # TODO: What if it is MM? Probably intepolate the default instance.
            ufo = builder.get_ufo_masters()[0]
            if fonttype == ftOPENTYPE:
                font = compileOTF(
                    ufo,
                    cffVersion=1,
                    inplace=True,
                    # layerName=,
                    optimizeCFF=2,
                    skipExportGlyphs=False,
                )
                font.save(filename)
                return 0
            elif fonttype == ftTRUETYPE:
                # TODO: For TTF, compile UFO hinting
                font = compileTTF(
                    ufo,
                    removeOverlaps=False,
                    flattenComponents=False,  # FL only has one level of components
                    # convertCubics=,
                    # cubicConversionError=,
                    # layerName=,
                    skipExportGlyphs=False,
                    dropImpliedOnCurves=False,
                    allQuadratic=True,
                )
                font.save(filename)
                return 0
            elif fonttype == ftFONTLAB:
                # What's the difference to just saving the VFB? Probably interpolating
                # the default instance?
                # TODO: Verify and interpolate
                font.Save(filename)
                return 0

        else:
            # We cannot generate a font at the moment, let's fake it.
            # Check if the current font has a fake_binary.
            binary = font.fake_binary_get(fonttype)
            if binary:
                with open(filename, "wb") as f:
                    f.write(binary)
                return 0

        return -1

    def Add(self, font: Font) -> None:
        """
        Add 'font' to list of opened fonts and open the Font Window for it.
        """
        self._fonts.append(font)
        self.ifont = len(self._fonts) - 1
        # As long as no glyph window is open,
        # delta and scale will be points at (0, 0)
        self.delta = Point()
        self.scale = Point()
        self._layer = 0

    def UpdateFont(self, fontindex: int | None = None) -> None:
        """
        Updates current font or 'fontindex' (slow operation)
        """
        if fontindex is None:
            fontindex = self.ifont
        self._fonts[fontindex].fake_update()

    def SetFontWindow(
        self, fontindex: int, position: Rect, state: int | None = None
    ) -> None:
        """
        Set the window size and style for the Font Window where font 'fontindex' is
        shown.

        Args:
            fontindex (int): The font index.
            position (Rect): The position and size of the window.
            state (int | None, optional): The window state.
                0 = normal, 1 = minimized, 2 = maximized. Defaults to None.
        """
        raise NotImplementedError

    def UpdateGlyph(self, glyphindex: int | None = None) -> None:
        """
        Update the current glyph or 'glyphindex' glyph of the current font
        """
        raise NotImplementedError

    def EditGlyph(self, glyphindex: int | None = None) -> None:
        """
        Open the Glyph window for the 'glyphindex' glyph in the current font
        """
        raise NotImplementedError

    def CallCommand(self, commandcode: int) -> None:
        """
        Simulate a menu or toolbar command. Check WS_* constants for list of available
        commands.
        """
        raise NotImplementedError

    def Selected(self, glyphindex: int | None = None) -> int:
        """
        Return 1 if current glyph or 'glyphindex' glyph is selected.
        """
        if self.font is None:
            return 0

        if glyphindex is None:
            raise NotImplementedError
            # return 1 if fl.glyph.selected

        if glyphindex in self.font._selection:
            return 1

        return 0

    def Select(self, glyphid: str | Uni | int, value: bool | None = None) -> None:
        """
        Change a glyph's selection state. 'glyphid' may be string (glyph name), Uni
        (Unicode index) or integer (glyph index)

        Args:
            glyphid (str | Uni | int): The glyph identifier.
            value (bool | None, optional): The selection state. Defaults to None. None
                is interpreted as True.

        Raises:
            RuntimeError: If no font is opened.
        """
        if self.font is None:
            raise RuntimeError(
                "No font is available to perform operation: FontLab.Select()"
            )
        if isinstance(glyphid, str):
            glyphid = self.font.FindGlyph(glyphid)
        if value is None:
            value = True
        self.font.fake_select(glyphid, value)

    def Unselect(self) -> None:
        """
        Deselect all glyphs in the current font (fast operation).
        """
        if self.font is None:
            raise RuntimeError(
                "No font is available to perform operation: FontLab.Unselect()"
            )
        self.font.fake_deselect_all()

    def Message(
        self,
        message: str,
        question: str | None = None,
        okstring: str | None = None,
        cancelstring: str | None = None,
    ) -> int:
        """
        Show an alert message dialog box. All parameters but the first can be omitted.

        Args:
            message (str): The message.
            question (str | None, optional): The question text. Defaults to None.
            okstring (str | None, optional): The label of the OK button. Defaults to
                None.
            cancelstring (str | None, optional): The label of the Cancel button.
                Defaults to None.

        Returns:
            int: 1 if the OK button was clicked, 2 if the Cancel button was clicked or
                the window has been closed.
        """
        raise NotImplementedError

    def ScreenToGlyph(self, position: Point) -> Point:
        """
        Converts the screen coordinates of the point to glyph coordinates in the current
        Glyph Window.
        """
        raise NotImplementedError

    def GlyphToScreen(self, position: Point) -> Point:
        """
        Converts the glyph coordinates of the point to screen coordinates in the current
        Glyph Window.
        """
        raise NotImplementedError

    def UpdateRect(self, r: Rect) -> None:
        """
        Updates the rectangle r in the current Glyph Window.
        """
        raise NotImplementedError

    def HitContour(self, p: Point) -> tuple[int, int, float] | None:
        """
        Contour hit detection in the current Glyph Window.

        Args:
            p (Point): The point to use for hit detection.

        Returns:
            tuple[int, int, float] | None : (nodeindex, nodesubindex, hit_time), or None
                if the point doesn't hit any contour.

        Raises:
            RuntimeError: If the current window is not a Glyph Window.
            RuntimeError: If no window is open.
        """
        # RuntimeError: No window is opened: FontLab.HitContour(Point)
        # RuntimeError: Current window is not Glyph window: FontLab.HitContour(Point)
        raise NotImplementedError

    def GetCanvas(self) -> Canvas:
        """
        Return a :py:class:`Canvas` for the current Glyph Window.
        """
        raise RuntimeError("Current window is not Glyph window: FontLab.GetCanvas()")

    def GetConvert(self, c: Canvas) -> None:
        """
        Copy conversion parameters from the current Glyph Window to the `Canvas`.
        """
        raise NotImplementedError

    def BeginProgress(self, title: str, counts: int) -> None:
        """
        Open a Progress dialog box with 'counts' number of 'ticks'.
        """
        raise NotImplementedError

    def TickProgress(self, tick: int) -> bool:
        """
        Update the Progress bar, return False if the Cancel button was pressed.
        This is a relatively 'expensive' operation.
        """
        raise NotImplementedError

    def EndProgress(self) -> None:
        """
        Close the Progress dialog box.
        """
        raise NotImplementedError

    def Random(self, lovalue: float, hivalue: float | None = None) -> int:
        """
        (hivalue) | (lovalue, hivalue)

        - returns random value (fast operation)
        """
        # lovalue and hivalue are truncated to int before finding the random number
        # int(lovalue) <= n < int(hivalue)
        raise NotImplementedError

    def TransformGlyph(self, glyph: Glyph, code: int, text: str) -> None:
        """
        Transforms the glyph using one of the Transform actions.

        Save one of Transform Range programs for reference to format of the command
        string.
        """
        raise NotImplementedError

    def ForSelected(self, function: Callable[[Font, Glyph, int], None]) -> None:
        """
        Call `function` for each selected glyph in the current font. The function has
        the following format:

        function(font: Font, glyph: Glyph, glyphindex: int)
        """
        if self.font is None:
            return

        for glyphindex, glyph in enumerate(self.font.glyphs):
            function(self.font, glyph, glyphindex)

    def SetUndo(self) -> None:
        """
        Save the current state to the undo buffer.
        """
        raise NotImplementedError

    # Additional methods reported by dir(fl)

    def GetFileName(
        self,
        open_save: int,
        suffix: str | None = None,
        filename: str | None = None,
        filetype: str | None = None,
    ) -> str:
        """
        Open a file picker dialog.

        Args:
            open_save (int): 0 for a Save dialog, 1 for an Open dialog.
            suffix (str | None, optional): The suggested file suffix. Ignored in Open
                dialogs. Defaults to None.
            filename (str | None, optional): The suggested file name. Defaults to None.
            filetype (str | None, optional): The suggested file type. Defaults to None.

        Returns:
            str: The path of the selected file.
        """
        raise NotImplementedError

    def GetPathName(self, title: str, message: str) -> str:
        """
        Show a folder picker.

        Args:
            title (str): The title of the dialog.
            message (str): The message of the dialog

        Returns:
            str: The path of the selected folder.
        """
        raise NotImplementedError

    def LoadNamFile(self, namfilename: str) -> None:
        raise NotImplementedError

    def Lock(self, lock: bool) -> None:
        raise NotImplementedError

    def OpenFont(self, filename: str) -> Font | None:
        """
        Open a VFB file, or import a font from path `filename`. If successful, the
        `Font` is returned. The font is not added as a visible Window.

        Args:
            filename (str): The path to the VFB or font.

        Returns:
            Font | None: The font, or None if the file could not be opened.
        """
        font = Font()
        try:
            font.Open(filename)
        except:  # noqa: E722
            return None
        return font

    def _setcurrentfont(self, *args: int) -> None:
        """
        This seems to have no effect
        """
        if len(args) != 1:
            raise RuntimeError("Incorrect # of args to: FontLab._setcurrentfont()")
        if not isinstance(args[0], int):
            raise RuntimeError(
                "Number is expected in arg 1: FontLab._setcurrentfont(Font font)"
            )
