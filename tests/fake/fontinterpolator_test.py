import unittest

from mutatorMath import Location, Mutator

from FL.fake.FontInterpolator import FontInterpolator
from FL.objects.Font import Font


class FontInterpolatorTests(unittest.TestCase):
    def test_instantiation(self) -> None:
        f = Font()
        FontInterpolator(f)

    def test_ip_value_array(self) -> None:
        f = Font()
        f.DefineAxis("Weight", "Weight", "Wt")
        f.DefineAxis("Width", "Width", "Wd")
        fi = FontInterpolator(f)
        fi.location = Location(wt=0.289, wd=0.472)  # TheSans SCd Plain
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

    def test_ip_value_limit(self) -> None:
        f = Font()
        f.DefineAxis("Weight", "Weight", "Wt")
        f.DefineAxis("Width", "Width", "Wd")
        fi = FontInterpolator(f)
        fi.location = Location(wt=0.289, wd=0.472)  # TheSans SCd Plain
        values = [
            505,  # wt0 wd0
            509,  # wt1 wd0
            506,  # wt0 wd1
            512,  # wt1 wd1
        ]
        expected = 507
        result = fi._ip_value_limit(4, values)
        assert result == expected

    def test_ip_value(self) -> None:
        f = Font()
        f.DefineAxis("Weight", "Weight", "Wt")
        f.DefineAxis("Width", "Width", "Wd")
        fi = FontInterpolator(f)
        fi.location = Location(wt=0.289, wd=0.472)  # TheSans SCd Plain
        values = [
            505,  # wt0 wd0
            509,  # wt1 wd0
            506,  # wt0 wd1
            512,  # wt1 wd1
        ]
        expected = 507
        result = fi._ip_value(values)
        assert result == expected
