import unittest

from FL.objects.Guide import Guide


class GuideTests(unittest.TestCase):
    def test_instantiation(self) -> None:
        g = Guide()
        assert g.parent is None
        assert g.position == 0
        assert g.width == 21
        assert g.positions == [0] * 16
        assert g.widths == [21] * 16

    def test_angle_45(self) -> None:
        # An angle of 45° is converted to 10000 in the widths list
        g = Guide()
        g.angle = 45
        assert g.width == 10000

    def test_angle_40(self) -> None:
        # An angle of 40° is converted to 8391 in the widths list
        g = Guide()
        g.angle = 40
        assert g.width == 8391
        # ... and converted back with limited precision
        # FIXME: Use actual precision
        # assert g.angle == 40.0000114441
        assert g.angle == 40.000012400755736

    def test_angle_60(self) -> None:
        # An angle of 60° is clamped to 45° (10000 in the widths list)
        g = Guide()
        g.angle = 60
        assert g.width == 10000
        assert g.angle == 45.0

    def test_angle_mm(self) -> None:
        # Setting the angle sets it for all masters
        g = Guide()
        g.angle = 45
        assert g.widths == [10000] * 16

    def test_position_mm(self) -> None:
        # Setting the position sets it for all masters
        g = Guide()
        g.position = 100
        assert g.positions == [100] * 16

    def test_width_mm(self) -> None:
        # Setting the "width" sets it for all masters
        g = Guide()
        g.width = 100
        assert g.widths == [100] * 16
