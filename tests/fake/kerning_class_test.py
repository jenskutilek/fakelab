import unittest

from FL.fake.KerningClass import KerningClass


class KerningClassTests(unittest.TestCase):
    def test_instantiation_empty(self) -> None:
        kc = KerningClass()
        assert isinstance(kc, KerningClass)
        assert kc.name is None
        assert kc.sides == ""
        assert kc.keyglyph is None
        assert kc.glyphs == []

    def test_instantiation_from_flclass(self) -> None:
        kc = KerningClass(fromFLClass="_LAT_A_1st: A' Adieresis Aacute")
        assert kc.name == "_LAT_A_1st"
        assert kc.sides == "L"  # derived from "1st"
        assert kc.keyglyph == "A"
        assert kc.glyphs == ["Adieresis", "Aacute"]
