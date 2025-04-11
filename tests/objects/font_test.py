import unittest
from pathlib import Path

import pytest

from FL import Feature, Font, Glyph, fl


class FontTests(unittest.TestCase):
    def test_instantiation(self):
        f = Font()
        assert isinstance(f, Font)

    def test_instantiation_path(self):
        vfb_path = Path(__file__).parent.parent.parent / "tests" / "data" / "empty.vfb"

        f = Font(str(vfb_path))
        assert len(fl) == 0
        fl.Add(f)
        assert len(fl) == 1
        assert f.file_name == str(vfb_path)

    def test_add_glyph(self):
        f = Font()
        assert len(f) == 0
        f.glyphs.append(Glyph())
        assert len(f) == 1

    def test_find_glyph(self):
        f = Font()
        g = Glyph()
        g.name = "adieresis"
        f.glyphs.append(g)

        # Glyph in font with index 0
        i = f.FindGlyph("adieresis")
        assert i == 0

        # Glyph not in font
        i = f.FindGlyph("a")
        assert i == -1

    def test_features_readonly(self):
        f = Font()
        with pytest.raises(RuntimeError):
            f.features = []

    def test_features_iadd_freeze(self):
        f = Font()
        with pytest.raises(ReferenceError):
            f.features += Feature()

    def test_features_setitem(self):
        f = Font()
        fea = Feature("aaaa")
        f.features.append(fea)
        assert len(f.features) == 1
        assert fea.parent == f
        fea = Feature("bbbb")
        f.features[0] = fea
        assert len(f.features) == 1
        assert fea.parent == f
        assert f.features[0].tag == "bbbb"

    def test_features_setslice(self):
        # FIXME
        f = Font()
        f.features.append(Feature("aaaa"))
        f.features.append(Feature("bbbb"))
        assert len(f.features) == 2
        # Will actually raise an IndexError, only [0:1] works in FL if the feature
        # list has two elements:
        # f.features[0:2] = [Feature("cccc"), Feature("dddd")]
        # assert f.features[0].parent == f
        # assert f.features[0].tag == "cccc"
        # assert f.features[1].parent == f
        # assert f.features[1].tag == "dddd"

    def test_features_append(self):
        f = Font()
        fea = Feature()
        f.features.append(fea)
        assert len(f.features) == 1
        assert fea.parent == f

    def test_fontnames_readonly(self):
        f = Font()
        with pytest.raises(RuntimeError):
            f.fontnames = []

    def test_glyphs_readonly(self):
        f = Font()
        with pytest.raises(RuntimeError):
            f.glyphs = []

    def test_truetypetables_readonly(self):
        f = Font()
        with pytest.raises(RuntimeError):
            f.truetypetables = []

    def test_write_empty_from_scratch(self):
        f = Font()
        vfb_path = Path(__file__).parent.parent / "data" / "empty.scratch.vfb"
        f.Save(str(vfb_path))

    # def test_SaveAFM(self):
    #     base_path = Path(__file__).parent.parent / "data" / "mini.vfb"
    #     f = Font(str(base_path))
    #     f.SaveAFM(str(base_path.with_suffix(".gen.afm")))
    #     with open(base_path.with_suffix(".gen.afm")) as afm:
    #         actual = afm.read()
    #     with open(base_path.with_suffix(".afm")) as afm:
    #         expected = afm.read()
    #     assert actual == expected

    # def test_SaveAFM_expanded(self):
    #     base_path = Path(__file__).parent.parent / "data" / "mini.vfb"
    #     f = Font(str(base_path))
    #     assert f.classes == ["_LAT_a_LEFT: a' c", "_LAT_c_RIGHT: c' a", "_LAT_b: b'"]
    #     kerning = f.fake_get_afm_kerning(expand_kerning=True)
    #     assert kerning == [
    #         ("a", "period", -100),
    #         ("c", "period", -100),  # expanded pair
    #         ("period", "a", -90),
    #         ("period", "c", -120),
    #         ("period", "period", 10),
    #         ("space", "period", -80),
    #     ]
    #     f.fake_save_afm_expanded(str(base_path.with_suffix(".expanded.gen.afm")))
    #     with open(base_path.with_suffix(".expanded.gen.afm")) as afm:
    #         actual = afm.read()
    #     with open(base_path.with_suffix(".expanded.afm")) as afm:
    #         expected = afm.read()
    #     assert actual == expected

    def test_classes(self):
        f = Font()
        g = Glyph()
        g.name = "adieresis"
        f.glyphs.append(g)

        # Glyph in font with index 0
        i = f.FindGlyph("adieresis")
        assert i == 0

        # Glyph not in font
        i = f.FindGlyph("a")
        assert i == -1

    def test_classes_deserialize(self):
        base_path = Path(__file__).parent.parent / "data" / "classes_duplicate.vfb"
        f = Font(str(base_path))
        assert f.classes == [
            "_a: a'",
            "_a: a'",
            ".mtrx3: a'",
            ".mtrx4:",
            ".mtrx5:",
            "class6:",
            "_kern7:",
            ".mtrx8:",
        ]
        assert f._classes._kerning_flags == {"_a": (1024, 0), "_kern7": (2048, 0)}
        assert f._classes._metrics_flags == {
            ".mtrx3": (
                0,
                1025,
                0,
            ),
            ".mtrx4": (
                0,
                5121,
                0,
            ),
            ".mtrx5": (
                0,
                6145,
                0,
            ),
            ".mtrx8": (
                0,
                3073,
                0,
            ),
        }
        # First class is kerning left
        assert f.GetClassLeft(0) == 1
        assert f.GetClassRight(0) == 0
        assert f.GetClassMetricsFlags(0) == (0, 0, 0)
        # Duplicate class has no flags
        assert f.GetClassLeft(1) == 0
        assert f.GetClassRight(1) == 0
        assert f.GetClassMetricsFlags(0) == (0, 0, 0)
        # Class 2 is metrics left
        assert f.GetClassLeft(2) == 0
        assert f.GetClassRight(2) == 0
        assert f.GetClassMetricsFlags(2) == (1, 0, 0)
        # Class 3 is metrics left and width
        assert f.GetClassLeft(3) == 0
        assert f.GetClassRight(3) == 0
        assert f.GetClassMetricsFlags(3) == (1, 0, 1)
        # Class 4 is metrics right and width
        assert f.GetClassLeft(4) == 0
        assert f.GetClassRight(4) == 0
        assert f.GetClassMetricsFlags(4) == (0, 1, 1)
        # Class 5 is OpenType
        assert f.GetClassLeft(5) == 0
        assert f.GetClassRight(5) == 0
        assert f.GetClassMetricsFlags(5) == (0, 0, 0)
        # Class 6 is kerning right
        assert f.GetClassLeft(6) == 0
        assert f.GetClassRight(6) == 1
        assert f.GetClassMetricsFlags(6) == (0, 0, 0)
        # Class 7 is metrics left and right
        assert f.GetClassLeft(7) == 0
        assert f.GetClassRight(7) == 0
        assert f.GetClassMetricsFlags(7) == (1, 1, 0)
        # Class 8 is out of bounds
        assert f.GetClassLeft(8) is None
        assert f.GetClassRight(8) is None
        assert f.GetClassMetricsFlags(8) is None

    def test_class_flags_persist(self):
        # Class flags should persist in the font when the class list is replaced
        f = Font()
        f.classes = ["caps: O", ".mtrx1: O", "_kern3: O'"]
        f.SetClassFlags(2, 1, 0)  # 3rd class is left
        assert (f.GetClassLeft(0), f.GetClassRight(0)) == (0, 0)
        assert (f.GetClassLeft(1), f.GetClassRight(1)) == (0, 0)
        assert (f.GetClassLeft(2), f.GetClassRight(2)) == (1, 0)
        assert (f.GetClassLeft(3), f.GetClassRight(3)) == (None, None)

        f.classes = ["caps: O", ".mtrx1: O", "_kern3: O'", "_A: A' Aacute"]
        # 3rd class should still have the left flag
        assert (f.GetClassLeft(2), f.GetClassRight(2)) == (1, 0)
        assert (f.GetClassLeft(3), f.GetClassRight(3)) == (0, 0)
        assert (f.GetClassLeft(4), f.GetClassRight(4)) == (None, None)

        f.classes = ["caps: O", ".mtrx1: O", "_kern3: O'"]
        # 3rd class should still have the left flag
        assert (f.GetClassLeft(2), f.GetClassRight(2)) == (1, 0)
        assert (f.GetClassLeft(3), f.GetClassRight(3)) == (None, None)
