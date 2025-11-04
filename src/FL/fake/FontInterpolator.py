from __future__ import annotations

from typing import TYPE_CHECKING

from mutatorMath import Location, Mutator
from mutatorMath.objects.mutator import buildMutator

if TYPE_CHECKING:
    from FL.objects.Font import Font


class FontInterpolator:
    def __init__(self, src_font: Font) -> None:
        """Interpolate an instance of a MM font

        Args:
            src_font (Font): The source font, multiple or single master. If the font
                contains no axes, a 1:1 copy of the font will be returned.
        """
        self._src = src_font
        self._num_axes = len(self._src.axis)
        self._num_masters = self._num_axes**2
        self._read_axis_mappings()

    def interpolate(self, values: tuple[float, ...], tgt_font: Font) -> None:
        """Do the interpolation and return the interpolated font.

        Args:
            values (tuple[float, ...]): A tuple containing interpolation values for
                all MM axes defined in the MM font. The values refer to the axis
                mappings defined in Font._axis_mappings. If there are more values than
                axes, the additional values are silently ignored. Float values are
                truncated to int.
            tgt_font (Font): The target font.
        """
        self._tgt = tgt_font
        if self._num_axes == 0:
            # Makes a direct copy of the font.
            self._tgt._copy_constructor(self._src)
            return

        self.location = self._map_location(values)

        self._ip_fontinfo()
        self._ip_glyphs()
        self._ip_guides_global()
        self._ip_hinting

    def _map_location(self, values: tuple[float, ...]) -> Location:
        # Map the input axis values to internal scale (0-1)

        return Location({f"a{i}": v for i, v in enumerate(values)})

    def _read_axis_mappings(self) -> None:
        # Convert axis mappings from Font into a format mutatorMath understands
        pass

    # Interpolation methods for the different MM parts

    def _ip_fontinfo(self) -> None:
        self._tgt.blue_values = self._ip_value_array(
            self._src.blue_values_num, self._src.blue_values
        )

    def _ip_glyphs(self) -> None:
        pass

    def _ip_guides_global(self) -> None:
        pass

    def _ip_hinting(self) -> None:
        pass

    # Lower level

    def _build_axis_map(self) -> list[tuple[int, ...]]:
        match self._num_axes:
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

    def _build_mutator(self, master_values: list[int]) -> Mutator:
        locations = self._build_axis_map()
        items = []

        m = 0
        for location_tuple in locations:
            loc_dict: dict[str, int] = {}
            for i in range(len(location_tuple)):
                loc_dict[self._src.axis[i][1].lower()] = location_tuple[i]
            items.append((Location(loc_dict), master_values[m]))
            m += 1

        _, mb = buildMutator(items)
        return mb

    def _ip_value_array(
        self, num_values: int, values: list[list[int]]
    ) -> list[list[int]]:
        # Interpolate a 2d array, e.g. blue values
        # one array per master, master index is the top-level index

        result: list[int] = []
        print(
            f"Interpolating {self._num_masters} masters with location {self.location} ..."
        )
        for i in range(num_values):
            master_values = [values[m][i] for m in range(self._num_masters)]
            mutator = self._build_mutator(master_values)
            result.append(round(mutator.makeInstance(self.location)))

        return [result]
