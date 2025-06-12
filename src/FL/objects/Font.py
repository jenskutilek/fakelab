from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

from FL.fake.Font import FakeFont
from FL.helpers.classList import ClassList
from FL.helpers.ListParent import ListParent
from FL.objects.Encoding import Encoding
from FL.objects.Rect import Rect
from FL.objects.TTInfo import TTInfo
from FL.objects.Uni import Uni
from FL.objects.WeightVector import WeightVector

if TYPE_CHECKING:
    from FL.objects.Feature import Feature
    from FL.objects.Glyph import Glyph
    from FL.objects.Guide import Guide
    from FL.objects.NameRecord import NameRecord
    from FL.objects.TrueTypeTable import TrueTypeTable


class Font(FakeFont):
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
        "_truetypetables",
        "_xuid_num",
        "_xuid",
        "apple_name",
        "ascender",
        "blue_fuzz",
        "blue_scale",
        "blue_shift",
        "blue_values_num",
        "blue_values",
        "cap_height",
        "codepages",
        "copyright",
        "customdata",
        "default_character",
        "default_width",
        "descender",
        "designer_url",
        "designer",
        "family_blues_num",
        "family_blues",
        "family_name",
        "family_other_blues_num",
        "family_other_blues",
        "fond_id",
        "font_name",
        "font_style",
        "force_bold",
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
        "other_blues_num",
        "other_blues",
        "panose",
        "pcl_chars_set",
        "pcl_id",
        "pref_family_name",
        "pref_style_name",
        "slant_angle",
        "source",
        "stem_snap_h_num",
        "stem_snap_h",
        "stem_snap_v_num",
        "stem_snap_v",
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
        "vendor",
        "version_major",
        "version_minor",
        "version",
        "vguides",
        "vp_id",
        "weight_code",
        "weight_vector",
        "weight",
        "width",
        "x_height",
        "year",
        # Non-API:
        "_export_pclt_table",
        "_pclt_table",
        "_axis_count",
        "_anisotropic_interpolation_mappings",
        "_axis_mappings_count",
        "_axis_mappings",
        "_master_names",
        "_master_locations",
        "_master_ps_infos",
        "_mapping_mode",
        # Internal:
        "fake_vfb_object",
    ]

    # Constructor

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
                self._copy_constructor(font_or_path)
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

        Returns a copy of the list. To change entries, you must reassign the whole list.
        """
        return list(self._classes)

    @classes.setter
    def classes(self, value: list[str]) -> None:
        self._classes.fake_set_classes(value)

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
    def features(self, value: list[Feature]) -> None:
        raise RuntimeError("Class Font has no attribute features or it is read-only")

    @property
    def fontnames(self) -> ListParent[NameRecord]:
        """
        List of font name records.
        """
        return self._fontnames

    @fontnames.setter
    def fontnames(self, value: list[NameRecord]) -> None:
        raise RuntimeError

    @property
    def glyphs(self) -> ListParent[Glyph]:
        """
        Return the array of glyphs.
        """
        # Read-only.
        return self._glyphs

    @glyphs.setter
    def glyphs(self, value: list[Glyph]) -> None:
        raise RuntimeError

    @property
    def truetypetables(self) -> ListParent[TrueTypeTable]:
        """
        List of custom TrueType tables.
        """
        # Read-only.
        return self._truetypetables

    @truetypetables.setter
    def truetypetables(self, value: list[TrueTypeTable]) -> None:
        raise RuntimeError

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
        self._xuid_num: int = value

    # Operations

    def __len__(self) -> int:
        """
        Return the number of glyphs.

        Returns:
            int: The number of glyphs.
        """
        return len(self._glyphs)

    def __getitem__(self, index: int | str) -> Glyph | None:
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

    # Methods

    def New(self) -> None:
        """
        Clear the font.
        """
        raise NotImplementedError

    def Open(self, filename: str) -> int:
        """
        Open a font from a VFB file.

        Args:
            filename (str): The path and file name of the VFB file.

        Returns:
            int: 1 on success, 0 if the file could not be opened.

        If you need to import a font (not in VFB format), use `FL.Open()` or
        `FL.OpenFont()`.
        """
        from FL.vfb.reader import VfbToFontReader

        self._set_file_name(None)  # TODO: What if the font already is loaded from disk?
        try:
            reader = VfbToFontReader(Path(filename), self)
            self.fake_vfb_object = reader.vfb
        except:  # noqa: E722
            raise
            return 0
        self._set_file_name(filename)
        return 1

    def Save(self, filename: str) -> None:
        """
        Save the font in VFB format.

        Args:
            filename (str): The path and file name of the VFB file.
        """
        from FL.vfb.writer import FontToVfbWriter

        self._set_file_name(filename)
        FontToVfbWriter(self, Path(filename))

    def OpenAFM(self, filename: str, mode: int, layer: int) -> None:
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

    def SaveAFM(self, filename: str) -> None:
        """
        Save an AFM and an INF file.

        Args:
            filename (str): The path and filename to save the files to.
        """
        afm = self.fake_get_afm()
        afm_path = Path(filename).with_suffix(".afm")
        with open(afm_path, "w") as f:
            f.write(afm)
        inf = self.fake_get_inf()
        inf_path = Path(filename).with_suffix(".inf")
        with open(inf_path, "w") as f:
            f.write(inf)

    def _normalize_upm(self, value: float) -> int:
        # TODO: truncate value before scaling?
        return int(value * 1000 / self.upm)

    def fake_bounding_rect(self, for_afm: bool = False) -> Rect:
        if for_afm:
            x0 = 0
            y0 = self.descender[0] - (100 * self.upm / 1000)
            y1 = self.ascender[0] + (100 * self.upm / 1000)
        else:
            x0 = 32767
            y0 = 32767
            y1 = -32767
        rect = Rect(x0, y0, -32767, y1)
        for g in self.glyphs:
            gr = g.GetBoundingRect()
            print(g.name, gr)
            rect += gr
        return rect

    def fake_save_afm_expanded(self, filename: str) -> None:
        afm = self.fake_get_afm(expand_kerning=True)
        afm_path = Path(filename).with_suffix(".afm")
        with open(afm_path, "w") as f:
            f.write(afm)

    def fake_get_afm(self, expand_kerning: bool = False) -> str:
        afm = ["StartFontMetrics 2.0"]
        r = self.fake_bounding_rect(for_afm=True)
        bbox = (
            f"{self._normalize_upm(r.ll.x)} {self._normalize_upm(r.ll.y)} "
            f"{self._normalize_upm(r.ur.x)} {self._normalize_upm(r.ur.y)}"
        )
        if bbox == "32767 32767 -32767 -32767":
            bbox = "0 0 0 0"
        afm.extend(
            [
                f"Comment Copyright {self.notice}",
                f"Comment Panose {' '.join([str(p) for p in self.panose])}",
                f"FullName {self.full_name}",
                f"FontName {self.font_name}",
                f"FamilyName {self.family_name}",
                f"Weight {self.weight}",
                f"Notice {self.copyright}",
                f"Version {self.version_major}.{self.version_minor:03d}",
                f"IsFixedPitch {('false', 'true')[self.is_fixed_pitch]}",
                f"ItalicAngle {self.italic_angle:0.2f}",
                f"FontBBox {bbox}",
                f"Ascender {self._normalize_upm(self.ascender[0])}",
                f"Descender {self._normalize_upm(self.descender[0])}",
                f"XHeight {self._normalize_upm(self.x_height[0])}",
                f"CapHeight {self._normalize_upm(self.cap_height[0])}",
                f"UnderlinePosition {self._normalize_upm(self.underline_position)}",
                f"UnderlineThickness {self._normalize_upm(self.underline_thickness)}",
                "EncodingScheme FontSpecific",
                f"StartCharMetrics {len(self.glyphs)}",
            ]
        )
        glyphs = self.fake_sort_glyphs(self.glyphs.data)
        for g in glyphs:
            r = g.bounding_box
            bbox = (
                f"{self._normalize_upm(r.ll.x)} {self._normalize_upm(r.ll.y)} "
                f"{self._normalize_upm(r.ur.x)} {self._normalize_upm(r.ur.y)}"
            )
            if bbox == "32767 32767 -32767 -32767":
                bbox = "0 0 0 0"
            afm.append(
                f"C {g.unicode or -1} ; WX {self._normalize_upm(g.width)} ; "
                f"N {g.name} ; B {bbox} ;"
            )
        afm.append("EndCharMetrics")

        kerning = self.fake_get_afm_kerning(expand_kerning)
        if kerning:
            kerning = self.fake_sort_kerning(kerning)
            afm.append("StartKernData")
            afm.append(f"StartKernPairs {len(kerning)}")
            prev_L = ""
            for L, R, value in kerning:
                if prev_L != "" and prev_L != L:
                    afm.append("")
                afm.append(f"KPX {L} {R} {self._normalize_upm(value)}")
                prev_L = L

            afm.append("")
            afm.append("EndKernPairs")
            afm.append("EndKernData")
        afm.append("EndFontMetrics\n")

        return "\n".join(afm)

    def fake_get_afm_kerning(
        self, expand_kerning: bool = False
    ) -> list[tuple[str, str, int]]:
        if expand_kerning:
            self.fake_kerning.expand()
            return self.fake_kerning.flat_kerning

        kerning = []
        for g in self.glyphs:
            L = g.name
            for pair in g.kerning:
                R = self.glyphs[pair.key].name
                value = pair.value
                kerning.append((L, R, value))
        return kerning

    def fake_get_inf(self) -> str:
        inf = ""
        return inf

    def fake_set_features(self, features: str) -> None:
        self._features.clean()
        print("Features are ignored")

    def fake_sort_glyphs(self, glyphs: list[Glyph]) -> list[Glyph]:
        glyph_order = tuple([rec.name for rec in self.encoding])
        sortable = [(glyph_order.index(glyph.name), glyph) for glyph in glyphs]
        sortable.sort()
        print(sortable)
        return [glyph for _, glyph in sortable]

    def fake_sort_kerning(
        self, kerning: list[tuple[str, str, int]]
    ) -> list[tuple[str, str, int]]:
        glyph_order = tuple([rec.name for rec in self.glyphs])
        sortable = [
            (glyph_order.index(L), glyph_order.index(R), L, R, value)
            for L, R, value in kerning
        ]
        sortable.sort()
        return [(L, R, value) for _, _, L, R, value in sortable]

    def Reencode(self, e: Encoding, style: int = 0) -> None:
        """
        Apply an encoding to the font.

        The parameters of this method are not reported by the docstring and I don't know
        what the style parameter does.

        Args:
            e (Encoding): The encoding.
            style (int, optional): _description_. Defaults to 0.
        """
        raise NotImplementedError

    def FindGlyph(self, name_uni_int: str | Uni | int) -> int:
        """
        (name: str) | (unicode: Uni) | (unicode: int)
        - finds glyph and return its index or -1
        """
        if isinstance(name_uni_int, str):
            # name
            for i, g in enumerate(self._glyphs):
                if g.name == name_uni_int:
                    return i
            return -1
        elif isinstance(name_uni_int, Uni):
            # uni object
            for i, g in enumerate(self._glyphs):
                if name_uni_int.value in g.unicodes:
                    return i
            return -1
        elif isinstance(name_uni_int, int):
            # int (unicode value)
            for i, g in enumerate(self._glyphs):
                if name_uni_int in g.unicodes:
                    return i
            return -1
        else:
            raise TypeError

    def DefineAxis(self, name: str, type: str, shortname: str) -> None:
        """
        Defines a new Multiple Master axis.

        Args:
            name (str): _description_
            type (str): _description_
            shortname (str): _description_
        """
        raise NotImplementedError

    def DeleteAxis(self, axisindex: int, position: float) -> None:
        """
        Removes the axis

        Args:
            axisindex (int): _description_
            position (float): _description_
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

    def GenerateGlyph(self, name: str) -> Glyph:
        """
        Generates new glyph using 'name' as a source of information about glyph's
        composition. See 'FontLabDir/Mapping/alias.dat' for composition definitions.

        Args:
            name (str): _description_

        Returns:
            Glyph: _description_

        The glyph is not added to the font automatically.
        """
        glyph = Glyph()
        glyph.name = name
        return glyph

    def has_key(self, name_uni_int: str | Uni | int) -> int:
        """
        Find a glyph by name, unicode or integer unicode and return 1 (found) or 0 (not
        found).

        Args:
            name_uni_int (str | Uni | int): _description_

        Returns:
            int: 1 if the glyph name or unicode value are present in the font,
                0 otherwise.
        """
        glyph_index = self.FindGlyph(name_uni_int)
        if glyph_index == -1:
            return 0
        return 1

    def GenerateFont(self, fontType: int, filename: str) -> None:
        """
        Generate a font. Deprecated. See the `FL.objects.FontLab` class for a
        description.

        As a method of the `Font` class, this method is deprecated. Since FontLab 4.52
        for Mac and FontLab 4.53 for Windows, `GenerateFont` is a method of the
        `FontLab` class.

        Args:
            fontType (int): The font type.
            filename (str): The path and file name of the generated font.

        Raises:
            AttributeError: In FontLab 5, the method is deprecated.
        """
        raise AttributeError

    # Undocumented methods

    def MakeKernFeature(self, vector: WeightVector) -> None:
        """
        Generates 'kern' feature using font kerning and classes

        Args:
            vector (WeightVector): The `WeightVector` used to interpolate the kerning
                values.
        """
        raise NotImplementedError

    def MergeFonts(self, source: Font, flags: int | None = None) -> None:
        """
        Append all glyphs from the source font to the current fonts.
        Check mfXXXX constants for options.

        Args:
            source (Font): The source font to be merged.
            flags (int | None, optional): _description_. Defaults to None.
        """
        raise NotImplementedError

    def SetClassFlags(
        self,
        class_index: int,
        left_lsb: bool | int,
        right_rsb: bool | int,
        width: bool | int | None = None,
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
        Return the 'left' property of the class.

        Args:
            class_index (int): _description_

        Returns:
            int | None: Returns 0 for non-kerning classes, 0 or 1 for kerning classes,
                None for class_index outside the classes list length.
        """
        return self._classes.GetClassLeft(class_index)

    def GetClassRight(self, class_index: int) -> int | None:
        """
        Return the 'right' property of the class.

        Args:
            class_index (int): _description_

        Returns:
            int | None: Returns 0 for non-kerning classes, 0 or 1 for kerning classes,
                None for class_index outside the classes list length.
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
        self.width = "Normal"
        self.designer: str | None = None
        self.designer_url: str | None = None
        # list of font name records
        self._fontnames: ListParent[NameRecord] = ListParent(parent=self)
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
        self.xuid_num = 0
        self._xuid: list[int] = []
        # TrueType vendor code
        self.vendor: str = ""
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
        self.ascender: list[int] = [750] * 16
        # list of descenders, one for each master
        self.descender: list[int] = [-250] * 16
        # list of CapHeight records, one for each master
        self.cap_height: list[int] = [700] * 16
        # list of xHeight values, one for each master
        self.x_height: list[int] = [500] * 16
        self.default_width: list[int] = [500] * 16
        self.slant_angle: float = 0.0
        self.italic_angle: float = 0.0
        self.is_fixed_pitch: int = 0
        self.underline_position: int = -100
        self.underline_thickness: int = 50

        #  Alignment
        self.blue_fuzz: list[int] = [1] * 16
        self.blue_scale: list[float] = [0.039625] * 16
        self.blue_shift: list[int] = [7] * 16

        # up until here the default values have been verified

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
        self.weight_vector = WeightVector()
        self.weight_vector._parent = self
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
        self._export_pclt_table: int = 0
        self._pclt_table: dict[str, Any] = {}
        self._axis_count: int = 0
        self._anisotropic_interpolation_mappings: list[tuple[int, int]] = []
        self._axis_mappings_count: list[int] = [0, 0, 0, 0]
        self._axis_mappings: list[list[float]] = [[0.0, 0.0] * 40]
        self._master_names = ["Untitled"]
        self._master_locations = [(1, (0.0, 0.0, 0.0, 0.0))]
        self._master_ps_infos = [
            {
                "font_matrix": [0.001, 0.0, 0.0, 0.001, 0.0, 0.0],
                "force_bold": 0,
                "blue_values": [0] * 14,
                "other_blues": [0] * 10,
                "family_blues": [0] * 14,
                "family_other_blues": [0] * 10,
                "blue_scale": 0.039625,
                "blue_shift": 7,
                "blue_fuzz": 1,
                "std_hw": 100,
                "std_vw": 50,
                "stem_snap_h": [0] * 12,
                "stem_snap_v": [0] * 12,
                "bounding_box": {
                    "xMin": 32767,
                    "yMin": 32767,
                    "xMax": -32767,
                    "yMax": -32767,
                },
                "adv_width_min": 0,
                "adv_width_max": 0,
                "adv_width_avg": 500,
                "ascender": 750,
                "descender": -250,
                "x_height": 500,
                "cap_height": 700,
            }
        ]

        self._mapping_mode = {
            "mapping_mode": "names_or_index",
            "2": 152,
            "3": 316,
            "mapping_id": 1,
        }
