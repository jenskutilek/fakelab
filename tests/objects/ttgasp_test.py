import unittest


from FL.objects.TTGasp import TTGasp


class TTGaspTests(unittest.TestCase):
    def test_instantiation(self) -> None:
        # No args
        t = TTGasp()
        assert t.ppm == 1000
        assert t.behavior == 0

    def test_instantiation_copy(self) -> None:
        # Use the copy constructor
        t0 = TTGasp()
        t0.ppm = 16
        t0.behavior = 6

        t = TTGasp(t0)
        assert t.ppm == 16
        assert t.behavior == 6

    def test_instantiation_args(self) -> None:
        # Initialize with ppm and behavior
        t = TTGasp(100, 15)
        assert t.ppm == 100
        assert t.behavior == 15
