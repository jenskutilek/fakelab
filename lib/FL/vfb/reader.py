from __future__ import annotations

from FL.helpers.nametables import StandardNametable
from FL.objects.Glyph import Glyph
from FL.objects.Encoding import Encoding
from FL.objects.EncodingRecord import EncodingRecord
from typing import TYPE_CHECKING
from vfbLib.vfb.vfb import Vfb

if TYPE_CHECKING:
    from pathlib import Path
    from FL.objects.Font import Font

font_mapping = {
    # "257"
    # "513"
    # "518"
    # "527"
    "sgn": "pref_family_name",  # 1024
    "ffn": "full_name",  # 1025
    "psn": "font_name",  # 1026
    "tfn": "family_name",  # 1027
    "weight_name": "style_name",  # 1028
    "Italic Angle": "italic_angle",  # 1029
    "underlinePosition": "underline_position",  # 1030
    "underlineThickness": "underline_thickness",  # 1031
    "Monospaced": "is_fixed_pitch",  # 1034
    "copyright": "copyright",  # 1037
    # "description": "openTypeNameDescription",  # 1038
    # "manufacturer": "openTypeNameManufacturer",  # 1039
    # "Type 1 Unique ID": "postscriptUniqueID",  # 1044
    "version full": "version",  # 1046
    "Slant Angle": "slant_angle",  # 1047
    "weight": "weight",  # 1048,
    "MS Character Set": "ms_charset",  # 1054
    "Menu Name": "menu_name",  # 1056
    "PCL ID": "pcl_id",  # 1057
    "VP ID": "vp_id",  # 1058
    # "1059"
    "MS ID": "ms_id",  # 1060
    "trademark": "trademark",  # 1061
    "designer": "designer",  # 1062
    "designerURL": "designer_url",  # 1063
    # "manufacturerURL": "openTypeNameManufacturerURL",  # 1064
    # "width_name": "widthName",  # 1065
    "Default Glyph": "default_character",  # 1066
    # "1068"
    # "License": "openTypeNameLicense",
    # "License URL": "openTypeNameLicenseURL",
    "FOND Family ID": "fond_id",  # 1090
    "FOND Name": "apple_name",  # 1092
    # 1093
    "panose": "panose",  # 1118
    "vendorID": "vendor",  # 1121
    # "Style Name": "",  # 1127
    "version": "version",  # 1128 or tt_version?
    "UniqueID": "tt_u_id",  # 1129
    "versionMajor": "version_major",  # 1130
    "versionMinor": "version_minor",  # 1131
    "year": "year",  # 1132
    "Type 1 XUIDs": "x_u_id",  # 1133
    "Type 1 XUIDs Count": "x_u_id_num",  # 1134
    "upm": "upm",  # 1135
    # "PCLT Table" 1136
    "tsn": "pref_style_name",  # 1137
    "OT Mac Name": "apple_name",  # 1139
    # "1140"
    # "hhea_ascender": "openTypeHheaAscender",
    # "hhea_descender": "openTypeHheaDescender",
    # "hhea_line_gap": "openTypeHheaLineGap",
    "fontNote": "note",  # 2025
}

# mapping_int = {
#     # "units_per_em": "unitsPerEm",  # duplicate
#     # "weight_class": "openTypeOS2WeightClass",  # duplicate
#     "width_class": "openTypeOS2WidthClass",
#     "lowest_rec_ppem": "openTypeHeadLowestRecPPEM",
#     "subscript_x_size": "openTypeOS2SubscriptXSize",
#     "subscript_y_size": "openTypeOS2SubscriptYSize",
#     "subscript_x_offset": "openTypeOS2SubscriptXOffset",
#     "subscript_y_offset": "openTypeOS2SubscriptYOffset",
#     "superscript_x_size": "openTypeOS2SuperscriptXSize",
#     "superscript_y_size": "openTypeOS2SuperscriptYSize",
#     "superscript_x_offset": "openTypeOS2SuperscriptXOffset",
#     "superscript_y_offset": "openTypeOS2SuperscriptYOffset",
#     "strikeout_size": "openTypeOS2StrikeoutSize",
#     "strikeout_position": "openTypeOS2StrikeoutPosition",
#     "OpenTypeOS2TypoAscender": "openTypeOS2TypoAscender",
#     "OpenTypeOS2TypoDescender": "openTypeOS2TypoDescender",
#     "OpenTypeOS2TypoLineGap": "openTypeOS2TypoLineGap",
#     "OpenTypeOS2WinAscent": "openTypeOS2WinAscent",
#     "OpenTypeOS2WinDescent": "openTypeOS2WinDescent",
# }


class VfbToFontReader:
    """
    Instantiate the Font object and all related objects from a `vfbLib.vfb.vfb.Vfb` (I
    know...) object (low-level representation of the binary VFB format)
    """

    def __init__(self, vfb_path: Path, font: Font) -> None:
        """Load the VFB file from `vfb_path` and instantiate its data into `font`.

        Args:
            vfb_path (Path): The file path from which to load the VFB data
            font (Font): The target object of the data
        """
        self.vfb_path = vfb_path
        self.font = font
        self.nametable = StandardNametable()
        self.open_vfb()
        self.read_into_font()

    def open_vfb(self) -> None:
        self.vfb = Vfb(self.vfb_path)
        self.vfb.decompile()

    def read_into_font(self) -> None:
        current_glyph: Glyph | None = None
        enc = self.font._encoding = Encoding()
        enc._parent = self.font
        gids = {}

        for e in self.vfb.entries:
            name = e.key
            data = e.decompiled
            if name == "header":
                pass
            elif name in font_mapping:
                attr = font_mapping[name]
                if hasattr(self.font, attr):
                    setattr(self.font, attr, data)
                else:
                    print(f"Unknown font attribute: {attr}")
                    raise AttributeError
            elif name == "PCLT Table":  # 1136
                pass
            elif name == "Name Records":  # 1138
                pass
            elif name == "Glyph":  # 2001
                if current_glyph is not None:
                    self.font.glyphs.append(current_glyph)
                current_glyph = Glyph()
                current_glyph.name = data["name"]
            elif name == "Encoding":
                gid, glyph_name = data
                gids[gid] = glyph_name
        if current_glyph is not None:
            self.font.glyphs.append(current_glyph)
        if gids:
            max_gid = min(255, max(gids))
            for i in range(max_gid + 1):
                er = EncodingRecord()
                if i in gids:
                    er.name = gids[i]
                    er.unicode = min(self.nametable.get_unicodes_for_name(er.name))
                else:
                    er.name = f"_{i:04d}"
                enc.append(er)
