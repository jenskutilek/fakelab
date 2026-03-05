import logging
from copy import deepcopy
from pathlib import Path

from vfbLib.enum import G
from vfbLib.parsers.text import OpenTypeStringParser
from vfbLib.typing import GlyphData, PSInfoDict

from FL.fake.FontInterpolator import FontInterpolator
from FL.fake.Kerning import FakeKerning
from FL.fake.mixins import GuideMixin, GuidePropertiesMixin
from FL.fake.PSInfo import get_default_ps_info
from FL.helpers.FLList import adjust_list
from FL.objects.base.Font import BaseFont
from FL.objects.Feature import Feature
from FL.objects.Glyph import Glyph
from FL.objects.Rect import Rect
from FL.objects.Uni import Uni

__doc__ = """
Base class for Font
"""


logger = logging.getLogger(__name__)


class FakeFont(BaseFont, GuideMixin, GuidePropertiesMixin):
    def __init__(self) -> None:
        # Additions for FakeLab

        super().__init__()
        self._fake_kerning = FakeKerning(self)
        self.fake_sparse_json = True
        self.fake_deselect_all()

    # Additional properties for FakeLab

    def fake_clear_defaults(self) -> None:
        """
        Clear some lists prior to deserializing a font from a Vfb.
        """
        self._master_names.clear()
        self._master_locations.clear()
        self._master_ps_infos.clear()

    @property
    def fake_kerning(self) -> FakeKerning:
        """
        Returns the `FL.fake.FakeKerning` object, which can be used to manipulate the
        font's kerning data.
        """
        return self._fake_kerning

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
            # print(g.name, gr)
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

    def fake_sort_glyphs(self, glyphs: list[Glyph]) -> list[Glyph]:
        glyph_order = tuple([rec.name for rec in self.encoding])
        sortable = [(glyph_order.index(glyph.name), glyph) for glyph in glyphs]
        sortable.sort()
        # print(sortable)
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

    def fake_update(self) -> None:
        """
        Is called from FontLab.UpdateFont()
        """
        for index, glyph in enumerate(self.glyphs):
            glyph.fake_update(self, index)

    def fake_deselect_all(self) -> None:
        """
        Deselect all glyphs. Is called from FontLab.Unselect().
        """
        self._selection: set[int] = set()

    def fake_select(self, gid: "str | Uni | int", value: bool | None = None) -> None:
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
        if isinstance(gid, int):
            glyph_index = gid
        elif isinstance(gid, Uni) or isinstance(gid, str):
            glyph_index = self.FindGlyph(gid)
        if glyph_index > -1:
            if value:
                self._selection |= {glyph_index}
            else:
                self._selection -= {glyph_index}

    def fake_set_class_flags(self, flags: list[str]) -> None:
        """
        Set the kerning class flags from a list of str ("L", "R", "LR", ...)
        """
        # FIXME: In the vfb, the flags are stored as tuples of two values. The second
        # value is 0, it's not clear what it represents. Maybe the width flag for
        # metrics classes?
        for i, f in enumerate(flags):
            self.SetClassFlags(i, "L" in f, "R" in f)

    def _set_file_name(self, filename: str | Path | None) -> None:
        """
        Make sure the file name (actually, the path) is stored as Path
        """
        if filename is None:
            self._file_name = None
            return

        self._file_name = Path(filename) if not isinstance(filename, Path) else filename

    def fake_generate_primary_instances(self) -> "list[FakeFont]":
        instances: "list[FakeFont]" = []
        # for inst_dict in self._primary_instances:
        #     print(inst_dict)
        #     interpolator = FontInterpolator(self)
        #     interpolator.interpolate(inst_dict["values"], style_name=inst_dict["name"])
        #     instances.append(interpolator._font)
        #     del interpolator
        inst_dict = self._primary_instances[11]
        # print(inst_dict)
        interpolator = FontInterpolator(self)
        interpolator.interpolate(inst_dict["values"], style_name=inst_dict["name"])
        instances.append(interpolator._font)
        del interpolator
        return instances

    def fake_deserialize_axis(self, data: str) -> None:
        # VFB stores only the long name of an axis.
        short_name = {
            "Weight": "Wt",
            "Width": "Wd",
            "Optical Size": "Op",
            "Serif": "Se",
        }.get(data, data[:2])
        self._axis.append((data, short_name, data))

    def fake_serialize_axis(self) -> list[str]:
        names = []
        for axis in self.axis:
            long, _, _ = axis
            names.append(long)
        return names

    def fake_deserialize_global_mask(self, data: GlyphData) -> None:
        self._global_mask: Glyph | None = Glyph(self._masters_count)
        self._global_mask.fake_deserialize(G.Glyph, data)

    def fake_serialize_global_mask(self) -> GlyphData:
        gm = self._global_mask
        return GlyphData(
            num_masters=gm.layers_number,
            nodes=[node.fake_serialize(gm.layers_number) for node in gm.nodes],
        )

    def fake_deserialize_features(self, features: list[str]) -> None:
        self._features.clean()
        features_dict = OpenTypeStringParser.build_fea_dict(features)
        prefix = features_dict.get("prefix")
        if prefix:
            self.ot_classes = "\n".join(prefix)
        for feature_dict in features_dict.get("features", []):
            feature = Feature(feature_dict["tag"], "\n".join(feature_dict["code"]))
            self.features.append(feature)

    def fake_serialize_features(self) -> list[str]:
        fea = []
        if self.ot_classes:
            fea.extend(self.ot_classes.splitlines())
            # FIXME: Do we need empty lines as separator?
            fea.append("\n")
        for feature in self.features:
            if feature.value is not None:
                fea.extend(feature.value.splitlines())
                fea.append("")
        return fea

    def fake_deserialize_master_ps_infos(self) -> None:
        # Master PS Infos are only stored for existing masters in the VFB, but for all
        # possible masters in the Font.
        num_entries = len(self._master_ps_infos)
        if num_entries < 16:
            for _ in range(16 - num_entries):
                self._master_ps_infos.append(get_default_ps_info())
        for info in self._master_ps_infos:
            # Trim down the lists to the actual number of values
            for key, num in (
                ("blue_values", self.blue_values_num),
                ("other_blues", self.other_blues_num),
                ("family_blues", self.family_blues_num),
                ("family_other_blues", self.family_other_blues_num),
                ("stem_snap_h", self.stem_snap_h_num),
                ("stem_snap_v", self.stem_snap_v_num),
            ):
                adjust_list(info[key], new_length=num, value=0)

    def fake_serialize_master_ps_infos(self) -> list[PSInfoDict]:
        infos = []
        for i in range(self._masters_count):
            info = deepcopy(self._master_ps_infos[i])
            # Adjust blues lists to full length
            for key, num in (
                ("blue_values", 14),
                ("other_blues", 10),
                ("family_blues", 14),
                ("family_other_blues", 10),
                ("stem_snap_h", 12),
                ("stem_snap_v", 12),
            ):
                adjust_list(info[key], new_length=num, value=0)
            infos.append(info)
        return infos

    def _fake_set_master_blues(
        self, key: str, values: list[int], num: int, master_index: int = 0
    ) -> None:
        # Assert that the number of passed values is within the allowed limit
        num_values = len(values)
        assert num_values <= num

        master_info = self._master_ps_infos[master_index]
        target_list = master_info[key]
        # Adjust to new length in all masters
        setattr(self, f"{key}_num", num_values)
        for i, value in enumerate(values):
            target_list[i] = value

    def fake_set_master_blue_values(
        self, values: list[int], master_index: int = 0
    ) -> None:
        """
        Set the blue values for a master.

        Args:
            values (list[int]): The values.
            master_index (int, optional): The master index. Defaults to 0.
        """
        self._fake_set_master_blues("blue_values", values, 14, master_index)

    def fake_set_master_other_blues(
        self, values: list[int], master_index: int = 0
    ) -> None:
        """
        Set the other blues values for a master.

        Args:
            values (list[int]): The values.
            master_index (int, optional): The master index. Defaults to 0.
        """
        self._fake_set_master_blues("other_blues", values, 10, master_index)

    def fake_set_family_blues(self, values: list[int], master_index: int = 0) -> None:
        """
        Set the family blues values for a master.

        Args:
            values (list[int]): The values.
            master_index (int, optional): The master index. Defaults to 0.
        """
        self._fake_set_master_blues("family_blues", values, 14, master_index)

    def fake_set_family_other_blues(
        self, values: list[int], master_index: int = 0
    ) -> None:
        """
        Set the family other blue values for a master.

        Args:
            values (list[int]): The values.
            master_index (int, optional): The master index. Defaults to 0.
        """
        self._fake_set_master_blues("family_other_blues", values, 10, master_index)

    def fake_map_axis_location(
        self, axis_index: int = -1, user_value: float = 0
    ) -> float:
        # FIXME
        return user_value / 1000

    def fake_master_map(self) -> list[tuple[int, ...]]:
        match self._axis_count:
            case 0:
                return []
            case 1:
                return [
                    (0,),
                    (1,),
                ]
            case 2:
                return [
                    (0, 0),
                    (1, 0),
                    (0, 1),
                    (1, 1),
                ]
            case 3:
                return [
                    (0, 0, 0),
                    (1, 0, 0),
                    (0, 1, 0),
                    (1, 1, 0),
                    (0, 0, 1),
                    (1, 0, 1),
                    (0, 1, 1),
                    (1, 1, 1),
                ]
            case 4:
                return [
                    (0, 0, 0, 0),
                    (1, 0, 0, 0),
                    (0, 1, 0, 0),
                    (1, 1, 0, 0),
                    (0, 0, 1, 0),
                    (1, 0, 1, 0),
                    (0, 1, 1, 0),
                    (1, 1, 1, 0),
                    (0, 0, 0, 1),
                    (1, 0, 0, 1),
                    (0, 1, 0, 1),
                    (1, 1, 0, 1),
                    (0, 0, 1, 1),
                    (1, 0, 1, 1),
                    (0, 1, 1, 1),
                    (1, 1, 1, 1),
                ]
            case _:
                raise ValueError("Only 1 to 4 axes are supported.")

    def fake_remove_axis(
        self, index: int, position: float, round_values: bool = True
    ) -> None:
        if self._axis_count == 0:
            # Ignore silently
            return

        assert index == self._axis_count - 1, "Can only remove the last axis for now"

        if self._global_mask is not None:
            self._global_mask.fake_remove_axis(index, position, round_values)

        # Remove axis from glyphs
        for glyph in self.glyphs:
            glyph.fake_remove_axis(index, position, round_values)

        for guide in self.hguides:
            guide.fake_remove_axis(index, position, round_values)
        for guide in self.vguides:
            guide.fake_remove_axis(index, position, round_values)

        # TODO: Remove axis from fontinfo (interpolate values)

        for attr in (
            self._ascender,
            self._descender,
            self._cap_height,
            self._x_height,
            self._default_width,
            # self.blue_fuzz,
            # self.blue_scale,
            # self.blue_shift,
            # self.force_bold,
            # self.stem_snap_h,
            # self.stem_snap_v,
        ):
            remove_axis_from_list(attr, index, position, round_values)
            # These always store all possible 16 masters, so we must extend them to the
            # full length again.
            adjust_list(attr, 16)

        # Remove axis from font
        self._axis.pop()
        self._axis_count = len(self._axis)

        self._masters_count //= 2

        remove_axis_from_factor_list(self.weight_vector._weights, index)
        adjust_list(self._anisotropic_interpolation_mappings, self._axis_count)

        # Primary instances
        if self._axis_count > 0:
            # FIXME: This seems a bit more complicated. Locations that are still inside
            # the design space must be recalculated, others zeroed.
            # remove_axis_from_list(self._primary_instance_locations, position)
            for p in self._primary_instances:
                values = list(p["values"])
                remove_axis_from_list(values, index, position, round_values=False)
                adjust_list(values, 4, 0.0)
                p["values"] = tuple(values)
        else:
            self._primary_instance_locations = []
            self._primary_instances = []

        # Remove master names, recalculate if there are any axes left
        self._master_names = []
        if self._axis_count > 0:
            base = ""
            for _, short_name, _ in self.axis:
                base += f"{short_name}%s "
            for loc in self.fake_master_map():
                self._master_names.append(base % loc)
        else:
            self._master_names = ["Untitled"]
