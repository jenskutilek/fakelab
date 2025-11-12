from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal, DefaultContext, setcontext
from typing import Any

from FL.objects.Point import Point

DefaultContext.rounding = ROUND_HALF_UP
setcontext(DefaultContext)


def add_axis_to_list(seq: list[Any]) -> None:
    """
    Adjust the length of a list in place by duplicating it (= adding an MM axis).

    Args:
        seq (list[Any]): The list to be adjusted.
    """
    if not seq:
        return

    if isinstance(seq[0], Point):
        new_values = [Point(p) for p in seq]
    else:
        new_values = [v for v in seq]

    seq.extend(new_values)


def add_axis_to_master_list(seq: list[list[Any]]) -> None:
    """
    Add an axis to a 2d list of values per master. Top level index is the master index.

    Args:
        seq (list[list[Any]]): The list to be adjusted.
    """
    if not seq[0]:
        return

    if isinstance(seq[0][0], Point):
        new_values = [[Point(p) for p in seq[m]] for m in range(len(seq))]
    else:
        new_values = [[v for v in seq[m]] for m in range(len(seq))]

    seq.extend(new_values)


def remove_axis_from_list(seq: list[int], interpolation: float) -> None:
    """
    Adjust the length of a list in place by halving it (= removing an MM axis).
    The interpolation factor will be used to interpolate the remaining values.

    Args:
        seq (list[Any]): The list to be adjusted.
        interpolation (float, optional): The interpolation factor. Defaults to 0.0.

    Raises:
        ValueError: If the list has an odd number of elements.
    """
    num_values = len(seq)
    if num_values % 2:
        raise ValueError(f"List must have an even number of elements: {seq}")

    half = num_values // 2
    # TODO: Add fast path for interpolation value 0 and 1?
    for i in range(half):
        seq[i] = interpolate(seq[i], seq[half + i], interpolation)
    for i in range(half):
        seq.pop()


def remove_axis_from_factor_list(seq: list[float]) -> None:
    """
    Like `remove_axis_from_list`, but adds the values instead of interpolating them.
    Used for reducing the `Font.weight_vector` list.

    Args:
        seq (list[float]): The list to be adjusted.

    Raises:
        ValueError: If the list has an odd number of elements.
    """
    num_values = len(seq)
    if num_values % 2:
        raise ValueError(f"List must have an even number of elements: {seq}")

    half = num_values // 2
    for i in range(half):
        seq[i] = seq[i] + seq[half + i]
    for i in range(half):
        seq.pop()


def remove_axis_from_master_list(seq: list[list[int]], interpolation: float) -> None:
    """
    Remove an axis from a 2d list of values per master. Top level index is the master
    index. The interpolation factor will be used to interpolate the remaining values.

    Args:
        seq (list[list[int]]): The list of masters and values to be adjusted.
        interpolation (float, optional): The interpolation factor. Defaults to 0.0.

    Raises:
        ValueError: If the list has an odd number of elements.
    """
    num_masters = len(seq)
    if num_masters % 2:
        raise ValueError(f"List must have an even number of elements: {seq}")

    half = num_masters // 2
    num_values = len(seq[0])
    new_values: list[list[int]] = [[] for _ in range(half)]
    for v in range(num_values):
        master_values = []
        for m in range(num_masters):
            master_values.append(seq[m][v])
        remove_axis_from_list(master_values, interpolation)
        for m, value in enumerate(master_values):
            new_values[m].append(value)

    for v in range(num_values):
        for m in range(half):
            seq[m][v] = new_values[m][v]
    for _ in range(half):
        seq.pop()


def remove_axis_from_point_list(seq: list[Point], interpolation: float) -> None:
    """
    Adjust the length of a list in place by halving it (= removing an MM axis).
    The interpolation factor will be used to interpolate the remaining points.

    Args:
        seq (list[Point]): The list of points to be adjusted.
        interpolation (float, optional): The interpolation factor. Defaults to 0.0.

    Raises:
        ValueError: If the list has an odd number of elements.
    """
    num_values = len(seq)
    if num_values % 2:
        raise ValueError(f"List must have an even number of elements: {seq}")

    half = num_values // 2
    # TODO: Add fast path for interpolation value 0 and 1?
    for i in range(half):
        seq[i] = interpolate_point(seq[i], seq[half + i], interpolation)
    for i in range(half):
        seq.pop()


def remove_axis_from_master_point_list(
    seq: list[list[Point]], interpolation: float
) -> None:
    """
    Remove an axis from a 2d list of points per master. Top level index is the master
    index. The interpolation factor will be used to interpolate the remaining points.

    Args:
        seq (list[list[Point]]): The list of masters and points to be adjusted.
        interpolation (float, optional): The interpolation factor. Defaults to 0.0.

    Raises:
        ValueError: If the list has an odd number of elements.
    """
    num_masters = len(seq)
    if num_masters % 2:
        raise ValueError(f"List must have an even number of elements: {seq}")

    half = num_masters // 2
    num_values = len(seq[0])
    new_points: list[list[Point]] = [[] for _ in range(half)]
    for v in range(num_values):
        master_points = []
        for m in range(num_masters):
            master_points.append(seq[m][v])
        remove_axis_from_point_list(master_points, interpolation)
        for m, point in enumerate(master_points):
            new_points[m].append(point)

    for v in range(num_values):
        for m in range(half):
            seq[m][v].Assign(new_points[m][v])
    for _ in range(half):
        seq.pop()


def interpolate(v0: float, v1: float, factor: float) -> int:
    return int(round(Decimal(str(interpolate_float(v0, v1, factor))), 0))


def interpolate_float(v0: float, v1: float, factor: float) -> float:
    return v0 + (v1 - v0) * factor


    # TODO: Do we need to round at all?
def interpolate_point(p0: Point, p1: Point, factor: float) -> Point:
    return round(p0 + (p1 - p0) * factor)
