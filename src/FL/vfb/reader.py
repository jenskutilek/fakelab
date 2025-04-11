from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from vfbLib.vfb.vfb import Vfb

from FL.helpers.nametables import StandardNametable
from FL.objects.Encoding import Encoding
from FL.objects.EncodingRecord import EncodingRecord
from FL.objects.Glyph import Glyph

if TYPE_CHECKING:
    from pathlib import Path

    from FL.objects.Font import Font


logger = logging.getLogger(__name__)


font_mapping_direct = {
    "font_name",
    "weight_vector",
    "unique_id",
    "version",
    "notice",
    "full_name",
    "family_name",
    "pref_family_name",
    "menu_name",
    "apple_name",
    "weight",
    "width",
    "copyright",
    "trademark",
    "designer",
    "designer_url",
    "vendor_url",
    "source",
    "is_fixed_pitch",
    "weight_code",
    "italic_angle",
    "slant_angle",
    "underline_position",
    "underline_thickness",
    "ms_charset",
    "panose",
    "tt_version",
    "tt_u_id",
    "style_name",
    "pref_style_name",
    "mac_compatible",
    "vendor",
    # "xuid",  # has no setter
    "xuid_num",
    "year",
    "version_major",
    "version_minor",
    "upm",
    "fond_id",
    "blue_values_num",
    "other_blues_num",
    "family_blues_num",
    "family_other_blues_num",
    "stem_snap_h_num",
    "stem_snap_v_num",
    "font_style",
    "pcl_id",
    "vp_id",
    "ms_id",
    "pcl_chars_set",
    # "unicoderanges",  # must be converted to a list of bits
    "note",
    "customdata",
    "default_character",
}

glyph_mapping = {
    "Links",
    "image",
    "Glyph Bitmaps",
    "2023",
    "Glyph Sketch",
    "2010",
    "mask",
    "2011",
    "2028",
    "Glyph Origin",
    "unicodes",
    "Glyph Unicode Non-BMP",
    "mark",
    "glyph.customdata",
    "glyph.note",
    "Glyph GDEF Data",
    "Glyph Anchors Supplemental",
    "Glyph Anchors MM",
    "Glyph Guide Properties",
}

ttinfo_mapping_direct = {
    "gasp",
    "hhea_line_gap",
    "hhea_ascender",
    "hhea_descender",
}


class VfbToFontReader:
    """
    Instantiate the Font object and all related objects from a `vfbLib.vfb.vfb.Vfb` (I
    know...) object (low-level representation of the binary VFB format)
    """

    def __init__(self, vfb_path: Path, font: Font) -> None:
        """
        Load the VFB file from `vfb_path` and instantiate its data into `font`.

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
        classes: list[str] = []
        glyph: Glyph | None = None
        gids = {}

        for e in self.vfb.entries:
            name = e.key
            data = e.decompiled
            if name == "header":
                pass
            elif name in font_mapping_direct:
                if hasattr(self.font, name):
                    setattr(self.font, name, data)
                else:
                    raise AttributeError(f"Unknown font attribute: {name}")
            elif name == "xuid":
                # Has no setter in Python API
                self.font._xuid = data
            elif name == "Encoding":
                gid, glyph_name = data
                gids[gid] = glyph_name
            elif name == "Encoding Default":
                # Where is this used?
                pass
            elif name == "1502":
                pass
            elif name == "518":
                pass
            elif name == "257":
                pass
            elif name == "Master Count":
                self.font._masters_count = data
            elif name == "License":
                self.font._license = data
            elif name == "License URL":
                self.font._license_url = data
            elif name == "1140":
                pass
            elif name == "1093":
                pass
            elif name == "1068":
                pass
            elif name == "Binary cvt Table":
                pass
            elif name == "Binary prep Table":
                pass
            elif name == "Binary fpgm Table":
                pass
            elif name in ttinfo_mapping_direct:
                setattr(self.font.ttinfo, name, data)
            elif name == "ttinfo":
                pass
            elif name == "1271":
                pass
            elif name == "TrueType Stem PPEMs":
                pass
            elif name == "TrueType Stem PPEMs 1":
                pass
            elif name == "TrueType Stems":
                pass
            elif name == "TrueType Zones":
                pass
            elif name == "unicoderanges":
                # Must be converted to list
                pass
            elif name == "stemsnaplimit":
                pass
            elif name == "zoneppm":
                pass
            elif name == "codeppm":
                pass
            elif name == "1604":
                pass
            elif name == "2032":
                pass
            elif name == "TrueType Zone Deltas":
                pass
            elif name == "Name Records":
                pass
            elif name == "Custom CMAPs":
                pass
            elif name == "PCLT Table":
                pass
            elif name == "Export PCLT Table":
                pass
            elif name == "2030":
                pass
            elif name == "TrueTypeTable":
                pass
            elif name == "OpenType Metrics Class Flags":
                self.font._classes.fake_metrics_flags = data
            elif name == "OpenType Kerning Class Flags":
                self.font._classes.fake_kerning_flags = data
            elif name == "features":
                self.font.fake_set_features(data)
            elif name == "OpenType Class":
                classes.append(data)
            elif name == "513":
                pass
            elif name == "271":
                pass
            elif name == "Axis Count":
                pass
            elif name == "Axis Name":
                pass
            elif name == "Anisotropic Interpolation Mappings":
                pass
            elif name == "Axis Mappings Count":
                pass
            elif name == "Axis Mappings":
                pass
            elif name == "Master Name":
                pass
            elif name == "Master Location":
                pass
            elif name == "Primary Instance Locations":
                pass
            elif name == "Primary Instances":
                pass
            elif name == "PostScript Info":
                pass
            elif name == "527":
                pass
            elif name == "Global Guides":
                pass
            elif name == "Global Guide Properties":
                pass

            elif name == "Glyph":
                # Append the current glyph
                if glyph is not None:
                    self.font.glyphs.append(glyph)
                # Make a new glyph
                logger.info(f"Adding Glyph: '{data.get('name')}'")
                glyph = Glyph()
                # Add the data
                glyph.fake_deserialize(name, data)
            elif name in glyph_mapping:
                assert glyph is not None, "Glyph must exist before adding data"
                glyph.fake_deserialize(name, data)

            elif name == "OpenType Export Options":
                pass
            elif name == "Export Options":
                pass
            elif name == "Mapping Mode":
                pass
            elif name == "1410":
                pass

            else:
                print(f"Unhandled VFB entry: {name}")

        if glyph is not None:
            self.font.glyphs.append(glyph)

        if gids:
            enc = self.font._encoding = Encoding()
            enc._parent = self.font

            max_gid = min(255, max(gids))
            for i in range(max_gid + 1):
                er = EncodingRecord()
                if i in gids:
                    er.name = gids[i]
                    er.unicode = min(self.nametable.get_unicodes_for_name(er.name))
                else:
                    er.name = f"_{i:04d}"
                enc.append(er)

        if classes:
            # The setter can't append, assign the whole list
            self.font._classes.fake_set_classes(classes)
