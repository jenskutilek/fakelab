from __future__ import annotations

import unittest

from FL.helpers.interpolation import (
    add_axis_to_list,
    add_axis_to_master_list,
    interpolate,
    interpolate_point,
    remove_axis_from_list,
    remove_axis_from_master_list,
    remove_axis_from_master_point_list,
    remove_axis_from_point_list,
    round_float,
    round_float_list,
    round_master_float_list,
    round_master_point_list,
    round_point,
    round_point_list,
)
from FL.objects.Point import Point


class FLListTests(unittest.TestCase):
    def test_add_axis_to_list(self) -> None:
        seq = [1, 0]
        add_axis_to_list(seq)
        assert seq == [1, 0, 1, 0]

    def test_add_axis_to_list_points(self) -> None:
        seq = [Point(1, 0)]
        add_axis_to_list(seq)
        assert seq == [Point(1, 0), Point(1, 0)]

    def test_add_axis_to_master_list(self) -> None:
        seq = [[1, 2], [3, 4]]
        add_axis_to_master_list(seq)
        assert seq == [[1, 2], [3, 4], [1, 2], [3, 4]]

    def test_add_axis_to_master_list_points(self) -> None:
        seq = [[Point(1, 2)], [Point(3, 4)]]
        add_axis_to_master_list(seq)
        assert seq == [[Point(1, 2)], [Point(3, 4)], [Point(1, 2)], [Point(3, 4)]]

    def test_remove_axis_from_list_1(self) -> None:
        seq = [1, 0, 10, 2]
        remove_axis_from_list(seq, index=1, interpolation=0.5, round_values=False)
        assert seq == [5.5, 1]

    def test_remove_axis_from_list_1_r(self) -> None:
        seq = [1, 0, 10, 2]
        remove_axis_from_list(seq, index=1, interpolation=0.5, round_values=True)
        assert seq == [6, 1]

    def test_remove_axis_from_master_list_1(self) -> None:
        seq = [[1, 0], [10, 2]]
        remove_axis_from_master_list(
            seq, index=1, interpolation=0.5, round_values=False
        )
        assert seq == [[5.5, 1]]

    def test_remove_axis_from_master_list_1_r(self) -> None:
        seq = [[1, 0], [10, 2]]
        remove_axis_from_master_list(seq, index=1, interpolation=0.5, round_values=True)
        assert seq == [[6, 1]]

    def test_remove_axis_from_point_list_1(self) -> None:
        seq = [Point(1, 0), Point(10, 2)]
        remove_axis_from_point_list(seq, index=1, interpolation=0.5, round_values=False)
        assert seq == [Point(5.5, 1)]

    def test_remove_axis_from_point_list_1_r(self) -> None:
        seq = [Point(1, 0), Point(10, 2)]
        remove_axis_from_point_list(seq, index=1, interpolation=0.5, round_values=True)
        # In interpolation, points are rounded, not truncated.
        assert seq == [Point(6, 1)]

    def test_remove_axis_from_master_point_list_1(self) -> None:
        seq = [[Point(1, 0), Point(0, 100)], [Point(10, 2), Point(10, 200)]]
        remove_axis_from_master_point_list(
            seq, index=1, interpolation=0.5, round_values=False
        )
        assert seq == [[Point(5.5, 1), Point(5, 150)]]

    def test_remove_axis_from_master_point_list_1_r(self) -> None:
        seq = [[Point(1, 0), Point(0, 100)], [Point(10, 2), Point(10, 200)]]
        remove_axis_from_master_point_list(
            seq, index=1, interpolation=0.5, round_values=True
        )
        # In interpolation, points are rounded, not truncated.
        assert seq == [[Point(6, 1), Point(5, 150)]]

    def test_interpolate_zero(self) -> None:
        result = interpolate(0, 1, 0.0)
        assert result == 0

    def test_interpolate_round_even(self) -> None:
        result = interpolate(0, 2, 0.5)
        assert result == 1

    def test_interpolate_round(self) -> None:
        result = interpolate(0, 1, 0.5)
        result = round_float(result)
        assert result == 1

    def test_interpolate_round_reversed(self) -> None:
        result = interpolate(1, 0, 0.5)
        result = round_float(result)
        assert result == 1

    def test_interpolate_points(self) -> None:
        p = interpolate_point(Point(0, 16), Point(1, 10), 0.5)
        p = round(p)
        assert (p.x, p.y) == (0.0, 13.0)

    def test_interpolate_points_half(self) -> None:
        p = interpolate_point(Point(0, 16), Point(1, 10), 0.999)
        p = round(p)
        assert (p.x, p.y) == (0.0, 10.0)
