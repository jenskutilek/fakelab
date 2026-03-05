from typing import TYPE_CHECKING, Any

from FL.fake.PSInfo import get_default_ps_info
from FL.helpers.classList import ClassList
from FL.helpers.FLList import adjust_list
from FL.helpers.ListParent import ListParent
from FL.objects.Encoding import Encoding
from FL.objects.Options import Options
from FL.objects.TTInfo import TTInfo
from FL.objects.WeightVector import WeightVector

if TYPE_CHECKING:
    from vfbLib.typing import CustomCmap, PSInfoDict

    from FL.objects.EncodingRecord import EncodingRecord
    from FL.objects.Feature import Feature
    from FL.objects.Glyph import Glyph
    from FL.objects.Guide import Guide
    from FL.objects.NameRecord import NameRecord
    from FL.objects.TrueTypeTable import TrueTypeTable


__doc__ = "Class to represent a font"


class BaseFont:
    """
    Base class to represent a font
    """

    __slots__ = [
        "_axis",
        "_classes",
        "_encoding",
        "_features",
        "_file_name",
        "_fontnames",
        "_glyphs",
        "_license_url",
        "_license",
        "_masters_count",
        "_postscript_hinting_options",
        "_truetypetables",
        "_xuid_num",
        "_xuid",
        "apple_name",
        "_ascender",
        "blue_fuzz",
        "blue_scale",
        "blue_shift",
        "_blue_values_num",
        "_cap_height",
        "codepages",
        "copyright",
        "customdata",
        "default_character",
        "_default_width",
        "_descender",
        "designer_url",
        "designer",
        "_family_blues_num",
        "family_name",
        "_family_other_blues_num",
        "fond_id",
        "font_name",
        "font_style",
        "full_name",
        "hguides",
        "is_fixed_pitch",
        "italic_angle",
        "mac_compatible",
        "menu_name",
        "modified",
        "ms_charset",
        "ms_id",
        "note",
        "notice",
        "ot_classes",
        "_other_blues_num",
        "panose",
        "pcl_chars_set",
        "pcl_id",
        "pref_family_name",
        "pref_style_name",
        "slant_angle",
        "source",
        "_stem_snap_h_num",
        "_stem_snap_v_num",
        "style_name",
        "trademark",
        "tt_u_id",
        "tt_version",
        "ttinfo",
        "underline_position",
        "underline_thickness",
        "unicoderanges",
        "unique_id",
        "upm",
        "vendor_url",
        "_vendor",
        "version_major",
        "version_minor",
        "version",
        "vguides",
        "vp_id",
        "weight_code",
        "weight_vector",
        "weight",
        "width",
        "_x_height",
        "year",
        # Non-API:
        "_custom_cmaps",
        "_custom_dict",
        "_encoding_default",
        "_export_pclt_table",
        "_export_options",
        "_global_mask",
        "_ot_export_options",
        "_pclt_table",
        "_axis_count",
        "_anisotropic_interpolation_mappings",
        "_axis_mappings_count",
        "_axis_mappings",
        "_collection",
        "_font_flags",  # 2030
        "_kerning_class_flags",
        "_master_names",
        "_master_locations",
        "_master_ps_infos",
        "_mapping_mode",
        "_metrics_class_flags",
        "_mm_enc_type",  # 1502
        "_primary_instance_locations",
        "_primary_instances",
        "_sample_text",  # 1140
        # Internal:
        "_fake_binaries",
        "_fake_kerning",
        "_file_name",
        "_selection",
        "fake_sparse_json",
        "fake_vfb_object",
    ]

    def __getitem__(self, index: int | str) -> "Glyph | None":
        """
        Access the glyphs array.

        Args:
            index (int | str): The glyph index to get.

        Returns:
            Glyph | None: Return the glyph, or None if the index was out of bounds.
        """
        if isinstance(index, str):
            # We got a glyph name
            for glyph in self._glyphs:
                if glyph.name == index:
                    return glyph
            return None

        return self._glyphs[index]

    def __init__(self) -> None:
        # Identification

        options = Options()

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
        self.width = "Normal"
        self.designer: str | None = None
        self.designer_url: str | None = None
        # list of font name records
        self._fontnames: "ListParent[NameRecord]" = ListParent(parent=self)
        # Copyright name field
        self.copyright: str | None = None
        # Notice field
        self.notice: str | None = None
        # Font note
        self.note: str | None = None
        # Type 1 Unique ID number
        self.unique_id: int = -1
        # TrueType Unique ID record
        self.tt_u_id: str | None = None
        # TrueType Version record
        self.tt_version: str | None = None
        self.trademark: str | None = None
        self._xuid: list[int] = []
        self._xuid_num: int = 0
        # TrueType vendor code
        self._vendor = options.VendorCode
        self.vendor_url: str | None = None
        self.version: str | None = None

        self.year: int = 0
        self.version_major: int = 1
        self.version_minor: int = 0

        self.vp_id: int = -1
        self.ms_charset: int = 0
        self.ms_id: int = 0
        # list of Panose values
        self.panose: list[int] = [0] * 10
        self.pcl_chars_set: str = " 9U"
        self.pcl_id: int = -1

        #  Dimensions
        self.upm: int = 1000
        # list of ascenders, one for each master
        self._ascender: list[int] = [750] * 16
        # list of descenders, one for each master
        self._descender: list[int] = [-250] * 16
        # list of CapHeight records, one for each master
        self._cap_height: list[int] = [700] * 16
        # list of xHeight values, one for each master
        self._x_height: list[int] = [500] * 16
        self._default_width: list[int] = [500] * 16
        self.slant_angle: float = 0.0
        self.italic_angle: float = 0.0
        self.is_fixed_pitch: int = 0
        self.underline_position: int = -100
        self.underline_thickness: int = 50

        #  Alignment
        self.blue_fuzz: list[int] = [1] * 16
        self.blue_scale: list[float] = [0.039625] * 16
        self.blue_shift: list[int] = [7] * 16

        # number of defined blue values
        self._blue_values_num = 0
        # number of defined OtherBlues values
        self._other_blues_num = 0
        # number of FamilyBlues records
        self._family_blues_num = 0
        # number of FamilyOtherBlues records
        self._family_other_blues_num = 0

        # The number of stem snap values is stored here, the values themselves are taken
        # from self._master_ps_infos
        self._stem_snap_h_num: int = 0
        self._stem_snap_v_num: int = 0

        # up until here the default values have been verified

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
        self._features: "ListParent[Feature]" = ListParent(parent=self)
        # font custom data field
        self.customdata: str = ""
        # list of custom TrueType tables
        self._truetypetables: "ListParent[TrueTypeTable]" = ListParent(parent=self)
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
        self.weight_vector = WeightVector()
        self.weight_vector._parent = self
        # list of horizontal guides
        # <font color="red">(new in v4.5.4 and not reported by docstring)</font>
        self.hguides: "list[Guide]" = []
        # list of vertical guides
        # <font color="red">(new in v4.5.4 and not reported by docstring)</font>
        self.vguides: "list[Guide]" = []

        self._axis: list[tuple[str, str, str]] = []
        self._glyphs: "ListParent[Glyph]" = ListParent(parent=self)

        # Font data that is not accessible via FL5 Python API
        self._collection: list[Any] = []
        self._encoding_default: "list[EncodingRecord]" = []
        self._font_flags = ""
        self._global_mask: Glyph | None = None
        self._masters_count: int = 1
        self._license: str = ""
        self._license_url: str = ""
        self._custom_cmaps: "list[CustomCmap]" = []
        self._custom_dict: str = ""
        self._export_pclt_table: int = 0
        self._pclt_table: dict[str, Any] = {
            "font_number": 0,
            "pitch": 0,
            "x_height": 0,
            "style": 0,
            "type_family": 0,
            "cap_height": 0,
            "symbol_set": 0,
            "typeface": "\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000",
            "character_complement": [0] * 8,
            "file_name": "\u0000\u0000\u0000\u0000\u0000\u0000",
            "stroke_weight": 0,
            "width_type": 0,
            "serif_style": 0,
        }
        self._export_options: list[str] = []
        self._ot_export_options: list[dict[str, int]] = []
        self._axis_count: int = 0
        self._anisotropic_interpolation_mappings: list[tuple[int, int]] = []
        self._axis_mappings_count: list[int] = [0, 0, 0, 0]
        self._axis_mappings: list[tuple[float, float]] = [(0.0, 0.0)] * 40
        self._kerning_class_flags: dict[str, tuple[int, int]] = {}
        self._metrics_class_flags: dict[str, tuple[int, int, int]] = {}
        self._master_names = ["Untitled"]
        self._master_locations = [(1, (0.0, 0.0, 0.0, 0.0))]
        # The infos are always stored for all possible masters
        self._master_ps_infos: "list[PSInfoDict]" = [
            get_default_ps_info() for _ in range(16)
        ]
        self._mapping_mode = {
            "mapping_mode": "names_or_index",
            "m2": 152,
            "m3": 316,
            "mapping_id": 1,
        }
        self._mm_enc_type = 0
        self._primary_instance_locations: list[float] = []
        self._primary_instances: list[dict[str, Any]] = []
        self._postscript_hinting_options: dict[str, list[int] | int] = {"other": []}
        self._sample_text = ""
        self.fake_vfb_object = None

    def __len__(self) -> int:
        """
        Return the number of glyphs.

        Returns:
            int: The number of glyphs.
        """
        return len(self._glyphs)

    def __repr__(self) -> str:
        return "<Font: '%s', %i glyphs>" % (self.full_name, len(self))

    # Helpers

    def _get_ps_info_blues(self, key: str) -> list[list[int]]:
        blues = []
        for master_ps_info in self._master_ps_infos:
            blues.append(master_ps_info[key])
        return blues

    def _set_blues_num_attr(
        self, value: int, attr: str, key: str, max_num: int
    ) -> None:
        if getattr(self, attr) == value:
            return

        if not 0 <= value <= max_num:
            raise RuntimeError(f'New "{attr[1:]}" is out of range 0..{max_num}')

        setattr(self, attr, value)
        for master_info in self._master_ps_infos:
            adjust_list(master_info[key], new_length=value, value=0)

    # Attributes

    @property
    def file_name(self) -> str:
        """
        Full path of the file from which the font was opened/saved.
        """
        # The file path is stored internally as Path, but we return a str
        return str(self._file_name)

    @property
    def ascender(self) -> list[int]:
        return self._ascender

    @ascender.setter
    def ascender(self, value: list[int]) -> None:
        raise RuntimeError("Class Font has no attribute ascender or it is read-only")

    @property
    def axis(self) -> list[tuple[str, str, str]]:
        """
        Array of font axes. Not reported by docstring nor e-font.

        Example: [("Weight", "Wt", "Weight")]
        """
        # Returns a copy (append has no effect)
        return self._axis.copy()

    @property
    def blue_values_num(self) -> int:
        return self._blue_values_num

    @blue_values_num.setter
    def blue_values_num(self, value: int) -> None:
        """
        Set the number of blue values. The length of the existing lists will be adjusted.

        Args:
            value (int): The number of blue values, 0 to 14.
        """
        self._set_blues_num_attr(value, "_blue_values_num", "blue_values", 14)

    @property
    def blue_values(self) -> list[list[int]]:
        """
        Two-dimensional array of BlueValues. Master index is top-level index.

        Returns:
            list[list[int]]: The blue values for all masters.
        """
        return self._get_ps_info_blues("blue_values")

    @blue_values.setter
    def blue_values(self, value: list[list[int]]) -> None:
        raise RuntimeError("Class Font has no attribute blue_values or it is read-only")

    @property
    def cap_height(self) -> list[int]:
        return self._cap_height

    @cap_height.setter
    def cap_height(self, value: list[int]) -> None:
        raise RuntimeError("Class Font has no attribute cap_height or it is read-only")

    @property
    def classes(self) -> list[str]:
        """
        List of glyph classes.

        Returns a copy of the list. To change entries, you must reassign the whole list.
        """
        return list(self._classes)

    @classes.setter
    def classes(self, value: list[str]) -> None:
        self._classes.fake_set_classes(value)

    @property
    def default_width(self) -> list[int]:
        return self._default_width

    @default_width.setter
    def default_width(self, value: list[int]) -> None:
        raise RuntimeError(
            "Class Font has no attribute default_width or it is read-only"
        )

    @property
    def descender(self) -> list[int]:
        return self._descender

    @descender.setter
    def descender(self, value: list[int]) -> None:
        raise RuntimeError("Class Font has no attribute descender or it is read-only")

    @property
    def encoding(self) -> Encoding:
        """
        Current encoding of the font.
        """
        return self._encoding

    @property
    def family_blues_num(self) -> int:
        return self._family_blues_num

    @family_blues_num.setter
    def family_blues_num(self, value: int) -> None:
        """
        Set the number of family blues values. The length of the existing lists will be
        adjusted.

        Args:
            value (int): The number of family blues values, 0 to 14.
        """
        self._set_blues_num_attr(value, "_family_blues_num", "family_blues", 14)

    @property
    def family_blues(self) -> list[list[int]]:
        """
        Two-dimensional array of FamilyBlues. Master index is top-level index.

        Returns:
            list[list[int]]: The family blues values for all masters.
        """
        return self._get_ps_info_blues("family_blues")

    @family_blues.setter
    def family_blues(self, value: list[list[int]]) -> None:
        raise RuntimeError(
            "Class Font has no attribute family_blues or it is read-only"
        )

    @property
    def family_other_blues_num(self) -> int:
        return self._family_other_blues_num

    @family_other_blues_num.setter
    def family_other_blues_num(self, value: int) -> None:
        """
        Set the number of family other blues values. The length of the existing lists
        will be adjusted.

        Args:
            value (int): The number of family other blues values, 0 to 10.
        """
        self._set_blues_num_attr(
            value, "_family_other_blues_num", "family_other_blues", 10
        )

    @property
    def family_other_blues(self) -> list[list[int]]:
        """
        Two-dimensional array of FamilyOtherBlues. Master index is top-level index.

        Returns:
            list[list[int]]: The family other blues values for all masters.
        """
        return self._get_ps_info_blues("family_other_blues")

    @family_other_blues.setter
    def family_other_blues(self, value: list[list[int]]) -> None:
        raise RuntimeError(
            "Class Font has no attribute family_other_blues or it is read-only"
        )

    @property
    def features(self) -> "ListParent[Feature]":
        """
        List of Opentype features.
        """
        return self._features

    @features.setter
    def features(self, value: "list[Feature]") -> None:
        raise RuntimeError("Class Font has no attribute features or it is read-only")

    @property
    def fontnames(self) -> "ListParent[NameRecord]":
        """
        List of font name records.
        """
        return self._fontnames

    @fontnames.setter
    def fontnames(self, value: "list[NameRecord]") -> None:
        raise RuntimeError

    @property
    def force_bold(self) -> list[int]:
        """
        List of Force Bold values, one for each master.

        Returns:
            list[int]: The Force Bold values.
        """
        return [self._master_ps_infos[i]["force_bold"] for i in range(16)]

    @force_bold.setter
    def force_bold(self, value: list[int]) -> None:
        raise RuntimeError("Class Font has no attribute force_bold or it is read-only")

    @property
    def glyphs(self) -> "ListParent[Glyph]":
        """
        Return the array of glyphs.
        """
        # Read-only.
        return self._glyphs

    @glyphs.setter
    def glyphs(self, value: "list[Glyph]") -> None:
        raise RuntimeError

    @property
    def other_blues_num(self) -> int:
        return self._other_blues_num

    @other_blues_num.setter
    def other_blues_num(self, value: int) -> None:
        """
        Set the number of other blues values. The length of the existing lists will be
        adjusted.

        Args:
            value (int): The number of other blues values, 0 to 10.
        """
        self._set_blues_num_attr(value, "_other_blues_num", "other_blues", 10)

    @property
    def other_blues(self) -> list[list[int]]:
        """
        Two-dimensional array of OtherBlues. Master index is top-level index.

        Returns:
            list[list[int]]: The other blues values for all masters.
        """
        return self._get_ps_info_blues("other_blues")

    @other_blues.setter
    def other_blues(self, value: list[list[int]]) -> None:
        raise RuntimeError("Class Font has no attribute other_blues or it is read-only")

    @property
    def stem_snap_h(self) -> list[list[int]]:
        return [
            [
                self._master_ps_infos[i]["stem_snap_h"][j]
                for j in range(self.stem_snap_h_num)
            ]
            for i in range(16)
        ]

    @stem_snap_h.setter
    def stem_snap_h(self, value: list[list[int]]) -> None:
        raise RuntimeError("Class Font has no attribute stem_snap_h or it is read-only")

    @property
    def stem_snap_h_num(self) -> int:
        return self._stem_snap_h_num

    @stem_snap_h_num.setter
    def stem_snap_h_num(self, value: int) -> None:
        if not 0 <= value <= 12:
            raise RuntimeError('New "stem_snap_h_num" is out of range 0..12')
        self._stem_snap_h_num = value
        for i in range(len(self._master_ps_infos)):
            adjust_list(self._master_ps_infos[i]["stem_snap_h"], value)

    @property
    def stem_snap_v(self) -> list[list[int]]:
        return [
            [
                self._master_ps_infos[i]["stem_snap_v"][j]
                for j in range(self.stem_snap_v_num)
            ]
            for i in range(16)
        ]

    @stem_snap_v.setter
    def stem_snap_v(self, value: list[list[int]]) -> None:
        raise RuntimeError("Class Font has no attribute stem_snap_v or it is read-only")

    @property
    def stem_snap_v_num(self) -> int:
        return self._stem_snap_v_num

    @stem_snap_v_num.setter
    def stem_snap_v_num(self, value: int) -> None:
        if not 0 <= value <= 12:
            raise RuntimeError('New "stem_snap_v_num" is out of range 0..12')
        self._stem_snap_v_num = value
        for i in range(len(self._master_ps_infos)):
            adjust_list(self._master_ps_infos[i]["stem_snap_v"], value)

    @property
    def truetypetables(self) -> "ListParent[TrueTypeTable]":
        """
        List of custom TrueType tables.
        """
        # Read-only.
        return self._truetypetables

    @truetypetables.setter
    def truetypetables(self, value: "list[TrueTypeTable]") -> None:
        raise RuntimeError

    @property
    def vendor(self) -> str:
        return self._vendor

    @vendor.setter
    def vendor(self, value: str) -> None:
        if len(value) > 4:
            self._vendor = value[:4]
        else:
            self._vendor = value

    @property
    def x_height(self) -> list[int]:
        return self._x_height

    @x_height.setter
    def x_height(self, value: list[int]) -> None:
        raise RuntimeError("Class Font has no attribute x_height or it is read-only")

    @property
    def xuid(self) -> list[int]:
        """
        A list of Type 1 XUID numbers.

        The list may contain from 0 to 20 entries. To change the length of the list, set
        `Font.xuid_num`.


        Returns:
            list[int]: The list of Type 1 XUID numbers.
        """
        return self._xuid

    @property
    def xuid_num(self) -> int:
        """_summary_

        Returns:
            int: _description_
        """
        return self._xuid_num

    @xuid_num.setter
    def xuid_num(self, value: int) -> None:
        if not 0 <= value <= 20:
            raise RuntimeError('New "xuid_num" is out of range 0..20')
        diff = value - self._xuid_num
        if diff < 0:
            self._xuid = self.xuid[:value]
        elif diff > 0:
            self._xuid.extend([0] * diff)
        self._xuid_num = value
