import unittest


from FL.objects.TTStem import TTStem


class TTStemTests(unittest.TestCase):
    def test_instantiation(self) -> None:
        # No args
        t = TTStem()
        assert t.name == ""
        assert t.width == 0
        assert t.ppm2 == 0
        assert t.ppm3 == 0
        assert t.ppm4 == 0
        assert t.ppm5 == 0
        assert t.ppm6 == 0

    def test_instantiation_copy(self) -> None:
        # Use the copy constructor
        t0 = TTStem()
        t0.name = "Hello"
        t0.width = 120
        t0.ppm2 = 8
        t0.ppm3 = 10
        t0.ppm4 = 14
        t0.ppm5 = 34
        t0.ppm6 = 45

        t = TTStem(t0)
        assert t.name == "Hello"
        assert t.width == 120
        assert t.ppm2 == 8
        assert t.ppm3 == 10
        assert t.ppm4 == 14
        assert t.ppm5 == 34
        assert t.ppm6 == 45

    def test_instantiation_args(self) -> None:
        # Initialize with width and upm
        t = TTStem(100, 1000)
        assert t.name == ""
        assert t.width == 100
        assert t.ppm2 == 15
        assert t.ppm3 == 25
        assert t.ppm4 == 35
        assert t.ppm5 == 45
        assert t.ppm6 == 55
