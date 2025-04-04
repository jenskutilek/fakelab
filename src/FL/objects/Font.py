from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from FL.fake.Font import FakeFont
from FL.helpers.classList import ClassList
from FL.helpers.ListParent import ListParent
from FL.objects.Encoding import Encoding
from FL.objects.TTInfo import TTInfo

if TYPE_CHECKING:
    from FL.objects import Guide, NameRecord, TrueTypeTable
    from FL.objects.Feature import Feature
    from FL.objects.Glyph import Glyph


class Font(FakeFont):
    def __init__(
        self,
        font_or_path: Font | str | None = None,
        instances: tuple[float, float, float, float] | None = None,
    ) -> None:
        super().__init__()
        self._set_defaults()

        # Process params

        if isinstance(font_or_path, Font):
            if instances is None:
                # Copy constructor
                raise NotImplementedError
            else:
                # Generate an instance
                # instances is a tuple containing instance values for all MM
                # axes defined in the font
                raise NotImplementedError
        elif isinstance(font_or_path, str) or isinstance(font_or_path, Path):
            # Instantiate with path
            self.Open(font_or_path)

        # else: Empty font

    def __repr__(self) -> str:
        return "<Font: '%s', %i glyphs>" % (self.full_name, len(self))

    # Attributes

    @property
    def file_name(self) -> str:
        """
        Full path of the file from which the font was opened/saved.
        """
        # The file path is stored internally as Path, but we return a str
        return str(self._file_name)

    @property
    def axis(self) -> list[tuple[str, str, str]]:
        """
        Array of font axes. Not reported by docstring nor e-font.

        Example: [('Weight', 'Wt', 'Weight')]
        """
        return self._axis

    @property
    def classes(self) -> list[str]:
        """
        List of glyph classes.
        """
        return list(self._classes)

    @classes.setter
    def classes(self, value: list[str]) -> None:
        # Carry over the flags when setting the value
        self._classes: ClassList = ClassList(value, self._classes)

    @property
    def encoding(self) -> Encoding:
        """
        Current encoding of the font.
        """
        return self._encoding

    @property
    def features(self) -> ListParent[Feature]:
        """
        List of Opentype features.
        """
        return self._features

    @features.setter
    def features(self, value) -> None:
        raise RuntimeError

    @property
    def fontnames(self) -> ListParent[NameRecord]:
        """
        List of font name records.
        """
        return self._fontnames

    @fontnames.setter
    def fontnames(self, value) -> None:
        raise RuntimeError

    @property
    def glyphs(self) -> ListParent[Glyph]:
        """
        Return the array of glyphs.
        """
        # Read-only.
        return self._glyphs

    @glyphs.setter
    def glyphs(self, value) -> None:
        raise RuntimeError

    @property
    def truetypetables(self) -> ListParent[TrueTypeTable]:
        """
        List of custom TrueType tables.
        """
        # Read-only.
        return self._truetypetables

    @truetypetables.setter
    def truetypetables(self, value) -> None:
        raise RuntimeError

    # Operations

    def __len__(self) -> int:
        """
        Return the number of glyphs.
        """
        return len(self._glyphs)

    def __getitem__(self, index: int | str) -> Glyph | None:
        """
        Accesses glyphs array
        """
        if isinstance(index, str):
            # We got a glyph name
            for glyph in self._glyphs:
                if glyph.name == index:
                    return glyph
            return None

        return self._glyphs[index]

    # Methods

    def New(self) -> None:
        """
        clears the font
        """
        raise NotImplementedError

    def Open(self, filename: str | Path) -> None:
        """
        opens font from VFB format
        """
        from FL.vfb.reader import VfbToFontReader

        self._set_file_name(filename)
        VfbToFontReader(Path(filename), self)

    def Save(self, filename: str | Path) -> None:
        """
        saves font in VFB format
        """
        from FL.vfb.writer import FontToVfbWriter

        self._set_file_name(filename)
        FontToVfbWriter(self, Path(filename))

    def OpenAFM(self, filename: str | Path, mode: int, layer: int) -> None:
        """
        open AFM-File, mode is the integer bit field.
          The bit list is:
          ALLMETRICS       - 0x0001
          THICKERMETRICS   - 0x0002
          WIDERMETRICS     - 0x0004
          CLOSEMETRICS     - 0x0008
          REPLACEKERNING   - 0x0010
          ADDKERNING       - 0x0020
          AUTOKERNING      - 0x0040
          REPLACEOTHERDATA - 0x0100
          REPLACENAMES     - 0x0200

          Constants for mode (only in FL 4.5 Mac)
          mtALLMETRICS
          mtTHICKERMETRICS
          mtWIDERMETRIC
          mtCLOSEMETRICS
          mtREPLACEKERNING
          mtADDKERNING
          mtAUTOKERNING
          mtREPLACEOTHERDATA
          mtREPLACENAMES
        """
        raise NotImplementedError

    def SaveAFM(self, filename: str | Path) -> None:
        """
        saves AFM- and INF-File (this method is not reported by the docstring)
        """
        raise NotImplementedError

    def Reencode(self, e: Encoding, style: int = 0) -> None:
        """
        applies Encoding to Font (the parameters of this method are not reported by the
        docstring and i don't know what the style parameter does)
        """
        raise NotImplementedError

    def FindGlyph(self, name_unicode_uniint: str | int) -> int:
        """
        (string name) | (Uni unicode) | (integer Unicode)
        - finds glyph and return its index or -1
        """
        if isinstance(name_unicode_uniint, str):
            # name
            for i, g in enumerate(self._glyphs):
                if g.name == name_unicode_uniint:
                    return i
            return -1
        elif isinstance(name_unicode_uniint, int):
            # int (unicode value)
            for i, g in enumerate(self._glyphs):
                if name_unicode_uniint in g.unicodes:
                    return i
            return -1
        else:
            # What is Uni supposed to be? I don't know
            raise TypeError

    def DefineAxis(self, name: str, type: str, shortname: str) -> None:
        """
        Defines a new Multiple Master axis.

        :param name: Name
        :type name:  str

        :param name: Type
        :type name:  str

        :param name: ShortName
        :type name:  str
        """
        raise NotImplementedError

    def DeleteAxis(self, axisindex: int, position: float) -> None:
        """
        Removes the axis
        """
        raise NotImplementedError

    def GenerateUnicode(self) -> None:
        """
        Generates Unicode indexes for all glyphs
        """
        raise NotImplementedError

    def GenerateNames(self) -> None:
        """
        Generates names for all glyphs
        """
        raise NotImplementedError

    def GenerateGlyph(self, glyphname: str) -> Glyph:
        """
        Generates new glyph using 'glyphname' as a source of information about glyph's
        composition. See 'FontLabDir/Mapping/alias.dat' for composition definitions
        """
        # The glyph is not added to the font automatically
        glyph = Glyph()
        glyph.name = glyphname
        return glyph

    def has_key(self, name_unicode_uniint: str | int) -> int:
        """
        (string name) | (Uni unicode) | (integer Unicode)
        - finds glyph and return 1 (found) or 0 (not found)
          <font color="red">(this method is not reported by the docstring)</font>
        """
        glyph_index = self.FindGlyph(name_unicode_uniint)
        if glyph_index == -1:
            return 0
        return 1

    def GenerateFont(self, fontType: int, filename: str | Path) -> None:
        """
        (fontType, filename)
        - generates Font, see <a href="FontLab.xml.html">FontLab</a> class for
          description. <font color="red">(As a method of the Font class, this
          method is deprecated. Since FontLab 4.52 for Mac
          and FontLab 4.53 for Windows, GenerateFont is a method
          of the FontLab class)</font>
        """
        # In FL 5, this raises an AttributeError
        raise AttributeError

    # Undocumented methods

    def MakeKernFeature(self, vector: list[float]) -> None:
        """
        [WeightVector vector]
        - generates 'kern' feature using font kerning and classes
        """
        raise NotImplementedError

    def MergeFonts(self, source: Font, flags: int | None = None) -> None:
        """
        (Font source[, flags])
        - appends all glyphs from the source font. Check mfXXXX constants for
        options
        """
        raise NotImplementedError

    def SetClassFlags(
        self,
        class_index: int,
        left_lsb: bool,
        right_rsb: bool,
        width: bool | None = None,
    ) -> None:
        """
        (int class_index, bool left, bool right)
        - allows to set 'left' and 'right' properties of the kerning class

        (int class_index, bool lsb, bool rsb, bool width)
        - allows to set 'lsb', 'rsb' and 'width' properties of the metrics class
        """
        self._classes.SetClassFlags(class_index, left_lsb, right_rsb, width)

    def GetClassLeft(self, class_index: int) -> int | None:
        """
        (int class_index)
        - returns the 'left' property of the class
        """
        return self._classes.GetClassLeft(class_index)

    def GetClassRight(self, class_index: int) -> int | None:
        """
        (int class_index)
        - returns the 'right' property of the class
        """
        return self._classes.GetClassRight(class_index)

    def GetClassMetricsFlags(self, class_index: int) -> tuple | None:
        """
        (int class_index)
        - returns the tuple containing LSB, RSB and Width flags of the metrics
        class
        """
        return self._classes.GetClassMetricsFlags(class_index)

    # Additional methods reported by dir(fl.font)

    def GenerateInstance(self) -> None:
        raise NotImplementedError

    # Defaults

    def _set_defaults(self) -> None:
        # Identification

        # full path of the file from which the font was opened/saved
        self._file_name = None
        # font Family Name
        self.family_name: str | None = None
        # font Style Name
        self.style_name: str | None = None
        # font Full Name
        self.full_name: str | None = None
        # font Font Name
        self.font_name: str | None = None

        # Font Style as BitList:
        # italic       =  1
        # underscored  =  2
        # negative     =  4
        # outlined     =  8
        # strikethough = 16
        # bold         = 32
        self.font_style: int = 64

        self.menu_name: str | None = None
        # FOND Name
        self.apple_name: str = ""
        # FOND ID
        self.fond_id: int = 128
        # OpenType-specific font Family Name
        self.pref_family_name: str | None = None
        # OpenType-specific font Style Name
        self.pref_style_name: str | None = None
        # OpenType-specific font Mac Name
        self.mac_compatible: str | None = None
        # glyph name that represents the PFM default
        self.default_character: str | None = None
        self.weight = None
        self.weight_code = -1
        self.width = "normal"
        self.designer: str | None = None

        # up until here the default values have been verified
        self.designer_url: str = ""
        # list of font name records
        self._fontnames: ListParent[NameRecord] = ListParent(parent=self)
        # Copyright name field
        self.copyright: str = ""
        # Notice field
        self.notice: str = ""
        # Font note
        self.note: str = ""
        # Type 1 Unique ID number
        self.unique_id: int = 0
        # TrueType Unique ID record
        self.tt_u_id: str = ""
        # TrueType Version record
        self.tt_version: str = ""
        self.trademark: str = ""
        self.x_u_id_num: int = 0
        self.x_u_id: str = ""
        # TrueType vendor code
        self.vendor: str = ""
        self.vendor_url: str = ""
        self.version: str = ""
        self.year: int = 0
        self.version_major: int = 0
        self.version_minor: int = 0
        self.vp_id: int = 0
        self.ms_charset: int = 0
        self.ms_id: int = 0
        # list of Panose values
        self.panose: list[int] = []
        self.pcl_chars_set: str = ""
        self.pcl_id: int = 0

        #  Dimensions
        self.upm: int = 1000
        # list of ascenders, one for each master
        self.ascender: list[int] = []
        # list of descenders, one for each master
        self.descender: list[int] = []
        # list of CapHeight records, one for each master
        self.cap_height: list[int] = []
        # list of xHeight values, one for each master
        self.x_height: list[int] = []
        self.default_width: int = 0
        self.slant_angle: int = 0
        # Italic Angle
        self.italic_angle: float = 0.0
        self.is_fixed_pitch: bool = False
        self.underline_position: int = 0
        self.underline_thickness: int = 0

        #  Alignment
        self.blue_fuzz: int = 0
        self.blue_scale: int = 0
        self.blue_shift: int = 0
        # number of defined blue values
        self.blue_values_num: int = 0
        # two-dimentional array of BlueValues
        # master index is top-level index
        self.blue_values: list[list[int]] = [[]]
        # number of defined OtherBlues values
        self.other_blues_num: int = 0
        # two-dimentional array of OtherBlues
        # master index is top-level index
        self.other_blues: list[list[int]] = [[]]
        # number of FamilyBlues records
        self.family_blues_num = 0
        # two-dimentional array of FamilyBlues
        # master index is top-level index
        self.family_blues: list[list[int]] = [[]]
        # number of FamilyOtherBlues records
        self.family_other_blues_num: int = 0
        # two-dimentional array of FamilyOtherBlues
        # master index is top-level index
        self.family_other_blues: list[list[int]] = [[]]
        # list of Force Bold values, one for each master
        self.force_bold: list[int] = [0]
        self.stem_snap_h_num: int = 0
        self.stem_snap_h: list[list[int]] = [[]]
        self.stem_snap_v_num: int = 0
        self.stem_snap_v: list[list[int]] = [[]]

        #  Other

        # 0 if unmodified, 1 if modified (to control the
        # 'save changes' dialog) <font color="red">(this attribute is not
        # reported by the docstring)</font>
        self.modified: int = 0
        # list of glyph classes
        self._classes = ClassList()
        # string containing the OT classes defined in the lower
        # right part of the OpenType panel <font color="red">(this description
        # is not reported by the docstring)</font>
        self.ot_classes: str = ""
        # list of OpenType features
        self._features: ListParent[Feature] = ListParent(parent=self)
        # font custom data field
        self.customdata: str = ""
        # list of custom TrueType tables
        self._truetypetables: ListParent[TrueTypeTable] = ListParent(parent=self)
        # loaded TrueType information
        # (mostly hinting-related tables)
        self.ttinfo = TTInfo()
        # current encoding of the font, read-only
        self._encoding = Encoding()
        self._encoding._parent = self
        self._encoding.load_font_default()
        # list of codepage-numbers (see OT-specs)
        # <font color="red">(this attribute is not reported by the docstring
        # this attribute is linked with the
        # ttinfo.os2_ul_code_page_range1 and
        # ttinfo.os2_ul_code_page_range2 values)</font>
        self.codepages: list[int] = []
        # list of unicoderange-numbers (see OT-specs)
        # <font color="red">(this attribute is not reported by the docstring)</font>
        self.unicoderanges: list[int] = []
        # the Created By field
        # <font color="red">(this description is not reported by the docstring)</font>
        self.source = None
        # list of MM-settings for generate instance
        self.weight_vector: list[float] = []
        # list of horizontal guides
        # <font color="red">(new in v4.5.4 and not reported by docstring)</font>
        self.hguides: list[Guide] = []
        # list of vertical guides
        # <font color="red">(new in v4.5.4 and not reported by docstring)</font>
        self.vguides: list[Guide] = []

        self._axis: list[tuple[str, str, str]] = []
        self._glyphs: ListParent[Glyph] = ListParent(parent=self)

        # Font data that is not accessible via FL5 Python API
        self._masters_count: int = 1
        self._license: str = ""
        self._license_url: str = ""
