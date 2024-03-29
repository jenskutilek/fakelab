from __future__ import annotations

import codecs
import json

from .TTInfo import TTInfo


class Font(object):
    def __init__(self, font_or_path=None, instances=None):
        self.set_defaults()

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
        elif isinstance(font_or_path, str):
            # Instantiate with path
            self._file_name = font_or_path
        # else: Empty font

    def __repr__(self):
        return "<Font: '%s', %i glyphs>" % (self.full_name, len(self))

    # Additions for FakeLab

    def fake_binary_get(self, fontType: int) -> bytes:
        binary_path = self._fake_binaries[str(fontType)]
        with open(binary_path, "rb") as f:
            binary = f.read()
        return binary
    
    def fake_binary_from_path(self, fontType: int, file_path: str) -> None:
        """
        Assign a binary file from a path. This will be used to fake the
        FakeLab.GenerateFont() method.
        """
        # Convert key to str because JSON needs it
        self._fake_binaries[str(fontType)] = file_path

    def fake_save(self, fp, sparse=True):
        if sparse:
            font_dict = {
                k: v
                for k, v in self.__dict__.items()
                if k not in (
                    "_file_name",
                    "fake_sparse_json",
                    "_selection",
                ) and v
            }

            def sub_dict(obj):
                return {
                    k: v
                    for k, v in obj.__dict__.items()
                    if k not in (
                        "_parent",
                    )
                }

        else:
            font_dict = {
                k: v
                for k, v in self.__dict__.items()
                if k not in (
                    "_file_name",
                    "fake_sparse_json",
                    "_selection",
                ) and v
            }

            def sub_dict(obj):
                return {
                    k: v
                    for k, v in obj.__dict__.items()
                    if k not in (
                        "_parent",
                    ) and v
                }

        json.dump(
                obj=font_dict,
                fp=fp,
                default=lambda o: sub_dict(o),
                indent=4
            )

    def fake_update(self):
        """
        Is called from FontLab.UpdateFont()
        """
        for index, glyph in enumerate(self.glyphs):
            glyph.fake_update(self, index)

    def fake_deselect_all(self):
        """
        Deselect all glyphs. Is called from FontLab.Unselect().
        """
        self._selection = set()

    def fake_select(self, glyph_index, value=None):
        """
        Change selection status for glyph_index.
        >>> f = Font()
        >>> f.fake_select(1, False)
        >>> print(f._selection)
        set()
        >>> f.fake_select(1, True)
        >>> print(f._selection)
        {1}
        >>> f.fake_select(3, True)
        >>> print(f._selection)
        {1, 3}
        >>> f.fake_select(2, False)
        >>> print(f._selection)
        {1, 3}
        >>> f.fake_select(1, False)
        >>> print(f._selection)
        {3}
        """
        if value:
            self._selection |= {glyph_index}
        else:
            self._selection -= {glyph_index}

    # Attributes

    @property
    def file_name(self):
        return self._file_name

    @property
    def axis(self):
        """
        Array of font axes. Not reported by docstring nor e-font.

        Example: [('Weight', 'Wt', 'Weight')]
        """
        return self._axis

    @property
    def glyphs(self):
        """
        Return the array of glyphs.
        """
        return self._glyphs

    # Operations

    def __len__(self):
        """
        Return the number of glyphs.
        """
        return len(self._glyphs)

    def __getitem__(self, index):
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

    def New(self):
        """
        clears the font
        """
        raise NotImplementedError

    def Open(self, filename: str):
        """
        opens font from VFB format
        """
        self._file_name = filename
        with codecs.open(self._file_name, "rb", "utf-8") as f:
            _dict = json.load(f)
        self._fake_binaries = _dict.get("_fake_binaries", {})
        # TODO: Read the rest of the font

    def Save(self, filename: str):
        """
        saves font in VFB format

        Saving VFB is not supported in FakeLab, but we can write a nice JSON
        format.
        """
        with codecs.open(filename, "wb", "utf-8") as f:
            self.fake_save(f, self.fake_sparse_json)
            self._file_name = filename

    def OpenAFM(self, filename: str, mode: int, layer: int):
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

    def SaveAFM(self, filename: str):
        """
        saves AFM- and INF-File (this method is not reported by the docstring)
        """
        raise NotImplementedError

    def Reencode(self, e: Encoding, style: int = 0):
        """(<a href="Encoding.xml.html">Encoding</a> E)|(<a href="Encoding.xml.html">Encoding</a> E, integer style)
        - applies <a href="Encoding.xml.html">Encoding</a> E to Font
          <font color="red">(the parameters of this method are not
          reported by the docstring and i don't
          know what the style parameter does)</font>
        """
        raise NotImplementedError

    def FindGlyph(self, name_unicode_uniint):
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

    def DefineAxis(self, name, type, shortname):
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

    def DeleteAxis(self, axisindex, position):
        """
        (axisindex, float position)
        - removes the axis
        """
        raise NotImplementedError

    def GenerateUnicode(self):
        """
        - generates Unicode indexes for all glyphs
        """
        raise NotImplementedError

    def GenerateNames(self):
        """
        - generates names for all glyphs
        """
        raise NotImplementedError

    def GenerateGlyph(self, glyphname):
        """(string glyphname)
        - generates new glyph using 'glyphname' as
          a source of information about glyph's composition
          see 'FontLabDir/Mapping/alias.dat' for composition
          definitions
        """
        raise NotImplementedError

    def has_key(self, name_unicode_uniint):
        """
        (string name) | (Uni unicode) | (integer Unicode)
        - finds glyph and return 1 (found) or 0 (not found)
          <font color="red">(this method is not reported by the docstring)</font>
        """
        raise NotImplementedError

    def GenerateFont(self, fontType, filename):
        """
        (fontType, filename)
        - generates Font, see <a href="FontLab.xml.html">FontLab</a> class for
          description. <font color="red">(As a method of the Font class, this 
          method is deprecated. Since FontLab 4.52 for Mac 
          and FontLab 4.53 for Windows, GenerateFont is a method 
          of the FontLab class)</font>
        """
        raise NotImplementedError
    
    # Undocumented methods

    def MakeKernFeature(self, vector):
        """
        [WeightVector vector]
        - generates 'kern' feature using font kerning and classes
        """
        raise NotImplementedError
    
    def MergeFonts(self, source: Font, flags=None):
        """
        (Font source[, flags])
        - appends all glyphs from the source font. Check mfXXXX constants for
        options
        """
        raise NotImplementedError

    def SetClassFlags(self, class_index: int, left: int, right: int, width=None) -> None:
        """
        (int class_index, bool left, bool right)
        - allows to set 'left' and 'right' properties of the kerning class

        (int class_index, bool lsb, bool rsb, bool width)
        - allows to set 'lsb', 'rsb' and 'width' properties of the metrics class
        """
        raise NotImplementedError
    
    def GetClassLeft(self, class_index: int) -> int:
        """
        (int class_index)
        - returns the 'left' property of the class
        """
        raise NotImplementedError
    
    def GetClassRight(self):
        """
        (int class_index)
        - returns the 'right' property of the class
        """
        raise NotImplementedError

    def GetClassMetricsFlags(self, class_index: int) -> tuple:
        """
        (int class_index)
        - returns the tuple containing LSB, RSB and Width flags of the metrics
        class
        """
        raise NotImplementedError

    # Defaults

    def set_defaults(self):
        # Additions for FakeLab

        self._fake_binaries = {}
        self.fake_sparse_json = True
        self.fake_deselect_all()

        # Identification

        self._file_name = None      # full path of the file from which the font was opened/saved
        self.family_name = None     # font Family Name
        self.style_name = None      # font Style Name
        self.full_name = None       # font Full Name
        self.font_name = None       # font Font Name
        # Font Style as BitList:
        # italic       =  1
        # underscored  =  2
        # negative     =  4
        # outlined     =  8
        # strikethough = 16
        # bold         = 32
        self.font_style = 64
        self.menu_name = None

        self.apple_name = ""            # (string)       - FOND Name
        self.fond_id = 128              # (int)             - FOND ID
        self.pref_family_name = None    # (string) - OpenType-specific font Family Name
        self.pref_style_name = None     # (string)  - OpenType-specific font Style Name
        self.mac_compatible = None      # (string)   - OpenType-specific font Mac Name
        self.default_character = None   # (string)- glyph name that represents the PFM default
        self.weight = None
        self.weight_code = -1
        self.width = "normal"
        self.designer = None            # (string)

        # up until here the default values have been verified
        self.designer_url = ""          # (string)
        self.fontnames = []             # [<a href="NameRecord.xml.html">NameRecord</a>]    - list of font name records
        self.copyright = ""             # (string)        - Copyright name field
        self.notice = ""                # (string)           - Notice field
        self.note = ""                  # (string)             - Font note
        self.unique_id = 0              # (integer)       - Type 1 Unique ID number
        self.tt_u_id = ""               # (string)          - TrueType Unique ID record
        self.tt_version = ""            # (string)       - TrueType Version record
        self.trademark = ""             # (string)
        self.x_u_id_num = 0
        self.x_u_id = ""
        self.vendor = ""                # (string)           - TrueType vendor code
        self.vendor_url = ""            # (string)
        self.version = ""               # (string)
        self.year = 0                   # (integer)
        self.version_major = 0          # (integer)
        self.version_minor = 0          # (integer)
        self.vp_id = 0                  # (integer)
        self.ms_charset = 0             # (integer)
        self.ms_id = 0                  # (integer)
        self.panose = []                # [integer]         - list of Panose values
        self.pcl_chars_set = ""         # (string)
        self.pcl_id = 0                 # (integer)

        #  Dimensions
        self.upm = 1000
        self.ascender = []              # [integer]   - list of ascenders, one for each master
        self.descender = []             # [integer]  - list of descenders, one for each master
        self.cap_height = []            # [integer] - list of CapHeight records, one for each master
        self.x_height = []              # [integer]   - list of xHeight values, one for each master
        self.default_width = 0
        self.slant_angle = 0
        self.italic_angle = 0.0         # (float) - Italic Angle
        self.is_fixed_pitch = False
        self.underline_position = 0     # (integer)
        self.underline_thickness = 0    # (integer)

        #  Alignment
        self.blue_fuzz = 0
        self.blue_scale = 0
        self.blue_shift = 0
        self.blue_values_num = 0        # (integer)             - number of defined blue values
        self.blue_values = [[]]         # [integer[integer]]        - two-dimentional array of BlueValues
        #                                         master index is top-level index

        self.other_blues_num = 0        # (integer)             - number of defined OtherBlues values
        self.other_blues = [[]]         # [integer[integer]]        - two-dimentional array of OtherBlues
        #                                         master index is top-level index

        self.family_blues_num = 0       # (integer)            - number of FamilyBlues records
        self.family_blues = [[]]        # [integer[integer]]       - two-dimentional array of FamilyBlues
        #                                         master index is top-level index

        self.family_other_blues_num = 0  # (integer)      - number of FamilyOtherBlues records
        self.family_other_blues = [[]]   # [integer[integer]] - two-dimentional array of FamilyOtherBlues
        #                                         master index is top-level index

        self.force_bold = 0             # [integer]                  - list of Force Bold values, one for 
        #                                         each master
        self.stem_snap_h_num = 0        # (integer)
        self.stem_snap_h = [[]]
        self.stem_snap_v_num = 0        # (integer)
        self.stem_snap_v = [[]]

        #  Other
        self.modified = 0  # (integer)      - 0 if unmodified, 1 if modified (to control the 
        #                           'save changes' dialog) <font color="red">(this attribute is not 
        #                           reported by the docstring)</font>
        self.classes = []  # [string]        - list of glyph classes
        self.ot_classes = ""  # (string)     - string containing the OT classes defined in the lower
        #                           right part of the OpenType panel <font color="red">(this description 
        #                           is not reported by the docstring)</font>
        self.features = []  # [<a href="Feature.xml.html">Feature</a>]      - list of OpenType features
        self.customdata = ""  # (string)     - font custom data field
        self.truetypetables = []  # [<a href="TrueTypeTable.xml.html">TrueTypeTable</a>] - list of custom TrueType tables
        self.ttinfo = TTInfo()  # (<a href="TTInfo.xml.html">TTInfo</a>)         - loaded TrueType information 
        #                                    (mostly hinting-related tables)
        self.encoding = None  # (<a href="Encoding.xml.html">Encoding</a>)     - current encoding of the font
        self.codepages = []  # [integer]     - list of codepage-numbers (see OT-specs)
        #                           <font color="red">(this attribute is not reported by the docstring
        #                           this attribute is linked with the
        #                           ttinfo.os2_ul_code_page_range1 and
        #                           ttinfo.os2_ul_code_page_range2 values)</font>
        self.unicoderanges = []  # [integer] - list of unicoderange-numbers (see OT-specs)
        #                           <font color="red">(this attribute is not reported by the docstring)</font>
        self._glyphs = []
        self.source = None  #                 - the Created By field
        #                          <font color="red">(this description is not reported by the docstring)</font>
        self.weight_vector = []  # [float]   - list of MM-settings for generate instance
        self.hguides = []  # [<a href="Guide.xml.html">Guide</a>]        - list of horizontal guides
        #                           <font color="red">(new in v4.5.4 and not reported by docstring)</font>
        self.vguides = []  # [<a href="Guide.xml.html">Guide</a>]        - list of vertical guides
        #                           <font color="red">(new in v4.5.4 and not reported by docstring)</font>

        self._axis = []


if __name__ == "__main__":
    import doctest
    import Glyph
    doctest.testmod()
    f = Font()
    g = Glyph.Glyph()
    f.glyphs.append(g)
    f.Save("test.json")
