from __future__ import annotations

import logging
from copy import deepcopy
from typing import TYPE_CHECKING

from mutatorMath import Location, Mutator
from mutatorMath.objects.mutator import buildMutator
from typing_extensions import TypedDict

from FL.helpers.interpolation import piecewise_linear_map

if TYPE_CHECKING:
    from FL.objects.Font import Font
    from FL.objects.Glyph import Glyph
    from FL.objects.Guide import Guide
    from FL.objects.Hint import Hint
    from FL.objects.Point import Point


logger = logging.getLogger(__name__)


class AxisDict(TypedDict):
    name: str
    minimum: float
    maximum: float
    default: float
    map: dict[float, float]


class FontInterpolator:
    def __init__(self, font: Font) -> None:
        """Interpolate an instance of a MM font

        Args:
            font (Font): The source font, multiple or single master. If the font
                contains no axes, a 1:1 copy of the font will be returned.
        """
        logger.warning(f"Opening font: {font}")
        # FIXME: We need to get rid of the vfb object in the font.
        # Right now, we need to temporarily null it so deepcopy can make a copy of the
        # font.
        vfb_obj = font.fake_vfb_object
        font.fake_vfb_object = None
        self._font = deepcopy(font)
        font.fake_vfb_object = vfb_obj

        self._num_axes = len(self._font.axis)
        self._num_masters = 2**self._num_axes

        self._build_axis_dicts()

    def interpolate(
        self,
        values: tuple[float, ...],
        family_name: str | None = None,
        style_name: str | None = None,
    ) -> None:
        """Do the interpolation and return the interpolated font.

        Args:
            values (tuple[float, ...]): A tuple containing interpolation values for
                all MM axes defined in the MM font. The values refer to the axis
                mappings defined in Font._axis_mappings. If there are more values than
                axes, the additional values are silently ignored. Float values are
                truncated to int.
            tgt_font (Font): The target font.
        """
        if self._num_axes == 0:
            logger.warning("Number of axes is 0, font is not modified.")
            return
        significant_values = values[: self._num_axes]
        self.location_user = self._map_location_user(significant_values)
        self.location = self._map_location(significant_values)

        self._ip_fontinfo()
        self._ip_glyphs()
        self._ip_guides_global()

        self._font._anisotropic_interpolation_mappings.clear()
        self._font._primary_instance_locations.clear()
        self._font._primary_instances.clear()
        self._font.weight_vector[0] = 1.0
        self._font.weight_code = int(self.location_user["wt"])
        self._font._axis.clear()
        self._font._axis_mappings_count = [0, 0, 0, 0]
        self._font._axis_mappings = [(0.0, 0.0)] * 40
        self._font._masters_count = 1

        if family_name:
            self._font.pref_family_name = family_name
        if style_name:
            self._font.pref_style_name = "Regular"  # TODO: Always?
            self._font.style_name = style_name
            if self._font.family_name is not None:
                self._font.font_name = f"{self._font.family_name.replace(' ', '')}-{style_name.replace(' ', '')}"
                self._font.full_name = f"{self._font.family_name} {style_name}"
            if self._font.apple_name is not None:
                self._font.apple_name += f" {style_name}"
        self._font._master_names = ["Untitled"]

    def _build_axis_dicts(self) -> None:
        # Build axis dicts with mappings that can be used to build a Mutator
        self._read_axis_mappings()
        self._master_locations = self._font.fake_master_map()
        self._axis_dict: dict[str, AxisDict] = {}
        for a in range(self._num_axes):
            axis_name = self._font.axis[a][1].lower()
            mappings = self.axis_mappings.get(a, {})
            inputs = mappings.keys()
            range_min = min(inputs, default=0.0)
            range_max = max(inputs, default=1000.0)
            self._axis_dict[axis_name] = {
                "name": axis_name,
                "minimum": range_min,
                "maximum": range_max,
                "default": range_min,
                "map": mappings,
            }

    def _map_user_to_internal(self, user_value: float, axis_tag: str) -> float:
        mapping = self._axis_dict[axis_tag].get("map")
        if not mapping:
            return user_value / 1000
        return piecewise_linear_map(user_value, mapping)

    def _map_location(self, values: tuple[float, ...]) -> Location:
        # Map the input axis values, one per axis, to internal scale (0-1)

        return Location(
            {
                self._font.axis[i][1].lower(): self._map_user_to_internal(
                    v, self._font.axis[i][1].lower()
                )
                for i, v in enumerate(values)
            }
        )

    def _map_location_user(self, values: tuple[float, ...]) -> Location:
        # The location in user coordinates

        return Location(
            {
                self._font.axis[i][1].lower(): v
                for i, v in enumerate(values[: self._num_axes])
            }
        )

    def _read_axis_mappings(self) -> None:
        # Convert axis mappings from Font into a format mutatorMath understands
        offset = 0
        self.axis_mappings: dict[int, dict[float, float]] = {}
        for a in range(len(self._font.axis)):
            self.axis_mappings[a] = {}
            num_mappings = self._font._axis_mappings_count[a]
            for m in range(num_mappings):
                user, internal = self._font._axis_mappings[offset + m]
                self.axis_mappings[a][user] = internal
            offset += 10  # There are always 10 mappings stored

    # Interpolation methods for the different MM parts

    def _ip_fontinfo(self) -> None:
        f = self._font

        # Key dimensions

        f.ascender[0] = self._ip_value(f.ascender)
        f.descender[0] = self._ip_value(f.descender)
        f.cap_height[0] = self._ip_value(f.cap_height)
        f.x_height[0] = self._ip_value(f.x_height)
        f.default_width[0] = self._ip_value(f.default_width)

        # Interpolate blue zones

        logger.warning("blue_scale is not interpolated yet")
        logger.warning("blue_shift is not interpolated yet")
        logger.warning("blue_fuzz is not interpolated yet")
        f.fake_set_master_blue_values(
            self._ip_value_array(f.blue_values_num, f.blue_values)[0]
        )
        f.fake_set_master_other_blues(
            self._ip_value_array(f.other_blues_num, f.other_blues)[0]
        )
        f.fake_set_family_blues(
            self._ip_value_array(f.family_blues_num, f.family_blues)[0]
        )
        f.fake_set_family_other_blues(
            self._ip_value_array(f.family_other_blues_num, f.family_other_blues)[0]
        )

        # Interpolate stems

        # We don't need to reduce the number of _master_ps_infos, there are alway 16.

        f._master_ps_infos[0]["std_hw"] = self._ip_value_limit(
            self._num_masters, [psinfo["std_hw"] for psinfo in f._master_ps_infos]
        )
        f._master_ps_infos[0]["std_vw"] = self._ip_value_limit(
            self._num_masters, [psinfo["std_vw"] for psinfo in f._master_ps_infos]
        )
        f._master_ps_infos[0]["stem_snap_h"] = self._ip_value_array(
            f.stem_snap_h_num, f.stem_snap_h
        )[0]
        f._master_ps_infos[0]["stem_snap_v"] = self._ip_value_array(
            f.stem_snap_v_num, f.stem_snap_v
        )[0]

        # TODO: TrueType stems

        # TODO: Font Matrix?

        # TODO:
        # recalculate bounding box, adv_width_min, adv_width_max

    def _ip_glyphs(self) -> None:
        for g in self._font.glyphs:
            self._ip_nodes(g)
            self._ip_anchors(g)
            self._ip_hints(g)
            self._ip_guides(g)
            self._ip_components(g)
            self._ip_kerning(g)
            g._metrics = self._ip_point(g._metrics)
            self._ip_mask(g)
            self._ip_vsb(g)
            g._layers_number = 1

    def _ip_guides_global(self) -> None:
        pass

    # Shared

    def _ip_guide(self, g: Guide) -> None:
        pass

    # Glyph

    def _ip_anchors(self, g: Glyph) -> None:
        pass

    def _ip_components(self, g: Glyph) -> None:
        pass

    def _ip_guides(self, g: Glyph) -> None:
        for guide in g._hguides:
            self._ip_guide(guide)
        for guide in g._vguides:
            self._ip_guide(guide)

    def _ip_hint(self, h: Hint) -> None:
        pass

    def _ip_hints(self, g: Glyph) -> None:
        for h in g._hhints:
            self._ip_hint(h)
        for h in g._vhints:
            self._ip_hint(h)

    def _ip_kerning(self, g: Glyph) -> None:
        pass

    def _ip_mask(self, g: Glyph) -> None:
        if g._mask is None:
            return

        g._mask_weight_vector = [g._mask_weight_vector[0]]
        self._ip_nodes(g._mask)
        if g._mask_metrics is None or g._mask_metrics_mm is None:
            return

        mask_metrics = [[g._mask_metrics]]
        for pt in g._mask_metrics_mm:
            mask_metrics.append([pt])

        g._mask_metrics = self._ip_point_array(mask_metrics)[0][0]
        g._mask_metrics_mm = None

    def _ip_nodes(self, g: Glyph) -> None:
        for n in g.nodes:
            n._points = self._ip_point_array(n._points)

    def _ip_vsb(self, g: Glyph) -> None:
        if not g._vsb:
            return

        g._vsb = [self._ip_value(g._vsb)]

    # Lower level

    def _build_mutator(self, master_values: list[int]) -> Mutator:
        # XXX: Do we have to do this for each value, or can we build the Mutator once,
        # and then reassign the master values?
        items = []

        m = 0
        for location_tuple in self._master_locations:
            loc_dict: dict[str, int] = {}
            for i in range(len(location_tuple)):
                loc_dict[self._font.axis[i][1].lower()] = location_tuple[i]
            items.append((Location(loc_dict), master_values[m]))
            m += 1

        if self._axis_dict:
            _, mb = buildMutator(items, self._axis_dict)
        else:
            _, mb = buildMutator(items)
        return mb

    def _ip_point(self, points: list[Point]) -> list[Point]:
        """
        Interpolate a Point array, e.g. metrics.

        Args:
            points (list[Point]): The 2d array of Points.

        Returns:
            list[Point]: The interpolated Point in a list.
        """
        px = []
        py = []
        for master_index in range(len(points)):
            px.append(points[master_index].x)
            py.append(points[master_index].y)
            # TODO: Anisotropic interpolation
        rx = self._ip_value(px)
        ry = self._ip_value(py)
        points[0].x = rx
        points[0].y = ry
        return [points[0]]

    def _ip_point_array(self, points: list[list[Point]]) -> list[list[Point]]:
        """
        Interpolate a 2d Point array, e.g. a node. One array per master, master index
        is the top-level index.

        Args:
            points (list[list[Point]]): The 2d array of Points.

        Returns:
            list[list[Point]]: The interpolated Points.
        """
        num_points = len(points[0])

        px = []
        py = []
        for master_index in range(len(points)):
            px.append([p.x for p in points[master_index]])
            py.append([p.y for p in points[master_index]])
            # TODO: Anisotropic interpolation
        rx = self._ip_value_array(num_points, px)
        ry = self._ip_value_array(num_points, py)
        for i in range(len(rx[0])):
            points[0][i].x = rx[0][i]
            points[0][i].y = ry[0][i]
        return [points[0]]  # Shorten the list to 1 master

    def _ip_value_array(
        self, num_values: int, values: list[list[int]]
    ) -> list[list[int]]:
        """
        Interpolate a 2d array, e.g. blue values. One array per master, master index
        is the top-level index.

        Args:
            num_values (int): The number of values from the array that will be
                considered. The resulting inner list will have this amount of members.
            values (list[list[int]]): The 2d array of values.

        Returns:
            list[list[int]]: The interpolated array.
        """
        result: list[int] = []
        # print(
        #     f"Interpolating {self._num_masters} masters with location {self.location} ..."
        # )
        for i in range(num_values):
            master_values = [values[m][i] for m in range(self._num_masters)]
            mutator = self._build_mutator(master_values)
            result.append(round(mutator.makeInstance(self.location)))

        return [result]

    def _ip_value_limit(self, num_values: int, master_values: list[int]) -> int:
        """
        Interpolate a list of values, 1 value per master. The processing is limited to
        the first `num_values` values.

        Args:
            num_values (int): The number of values from the array that will be
                considered.
            master_values (list[int]): The array of values.

        Returns:
            int: The interpolated value.
        """
        mutator = self._build_mutator(master_values[:num_values])
        return round(mutator.makeInstance(self.location))

    def _ip_value(self, master_values: list[int]) -> int:
        """
        Interpolate a list of values, 1 value per master.

        Args:
            master_values (list[int]): The array of values.

        Returns:
            int: The interpolated value.
        """
        mutator = self._build_mutator(master_values)
        return round(mutator.makeInstance(self.location))
