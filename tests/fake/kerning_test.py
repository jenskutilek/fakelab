import unittest
from pathlib import Path

from FL.fake.Kerning import FakeKerning


class FakeKerningTests(unittest.TestCase):
    def test_instantiation_empty(self) -> None:
        k = FakeKerning()
        assert isinstance(k, FakeKerning)
        assert k._font is None
        assert k.kerning == {}
        assert k.flat_kerning == []
        assert k.classes == {"L": {}, "R": {}}
        assert k.classes_left == {}
        assert k.classes_right == {}

    def test_import_flc(self) -> None:
        k = FakeKerning()
        k.import_flc(Path(__file__).parent / "classes.flc")
        assert len(k.classes_left) == 2
        assert len(k.classes_right) == 1
        assert k.classes_left["A"].glyphs == [
            "Agrave",
            "Aacute",
            "Acircumflex",
            "Adieresis",
            "Aring",  # Aring has a trailing space in the FLC file!
        ]
        assert k.classes_left["Z"].glyphs == [
            "Zcaron",
            "Zacute",
            "Zdotaccent",
            "Zeta",
            "uni1E92",
            "uni1E94",
        ]
        assert k.classes_right["Z"].glyphs == [
            "Zcaron",
            "Zacute",
            "Zdotaccent",
            "Zeta",
            "uni1E92",
            "uni1E94",
        ]
