import pytest
import unittest

from FL import fl, Feature, Font, Glyph
from pathlib import Path


class FontTests(unittest.TestCase):
    def test_instantiation(self):
        f = Font()
        assert isinstance(f, Font)

    def test_instantiation_path(self):
        vfb_path = Path(__file__).parent.parent.parent / "tests" / "data" / "empty.vfb"

        f = Font(vfb_path)
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
        f.features[0:2] = [Feature("cccc"), Feature("dddd")]
        assert f.features[0].parent == f
        assert f.features[0].tag == "cccc"
        assert f.features[1].parent == f
        assert f.features[1].tag == "dddd"

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
