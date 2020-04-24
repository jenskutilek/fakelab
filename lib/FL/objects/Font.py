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

    # Additions for FakeLab

    def fake_update(self):
        """
        Is called from FontLab.UpdateFont()
        """
        for index, glyph in enumerate(self.glyphs):
            glyph.fake_update(self, index)

    # Attributes

    @property
    def file_name(self):
        return self._file_name

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
        - clears the font
        """
        raise NotImplementedError

    def Open(self, filename):
        """
        (string filename)
        - opens font from VFB format
        """
        raise NotImplementedError

    def Save(self, filename):
        """
        (string filename)
        - saves font in VFB format

        Saving VFB is not supported in FakeLab, but we can write a nice JSON
        format.
        """
        with codecs.open(filename, "wb", "utf-8") as f:
            json.dump(
                obj={
                    k: v
                    for k, v in self.__dict__.items()
                    if k not in (
                        "_file_name",
                    )
                },
                fp=f,
                default=lambda o: {
                    k: v
                    for k, v in o.__dict__.items()
                    if k not in (
                        "_parent",
                    )
                },
                indent=4
            )
            self._file_name = filename

    def OpenAFM(self, filename, mode, layer):
        """
        (string filename, int mode, int layer)
        - open AFM-File, mode is the integer bit field.
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

          Constants for mode <font color="red">(only in FL 4.5 Mac)</font>
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

    def SaveAFM(self, filename):
        """(string filename)
        - saves AFM- and INF-File
          <font color="red">(this method is not reported by the docstring)</font>
        """
        raise NotImplementedError

    def Reencode(self, e, style=0):
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
        raise NotImplementedError

    def DefineAxis(self, name_type_shortname):
        """
        (string Name, string Type, string ShortName)
        - defines the new Multiple Master axis
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

    # Defaults

    def set_defaults(self):
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


if __name__ == "__main__":
    import doctest
    import Glyph
    doctest.testmod()
    f = Font()
    g = Glyph.Glyph()
    f.glyphs.append(g)
    f.Save("test.json")
