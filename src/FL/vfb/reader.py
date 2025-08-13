from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from vfbLib.enum import F, G, M, T
from vfbLib.vfb.vfb import Vfb

from FL.helpers.nametables import StandardNametable
from FL.objects.Encoding import Encoding
from FL.objects.EncodingRecord import EncodingRecord
from FL.objects.Glyph import Glyph
from FL.objects.NameRecord import NameRecord

if TYPE_CHECKING:
    from pathlib import Path

    from FL.objects.Font import Font


__doc__ = "VFB file reader"


logger = logging.getLogger(__name__)


font_mapping_direct = {
    F.font_name,
    F.weight_vector,
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
    F.vendor,
    # F.xuid,  # has no setter
    F.xuid_num,
    F.year,
    F.version_major,
    F.version_minor,
    F.upm,
    F.fond_id,
    F.blue_values_num,
    F.other_blues_num,
    F.family_blues_num,
    F.family_other_blues_num,
    F.stem_snap_h_num,
    F.stem_snap_v_num,
    F.font_style,
    F.pcl_id,
    F.vp_id,
    F.ms_id,
    F.pcl_chars_set,
    # F.unicoderanges,  # must be converted to a list of bits
    F.note,
    F.customdata,
    F.default_character,
}

glyph_mapping = {
    G.Links,
    G.image,
    G.Bitmaps,
    G.E2023,
    G.Sketch,
    G.HintingOptions,
    G.mask,
    G.MaskMetrics,
    G.MaskMetricsMM,
    G.Origin,
    G.unicodes,
    G.UnicodesNonBMP,
    G.mark,
    G.customdata,
    G.note,
    G.GDEFData,
    G.AnchorsProperties,
    G.AnchorsMM,
    G.GuideProperties,
}

ttinfo_mapping_direct = {
    T.hhea_line_gap,
    T.hhea_ascender,
    T.hhea_descender,
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

        font = self.font
        font.fake_clear_defaults()

        for e in self.vfb.entries:
            key = e.id
            assert isinstance(key, int)
            data = e.data

            if key in font_mapping_direct:
                attr = F(key).name
                if hasattr(font, attr):
                    setattr(font, attr, data)
                else:
                    raise AttributeError(f"Unknown font attribute: {attr}")
                continue

            if key in glyph_mapping:
                assert glyph is not None, "Glyph must exist before adding data"
                glyph.fake_deserialize(key, data)
                continue

            if key in (T.cvt, T.prep, T.fpgm):
                font.ttinfo.fake_set_binary(T(key).name, data)
                continue

            if key in (
                T.TrueTypeStems,
                T.TrueTypeStemPPEMs1,
                T.TrueTypeStemPPEMs2And3,
                T.TrueTypeStemPPEMs,
            ):
                font.ttinfo.fake_deserialize_stems(data)
                continue

            if key in (
                F.E257,
                F.E271,
                F.E513,
                F.E518,
                F.E527,
                F.E1068,
                F.E1140,
                F.E1502,
                F.E2030,
                F.E2030,
            ):
                font._unknown_pleasures[key] = data
                continue

            if key in ttinfo_mapping_direct:
                setattr(font.ttinfo, T(key).name, data)
                continue

            if key in (T.E1604, T.E2032):
                font.ttinfo._unknown_pleasures[key] = data
                continue

            match key:
                case F.xuid:
                    font._xuid = data
                case F.Encoding:
                    gid, glyph_name = data
                    gids[gid] = glyph_name
                case F.EncodingDefault:
                    # Where is this used?
                    gid, glyph_name = data
                    e = EncodingRecord()
                    e.name = glyph_name
                    font._encoding_default.append(e)
                case F.MasterCount:
                    font._masters_count = data
                case F.License:
                    font._license = data
                case F.LicenseURL:
                    font._license_url = data
                case F.PostScriptHintingOptions:
                    font._postscript_hinting_options = data
                case T.gasp:
                    font.ttinfo.fake_deserialize_gasp(data)
                case F.ttinfo:
                    font.ttinfo.fake_deserialize(data)
                case T.vdmx:
                    font.ttinfo.fake_deserialize_vdmx(data)
                case T.TrueTypeZones:
                    font.ttinfo.fake_deserialize_zones(data)
                case F.unicoderanges:
                    font.unicoderanges = data
                case T.stemsnaplimit:
                    font.ttinfo._stemsnaplimit = data
                case T.zoneppm:
                    font.ttinfo._zoneppm = data
                case T.codeppm:
                    font.ttinfo._codeppm = data
                case T.TrueTypeZoneDeltas:
                    font.ttinfo.fake_deserialize_zone_deltas(data)
                case F.fontnames:
                    assert isinstance(data, list)
                    for nr in data:
                        font.fontnames.append(NameRecord(tuple(nr)))
                case F.CustomCMAPs:
                    font._custom_cmaps = data
                case F.PCLTTable:
                    font._pclt_table = data
                case F.ExportPCLTTable:
                    font._export_pclt_table = data
                case F.TrueTypeTable:
                    font.truetypetables.append(data)
                case F.MetricsClassFlags:
                    font._metrics_class_flags = data
                case F.KerningClassFlags:
                    font._kerning_class_flags = data
                case F.features:
                    font.fake_deserialize_features(data)
                case F.GlyphClass:
                    classes.append(data)
                case F.AxisCount:
                    font._axis_count = data
                case F.AxisName:
                    font.fake_deserialize_axis(data)
                case F.AnisotropicInterpolationMappings:
                    font._anisotropic_interpolation_mappings = data
                case F.AxisMappingsCount:
                    font._axis_mappings_count = data
                case F.AxisMappings:
                    font._axis_mappings = data
                case M.MasterName:
                    font._master_names.append(data)
                case M.MasterLocation:
                    font._master_locations.append(data)
                case F.PrimaryInstanceLocations:
                    font._primary_instance_locations = data
                case F.PrimaryInstances:
                    font._primary_instances = data
                case M.PostScriptInfo:
                    font._master_ps_infos.append(data)
                case F.GlobalGuides:
                    font.fake_deserialize_guides(data)
                case F.GlobalGuideProperties:
                    font.fake_deserialize_guide_properties(data)
                case F.GlobalMask:
                    pass
                case G.Glyph:
                    # Append the current glyph
                    if glyph is not None:
                        font.glyphs.append(glyph)
                    # Make a new glyph
                    logger.info(f"Adding Glyph: '{data.get('name')}', {key}")
                    glyph = Glyph()
                    # Add the data
                    glyph.fake_deserialize(2001, data)
                case F.OpenTypeExportOptions:
                    font._ot_export_options = data
                case F.ExportOptions:
                    font._export_options = data
                case F.MappingMode:
                    font._mapping_mode = data
                case F.E1410:
                    pass
                case _:
                    logger.error(f"Unhandled VFB entry: {key}")

        if glyph is not None:
            font.glyphs.append(glyph)

        if gids:
            enc = font._encoding = Encoding()
            enc._parent = font

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
            font._classes.fake_set_classes(classes)
