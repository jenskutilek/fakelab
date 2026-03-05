from typing import TYPE_CHECKING, Any

from vfbLib.typing import MMNode

from FL.constants import (
    json2vfb_node_conns,
    json2vfb_node_types,
    nCURVE,
    nLINE,
    nMOVE,
    nOFF,
    vfb2json_node_conns,
    vfb2json_node_types,
)
from FL.helpers.interpolation import (
    add_axis_to_master_list,
    remove_axis_from_master_point_list,
    round_master_point_list,
)
from FL.helpers.ListParent import ListParent
from FL.objects.base.Node import BaseNode
from FL.objects.Point import Point

if TYPE_CHECKING:
    from FL.objects.Glyph import Glyph


class FakeNode(BaseNode):
    def fake_deserialize(self, num_masters: int, data: dict[str, Any]) -> None:
        self._masters_count = num_masters
        self.type = vfb2json_node_types[data["type"]]
        self.alignment = vfb2json_node_conns[data["flags"]]
        self._points = [ListParent() for _ in range(self._masters_count)]
        points = data.get("points", [])
        for master_index in range(num_masters):
            master_points = points[master_index]
            if self.type in (nMOVE, nLINE, nOFF):
                assert len(master_points) == 1
            elif self.type == nCURVE:
                assert len(master_points) == 3
            else:
                raise ValueError(f"Unknown Node type: {self.type}")
            for x, y in master_points:
                self._points[master_index].append(Point(x, y))
        if self.type in (nMOVE, nLINE, nOFF):
            assert len(self.points) == 1
        elif self.type == nCURVE:
            assert len(self.points) == 3
        else:
            raise ValueError(f"Unknown Node type: {self.type}")

    def fake_serialize(self, num_masters: int) -> "MMNode":
        d = MMNode(
            type=json2vfb_node_types[self.type],
            flags=json2vfb_node_conns[self.alignment],
            points=[],
        )
        points: list[list[tuple[int, int]]] = [[] for _ in range(num_masters)]
        for master_index, master_points in enumerate(self._points):
            for p in master_points:
                points[master_index].append((int(p.x), int(p.y)))
        d["points"] = points
        return d

    def fake_update(self, glyph: "Glyph | None" = None) -> None:
        """
        Is called from FontLab.UpdateFont()
        """
        self._parent: "Glyph | None" = glyph
        for p in self.points:
            p.fake_update(self)

    def fake_add_axis(self) -> None:
        add_axis_to_master_list(self._points)
        self._masters_count *= 2

    def fake_remove_axis(
        self,
        axisindex: int,
        interpolation: float,
        round_values: bool = True,
        num_masters: int = -1,
    ) -> None:
        if len(self) == 0:
            return

        # print(
        #     f"Node.fake_remove_axis {axisindex} for type {self.type}: {self._points} ({interpolation})"
        # )

        remove_axis_from_master_point_list(
            self._points, axisindex, interpolation, round_values
        )
        self._masters_count //= 2
        if round_values:
            round_master_point_list(self._points)
        # print(f"                             Result: {self._points}")
