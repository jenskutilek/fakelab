from decimal import ROUND_HALF_UP, Decimal, DefaultContext, setcontext
from typing import TYPE_CHECKING, Any, TypedDict

from FL.objects.Point import Point

if TYPE_CHECKING:
    from FL.objects.Font import Font

DefaultContext.rounding = ROUND_HALF_UP
setcontext(DefaultContext)


class AxisDict(TypedDict):
    name: str
    minimum: float
    maximum: float
    default: float
    map: dict[float, float]


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


# from fontTools.varLib.models import piecewiseLinearMap
def piecewise_linear_map(v: float, mapping: dict[float, float]) -> float:
    keys = mapping.keys()
    if not keys:
        return v
    if v in keys:
        return mapping[v]
    k = min(keys)
    if v < k:
        return v + mapping[k] - k
    k = max(keys)
    if v > k:
        return v + mapping[k] - k
    # Interpolate
    a = max(k for k in keys if k < v)
    b = min(k for k in keys if k > v)
    va = mapping[a]
    vb = mapping[b]
    return va + (vb - va) * (v - a) / (b - a)


def build_axis_dict(font: "Font") -> dict[str, AxisDict]:
    # Build axis dicts with mappings that can be used to build a Mutator
    axis_mappings = read_axis_mappings(font)
    # _master_locations = font.fake_master_map()
    axis_dict: dict[str, AxisDict] = {}
    for a in range(font._axis_count):
        axis_name = font.axis[a][1].lower()
        mappings = axis_mappings.get(a, {})
        inputs = mappings.keys()
        range_min = min(inputs, default=0.0)
        range_max = max(inputs, default=1000.0)
        axis_dict[axis_name] = {
            "name": axis_name,
            "minimum": range_min,
            "maximum": range_max,
            "default": range_min,
            "map": mappings,
        }
    return axis_dict


def map_user_to_internal(user_value: float, axis_tag: str, axis_dict: dict) -> float:
    mapping = axis_dict[axis_tag].get("map")
    if not mapping:
        return user_value / 1000
    return piecewise_linear_map(user_value, mapping)


def read_axis_mappings(font: "Font") -> dict[int, dict[float, float]]:
    # Convert axis mappings from Font into a format mutatorMath understands
    offset = 0
    axis_mappings: dict[int, dict[float, float]] = {}
    for a in range(len(font.axis)):
        axis_mappings[a] = {}
        num_mappings = font._axis_mappings_count[a]
        for m in range(num_mappings):
            user, internal = font._axis_mappings[offset + m]
            axis_mappings[a][user] = internal
        offset += 10  # There are always 10 mappings stored
    return axis_mappings


def remove_axis_from_list(
    seq: list[int] | list[float],
    index: int,
    interpolation: float,
    round_values: float,
    num_masters: int = -1,
) -> None:
    """
    Adjust the length of a list in place by halving it (= removing an MM axis).
    The interpolation factor will be used to interpolate the remaining values.

    Args:
        seq (list[Any]): The list to be adjusted.
        interpolation (float, optional): The interpolation factor. Defaults to 0.0.

    Raises:
        ValueError: If the list has an odd number of elements.
    """
    if num_masters < 0:
        num_values = len(seq)
    else:
        num_values = num_masters

    if num_values % 2:
        raise ValueError(f"List must have an even number of elements: {seq}")

    half = num_values // 2
    # TODO: Add fast path for interpolation value 0 and 1?
    for i in range(half):
        seq[i] = interpolate(seq[i], seq[half + i], interpolation)
    for i in range(half):
        seq.pop()
    if round_values:
        round_float_list(seq)


def remove_axis_from_factor_list(seq: list[float], index: int) -> None:
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


def remove_axis_from_master_list(
    seq: list[list[int] | list[float]],
    index: int,
    interpolation: float,
    round_values: bool,
    num_masters: int = -1,
) -> None:
    """
    Remove an axis from a 2d list of values per master. Top level index is the master
    index. The interpolation factor will be used to interpolate the remaining values.

    Args:
        seq (list[list[int]]): The list of masters and values to be adjusted.
        interpolation (float, optional): The interpolation factor. Defaults to 0.0.

    Raises:
        ValueError: If the list has an odd number of elements.
    """
    if num_masters < 0:
        num_masters = len(seq)

    if num_masters % 2:
        raise ValueError(f"List must have an even number of elements: {seq}")

    half = num_masters // 2
    num_values = len(seq[0])
    new_values: list[list[int | float]] = [[] for _ in range(half)]
    for v in range(num_values):
        master_values = []
        for m in range(num_masters):
            master_values.append(seq[m][v])
        remove_axis_from_list(master_values, index, interpolation, round_values)
        for m, value in enumerate(master_values):
            new_values[m].append(value)

    for v in range(num_values):
        for m in range(half):
            seq[m][v] = new_values[m][v]
    for _ in range(half):
        seq.pop()
    if round_values:
        round_master_float_list(seq)


def remove_axis_from_point_list(
    seq: list[Point],
    index: int,
    interpolation: float,
    round_values: bool,
    num_masters: int = -1,
) -> None:
    """
    Adjust the length of a list in place by halving it (= removing an MM axis).
    The interpolation factor will be used to interpolate the remaining points.

    Args:
        seq (list[Point]): The list of points to be adjusted.
        interpolation (float, optional): The interpolation factor. Defaults to 0.0.

    Raises:
        ValueError: If the list has an odd number of elements.
    """
    if num_masters < 0:
        num_values = len(seq)
    else:
        num_values = num_masters

    if num_values % 2:
        raise ValueError(f"List must have an even number of elements: {seq}")

    half = num_values // 2
    # TODO: Add fast path for interpolation value 0 and 1?
    for i in range(half):
        seq[i] = interpolate_point(seq[i], seq[half + i], interpolation)
    for i in range(half):
        seq.pop()
    if round_values:
        round_point_list(seq)


def remove_axis_from_master_point_list(
    seq: list[list[Point]],
    index: int,
    interpolation: float,
    round_values: bool,
    num_masters: int = -1,
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
    if num_masters < 0:
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
        remove_axis_from_point_list(master_points, index, interpolation, round_values)
        for m, point in enumerate(master_points):
            new_points[m].append(point)

    for v in range(num_values):
        for m in range(half):
            seq[m][v].Assign(new_points[m][v])
    for _ in range(half):
        seq.pop()
    if round_values:
        round_master_point_list(seq)


def interpolate(v0: float, v1: float, factor: float) -> float:
    return v0 + (v1 - v0) * factor


def interpolate_point(p0: Point, p1: Point, factor: float) -> Point:
    return p0 + (p1 - p0) * factor


def round_float(value: float) -> int:
    return int(round(Decimal(str(value)), 0))


def round_float_list(values: list[float]) -> None:
    # Round a list of floats in place
    for i, value in enumerate(values):
        values[i] = round_float(value)


def round_master_float_list(floats: list[list[float]]) -> None:
    # Round a list of floats in place
    for sublist in floats:
        round_float_list(sublist)


def round_master_point_list(points: list[list[Point]]) -> None:
    # Round a list of points in place
    for sublist in points:
        round_point_list(sublist)


def round_point(point: Point) -> None:
    # Truncates
    point.x = round_float(point.x)
    point.y = round_float(point.y)


def round_point_list(points: list[Point]) -> None:
    # Round a list of points in place
    for point in points:
        round_point(point)
