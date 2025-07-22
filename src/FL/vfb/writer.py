from __future__ import annotations

# from fontTools.misc.textTools import deHexStr, hexStr
from typing import TYPE_CHECKING, Any

from vfbLib.constants import entry_ids
from vfbLib.vfb.entry import VfbEntry
from vfbLib.vfb.header import VfbHeader
from vfbLib.vfb.vfb import Vfb

if TYPE_CHECKING:
    from pathlib import Path

    from FL.objects.Font import Font


class FontToVfbWriter:
    """
    Convert the Font object to the low-level `vfbLib.vfb.vfb.Vfb` structure and write it
    to `vfb_path`
    """

    def __init__(self, font: Font, vfb_path: Path) -> None:
        """Save the `font` into the VFB file at `vfb_path`.

        Args:
            font (Font): The source object of the data
            vfb_path (Path): The file path to which to write the VFB data
        """
        self.vfb_path = vfb_path
        self.font = font
        self.vfb = Vfb()
        self.compile()
        self.vfb.write(self.vfb_path)

    def add_direct_entries(self, keys: tuple[str, ...], parent: Any) -> None:
        for key in keys:
            self.add_entry(key, getattr(parent, key))

    def add_entry(self, eid: int | str, decompiled: Any) -> None:
        if isinstance(eid, str):
            eid_int = entry_ids.get(eid)
            if eid_int is None:
                raise ValueError
            e = VfbEntry(self.vfb, eid=eid_int)
        else:
            e = VfbEntry(self.vfb, eid=eid)
        e.decompiled = decompiled
        self.vfb.entries.append(e)

    def compile(self) -> None:
        self.compile_header()
        self.compile_encoding()
        self.compile_font_info()
        self.compile_glyphs()
        self.compile_options()
        # That's all, folks

    def compile_header(self) -> None:
        header = self.vfb.header = VfbHeader()
        # fmt: off
        header.decompiled = {
            "header0": 26,
            "filetype": "WLF10",
            "header1": 3,
            "chunk1": [
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 1, 0, 0, 0, 4, 0, 0, 0, 10, 0
            ],
            "creator": {"1": 1, "2": [5, 2, 2, 128], "3": 0},
            "end0": 6,
            "end1": 1,
            "end2": 0,
        }
        # fmt: on
        header.modified = True

    def compile_encoding(self) -> None:
        # TODO: "Encoding Default"?
        for i in range(len(self.font.encoding)):
            self.add_entry("Encoding", [i, self.font.encoding[i].name])

        # We don't know what these do exactly:
        # Sometimes 0, sometimes 1, sometimes 42694?
        self.add_entry(1502, self.font._unknown_pleasures["1502"])
        # Apparently always empty:
        self.add_entry(518, self.font._unknown_pleasures["518"])
        self.add_entry(257, self.font._unknown_pleasures["257"])

    def compile_font_info(self) -> None:
        font = self.font
        self.vfb.num_masters = font._masters_count
        self.add_entry("font_name", font.font_name)
        self.add_entry("Master Count", self.vfb.num_masters)
        self.add_entry("weight_vector", font.weight_vector[: self.vfb.num_masters])
        self.add_direct_entries(
            (
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
            ),
            font,
        )
        self.add_entry("License", font._license)
        self.add_entry("License URL", font._license_url)
        self.add_direct_entries(
            (
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
            ),
            font,
        )
        self.add_entry(1140, font._unknown_pleasures["1140"])
        self.add_direct_entries(
            (
                "vendor",
                "xuid",
                "xuid_num",
                "year",
                "version_major",
                "version_minor",
                "upm",
                "fond_id",
            ),
            font,
        )
        self.add_entry("PostScript Hinting Options", font._postscript_hinting_options)
        self.add_entry(1068, font._unknown_pleasures["1068"])
        self.add_direct_entries(
            (
                "blue_values_num",
                "other_blues_num",
                "family_blues_num",
                "family_other_blues_num",
                "stem_snap_h_num",
                "stem_snap_v_num",
                "font_style",
            ),
            font,
        )
        if font.pcl_id >= 0:
            self.add_entry("pcl_id", font.pcl_id)
        if font.vp_id >= 0:
            self.add_entry("vp_id", font.vp_id)

        self.add_direct_entries(
            (
                "ms_id",
                "pcl_chars_set",
            ),
            font,
        )

        self.compile_ttinfo()

        # Special handling required:
        self.add_entry("fontnames", [nr.fake_serialize() for nr in font.fontnames])
        self.add_entry("Custom CMAPs", font._custom_cmaps)
        self.add_entry("PCLT Table", font._pclt_table)
        self.add_entry("Export PCLT Table", font._export_pclt_table)
        if font.note:
            self.add_entry("note", font.note)
        self.add_entry(2030, font._unknown_pleasures["2030"])
        if font.customdata:
            self.add_entry("customdata", font.customdata)

        for ttt in font.truetypetables:
            self.add_entry("TrueTypeTable", ttt)

        # TODO:
        # "OpenType Metrics Class Flags"
        # "OpenType Kerning Class Flags"

        fea = font.fake_serialize_features()
        if fea:
            self.add_entry("features", fea)

        self.add_entry(513, font._unknown_pleasures["513"])
        self.add_entry(271, font._unknown_pleasures["271"])

        self.add_entry("Axis Count", len(font.axis))

        for axis_name in font.fake_serialize_axis():
            self.add_entry("Axis Name", axis_name)

        self.add_entry(
            "Anisotropic Interpolation Mappings",
            font._anisotropic_interpolation_mappings,
        )
        self.add_entry("Axis Mappings Count", font._axis_mappings_count)
        self.add_entry("Axis Mappings", font._axis_mappings)

        for master_index in range(self.vfb.num_masters):
            self.add_entry("Master Name", font._master_names[master_index])
            self.add_entry("Master Location", font._master_locations[master_index])

        if font._primary_instance_locations:
            self.add_entry(
                "Primary Instance Locations", font._primary_instance_locations
            )
        if font._primary_instances:
            self.add_entry("Primary Instances", font._primary_instances)

        for master_ps_info in font._master_ps_infos:
            self.add_entry("PostScript Info", master_ps_info)

        self.add_entry(527, font._unknown_pleasures["527"])

        if font.hguides or font.vguides:
            self.add_entry("Global Guides", font.fake_serialize_guides())
            self.add_entry(
                "Global Guide Properties", font.fake_serialize_guide_properties()
            )

        if font.default_character:
            self.add_entry("default_character", font.default_character)

    def compile_ttinfo(self) -> None:
        for k in ("cvt", "prep", "fpgm"):
            d = self.font.ttinfo.fake_get_binary(k)
            if d:
                self.add_entry(k, d)

        if gasp := self.font.ttinfo.fake_serialize_gasp():
            self.add_entry("gasp", gasp)

        self.add_entry("ttinfo", self.font.ttinfo.fake_serialize())
        self.add_entry("vdmx", self.font.ttinfo.fake_serialize_vdmx())
        self.add_direct_entries(
            ("hhea_line_gap", "hhea_ascender", "hhea_descender"), self.font.ttinfo
        )
        # "TrueType Stem PPEMS 2 And 3" are skipped, it is apparently a remnant of some
        # old FontLab version. The data is also contained in "TrueType Stem PPEMs"
        self.add_entry(
            "TrueType Stem PPEMs", self.font.ttinfo.fake_serialize_stem_ppems()
        )
        self.add_entry("TrueType Stems", self.font.ttinfo.fake_serialize_stems())
        self.add_entry(
            "TrueType Stem PPEMs 1", self.font.ttinfo.fake_serialize_stem_ppems1()
        )
        self.add_entry("TrueType Zones", self.font.ttinfo.fake_serialize_zones())
        self.add_entry("unicoderanges", self.font.unicoderanges)  # Not TTInfo
        self.add_entry("stemsnaplimit", self.font.ttinfo._stemsnaplimit)
        self.add_entry("zoneppm", self.font.ttinfo._zoneppm)
        self.add_entry("codeppm", self.font.ttinfo._codeppm)

        self.add_entry(1604, self.font.ttinfo._unknown_pleasures["1604"])
        self.add_entry(2032, self.font.ttinfo._unknown_pleasures["2032"])

        self.add_entry(
            "TrueType Zone Deltas", self.font.ttinfo.fake_serialize_zone_deltas()
        )

    def compile_glyphs(self) -> None:
        for glyph in self.font.glyphs:
            glyph_dict = glyph.fake_serialize()
            # TODO: Which keys are required?
            for key in (
                "Glyph",
                "Links",
                "image",
                "Glyph Bitmaps",
                "2023",
                "Glyph Sketch",
                "Glyph Hinting Options",
                "mask",
                "mask.metrics",
                "mask.metrics_mm",
                "Glyph Origin",
                "unicodes",
                "2034",
                "Glyph Unicode Non-BMP",
                "mark",
                "glyph.customdata",
                "glyph.note",
                "Glyph GDEF Data",
                "Glyph Anchors Supplemental",
                "Glyph Anchors MM",
                "Glyph Guide Properties",
            ):
                if key in glyph_dict:
                    self.add_entry(key, glyph_dict[key])

    def compile_options(self) -> None:
        # TODO:
        # "OpenType Export Options"
        # "Export Options"

        self.add_entry("Mapping Mode", self.font._mapping_mode)
