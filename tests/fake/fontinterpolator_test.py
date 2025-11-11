import unittest

from mutatorMath import Location, Mutator

from FL.fake.FontInterpolator import FontInterpolator
from FL.objects.Font import Font


class FontInterpolatorTests(unittest.TestCase):
    def test_instantiation(self) -> None:
        f = Font()
        FontInterpolator(f)

    def test_build_axis_map_1(self) -> None:
        f = Font()
        f._axis = [("Weight", "Wt", "Weight")]
        fi = FontInterpolator(f)
        result = fi._build_master_map()
        assert result == [(0,), (1,)]

    def test_build_axis_map_2(self) -> None:
        f = Font()
        f._axis = [("Weight", "Wt", "Weight"), ("Width", "Wd", "Width")]
        fi = FontInterpolator(f)
        result = fi._build_master_map()
        assert result == [(0, 0), (1, 0), (0, 1), (1, 1)]

    def test_build_axis_map_3(self) -> None:
        f = Font()
        f._axis = [
            ("Weight", "Wt", "Weight"),
            ("Width", "Wd", "Width"),
            ("Optical Size", "Op", "Optical Size"),
        ]
        fi = FontInterpolator(f)
        result = fi._build_master_map()
        assert result == [
            (0, 0, 0),
            (1, 0, 0),
            (0, 1, 0),
            (1, 1, 0),
            (0, 0, 1),
            (1, 0, 1),
            (0, 1, 1),
            (1, 1, 1),
        ]

    def test_build_axis_map_4(self) -> None:
        f = Font()
        f._axis = [
            ("Weight", "Wt", "Weight"),
            ("Width", "Wd", "Width"),
            ("Optical Size", "Op", "Optical Size"),
            ("Serif", "Se", "Serif"),
        ]
        fi = FontInterpolator(f)
        result = fi._build_master_map()
        assert result == [
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

    def test_ip_value_array(self) -> None:
        f = Font()
        f._axis = [("Weight", "Wt", "Weight"), ("Width", "Wd", "Width")]
        fi = FontInterpolator(f)
        fi.location = Location(wt=0.289, wd=0.479)  # TheSans SCd Plain
        values = [
            [-8, 0, 497, 505],  # wt0 wd0
            [-12, 0, 497, 509],  # wt1 wd0
            [-9, 0, 497, 506],  # wt0 wd1
            [-15, 0, 497, 512],  # wt1 wd1
        ]
        expected = [
            [-10, 0, 497, 507],
        ]
        result = fi._ip_value_array(4, values)
        assert result == expected
