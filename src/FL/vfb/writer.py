from __future__ import annotations

# from fontTools.misc.textTools import deHexStr, hexStr
from typing import TYPE_CHECKING, Any

from vfbLib.enum import F, G, M, T
from vfbLib.parsers.header import FL30_APP, FL30_FILE, FL30_SIGNATURE
from vfbLib.typing import FLVersionDict, VfbHeaderDict
from vfbLib.vfb.entry import VfbEntry
from vfbLib.vfb.header import VfbHeader
from vfbLib.vfb.vfb import Vfb

from FL.objects.Font import Font
from FL.objects.TTInfo import TTInfo

if TYPE_CHECKING:
    from enum import IntEnum
    from pathlib import Path


__doc__ = "VFB file writer"


class FontToVfbWriter:
    """
    Convert the Font object to the low-level `vfbLib.vfb.vfb.Vfb` structure and write it
    to `vfb_path`
    """

    def __init__(self, font: Font) -> None:
        """
        Instantiate a writer that can write the `font` into a VFB file.

        Args:
            font (Font): The source object of the data
        """
        self.font = font
        self.vfb = Vfb()
        self.compile()

    def write(self, vfb_path: Path) -> None:
        """
        Write the VFB to `vfb_path`.

        Args:
            vfb_path (Path): The file path to which to write the VFB data.
        """
        self.vfb.write(vfb_path)

    def add_direct_entries(
        self, keys: tuple[int, ...], parent: Font | TTInfo, enum: type[IntEnum] = F
    ) -> None:
        for key in keys:
            attr = enum(key).name
            self.add_entry(key, getattr(parent, attr))

    def add_entry(self, eid: int, data: Any = "") -> None:
        e = VfbEntry(self.vfb, eid=eid)
        e.data = data
        self.vfb.entries.append(e)

    def compile(self) -> None:
        self.compile_header()
        self.add_entry(F.BlockFileDataStart)
        self.add_entry(F.BlockFontStart)
        self.compile_fl_version()
        self.add_entry(F.BlockNamesStart)
        self.compile_encoding()
        self.add_entry(F.BlockNamesEnd, "")
        self.add_entry(F.BlockFontInfoStart, "")
        self.compile_font_info()
        self.add_entry(F.BlockFontInfoEnd, "")
        self.add_entry(F.BlockMMFontInfoStart, "")
        self.compile_mm_font_info()
        self.add_entry(F.BlockMMFontInfoEnd, "")
        self.compile_global_properties()
        self.compile_glyphs()
        self.compile_options()
        # We ignored the FL3 MM Kerning
        # self.add_entry(F.BlockMMKerningStart, "")
        # self.add_entry(F.BlockMMKerningEnd, "")
        self.add_entry(F.BlockFontEnd, "")
        self.add_entry(F.BlockFileDataEnd, "")
        # That's all, folks

    def compile_header(self) -> None:
        self.vfb.header = VfbHeader()
        self.vfb.header.data = VfbHeaderDict(
            signature=FL30_SIGNATURE,
            app_version=FL30_APP,
            file_version=FL30_FILE,
            version_major=3,
            version_minor=0,
        )

    def compile_fl_version(self) -> None:
        self.add_entry(
            F.FLVersion,
            FLVersionDict(platform="macos", version=(5, 2, 2, 128), owner=0),
        )

    def compile_encoding(self) -> None:
        for i in range(len(self.font._encoding_default)):
            self.add_entry(F.EncodingDefault, [i, self.font._encoding_default[i].name])
        for i in range(len(self.font.encoding)):
            self.add_entry(F.Encoding, [i, self.font.encoding[i].name])

        # We don't know what this is exactly:
        self.add_entry(F.MMEncType, self.font._unknown_pleasures[F.MMEncType])

    def compile_font_info(self) -> None:
        font = self.font
        self.vfb.num_masters = font._masters_count
        self.add_entry(F.font_name, font.font_name)
        self.add_entry(F.MasterCount, self.vfb.num_masters)
        self.add_entry(F.weight_vector, font.weight_vector[: self.vfb.num_masters])
        self.add_direct_entries(
            (
                F.unique_id,
                F.version,
                F.notice,
                F.full_name,
                F.family_name,
                F.pref_family_name,
                F.menu_name,
                F.apple_name,
                F.weight,
                F.width,
            ),
            font,
        )
        self.add_entry(F.License, font._license)
        self.add_entry(F.LicenseURL, font._license_url)
        self.add_direct_entries(
            (
                F.copyright,
                F.trademark,
                F.designer,
                F.designer_url,
                F.vendor_url,
                F.source,
                F.is_fixed_pitch,
                F.weight_code,
                F.italic_angle,
                F.slant_angle,
                F.underline_position,
                F.underline_thickness,
                F.ms_charset,
                F.panose,
                F.tt_version,
                F.tt_u_id,
                F.style_name,
                F.pref_style_name,
                F.mac_compatible,
            ),
            font,
        )
        self.add_entry(F.SampleText, font._unknown_pleasures[F.SampleText])
        self.add_direct_entries(
            (
                F.vendor,
                F.xuid,
                F.xuid_num,
                F.year,
                F.version_major,
                F.version_minor,
                F.upm,
                F.fond_id,
            ),
            font,
        )
        self.add_entry(F.PostScriptHintingOptions, font._postscript_hinting_options)
        self.add_entry(F.Collection, font._unknown_pleasures[F.Collection])
        self.add_direct_entries(
            (
                F.blue_values_num,
                F.other_blues_num,
                F.family_blues_num,
                F.family_other_blues_num,
                F.stem_snap_h_num,
                F.stem_snap_v_num,
                F.font_style,
            ),
            font,
        )
        if font.pcl_id >= 0:
            self.add_entry(F.pcl_id, font.pcl_id)
        if font.vp_id >= 0:
            self.add_entry(F.vp_id, font.vp_id)

        self.add_direct_entries(
            (
                F.ms_id,
                F.pcl_chars_set,
            ),
            font,
        )

        self.compile_ttinfo()

        # Special handling required:
        self.add_entry(F.fontnames, [nr.fake_serialize() for nr in font.fontnames])
        self.add_entry(F.CustomCMAPs, font._custom_cmaps)
        self.add_entry(F.PCLTTable, font._pclt_table)
        self.add_entry(F.ExportPCLTTable, font._export_pclt_table)
        if font.note:
            self.add_entry(F.note, font.note)
        self.add_entry(F.FontFlags, font._unknown_pleasures[F.FontFlags])
        if font.customdata:
            self.add_entry(F.customdata, font.customdata)

        for ttt in font.truetypetables:
            self.add_entry(F.TrueTypeTable, ttt)

        if metrics_class_flags := font._metrics_class_flags:
            self.add_entry(F.MetricsClassFlags, metrics_class_flags)
        if kerning_class_flags := font._kerning_class_flags:
            self.add_entry(F.KerningClassFlags, kerning_class_flags)

        fea = font.fake_serialize_features()
        if fea:
            self.add_entry(F.features, fea)

        for ot_class in font._classes:
            self.add_entry(F.GlyphClass, ot_class)

    def compile_mm_font_info(self) -> None:
        font = self.font
        self.add_entry(F.AxisCount, len(font.axis))

        for axis_name in font.fake_serialize_axis():
            self.add_entry(F.AxisName, axis_name)

        self.add_entry(
            F.AnisotropicInterpolationMappings, font._anisotropic_interpolation_mappings
        )
        self.add_entry(F.AxisMappingsCount, font._axis_mappings_count)
        self.add_entry(F.AxisMappings, font._axis_mappings)

        for master_index in range(self.vfb.num_masters):
            self.add_entry(M.MasterName, font._master_names[master_index])
            self.add_entry(M.MasterLocation, font._master_locations[master_index])

        if font._primary_instance_locations:
            self.add_entry(F.PrimaryInstanceLocations, font._primary_instance_locations)
        if font._primary_instances:
            self.add_entry(F.PrimaryInstances, font._primary_instances)

        for master_ps_info in font.fake_serialize_master_ps_infos():
            self.add_entry(M.PostScriptInfo, master_ps_info)

    def compile_global_properties(self) -> None:
        font = self.font
        if font.hguides or font.vguides:
            self.add_entry(F.GlobalGuides, font.fake_serialize_guides())
            self.add_entry(
                F.GlobalGuideProperties, font.fake_serialize_guide_properties()
            )

        if font._global_mask:
            self.add_entry(F.GlobalMask, font.fake_serialize_global_mask())

        if font.default_character:
            self.add_entry(F.default_character, font.default_character)

    def compile_ttinfo(self) -> None:
        for k in (T.cvt, T.prep, T.fpgm):
            d = self.font.ttinfo.fake_get_binary(T(k).name)
            if d:
                self.add_entry(k, d)

        if gasp := self.font.ttinfo.fake_serialize_gasp():
            self.add_entry(T.gasp, gasp)

        self.add_entry(F.ttinfo, self.font.ttinfo.fake_serialize())
        self.add_entry(T.vdmx, self.font.ttinfo.fake_serialize_vdmx())
        self.add_direct_entries(
            (T.hhea_line_gap, T.hhea_ascender, T.hhea_descender), self.font.ttinfo, T
        )
        # "TrueType Stem PPEMS 2 And 3" are skipped, it is apparently a remnant of some
        # old FontLab version. The data is also contained in "TrueType Stem PPEMs"
        self.add_entry(
            T.TrueTypeStemPPEMs, self.font.ttinfo.fake_serialize_stem_ppems()
        )
        self.add_entry(T.TrueTypeStems, self.font.ttinfo.fake_serialize_stems())
        self.add_entry(
            T.TrueTypeStemPPEMs1, self.font.ttinfo.fake_serialize_stem_ppems1()
        )
        self.add_entry(T.TrueTypeZones, self.font.ttinfo.fake_serialize_zones())
        self.add_entry(F.unicoderanges, self.font.unicoderanges)  # Not TTInfo
        self.add_entry(T.stemsnaplimit, self.font.ttinfo._stemsnaplimit)
        self.add_entry(T.zoneppm, self.font.ttinfo._zoneppm)
        self.add_entry(T.codeppm, self.font.ttinfo._codeppm)

        self.add_entry(T.dropoutppm, self.font.ttinfo._unknown_pleasures[T.dropoutppm])
        self.add_entry(
            T.MeasurementLine, self.font.ttinfo._unknown_pleasures[T.MeasurementLine]
        )

        self.add_entry(
            T.TrueTypeZoneDeltas, self.font.ttinfo.fake_serialize_zone_deltas()
        )

    def compile_glyphs(self) -> None:
        for glyph in self.font.glyphs:
            glyph_dict = glyph.fake_serialize()
            # TODO: Which keys are required?
            for key in (
                G.Glyph,
                G.Links,
                G.image,  # FIXME
                G.Bitmaps,  # FIXME
                G.VSB,
                G.Sketch,  # FIXME
                G.HintingOptions,
                G.mask,
                G.MaskMetrics,
                G.MaskMetricsMM,
                G.Origin,
                G.unicodes,
                G.CustomDict,
                G.UnicodesNonBMP,
                G.mark,
                G.customdata,
                G.note,
                G.GDEFData,
                G.AnchorsProperties,
                G.AnchorsMM,
                G.GuideProperties,
            ):
                if key in glyph_dict:
                    self.add_entry(key, glyph_dict[key])

    def compile_options(self) -> None:
        if ot_export_options := self.font._ot_export_options:
            self.add_entry(F.FontOptions, ot_export_options)
        if export_options := self.font._export_options:
            self.add_entry(F.ExportOptions, export_options)

        self.add_entry(F.MappingMode, self.font._mapping_mode)
