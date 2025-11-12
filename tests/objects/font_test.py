import unittest
from pathlib import Path

import pytest

from FL import Feature, Font, Glyph, fl


class FontTests(unittest.TestCase):
    def test_instantiation(self) -> None:
        f = Font()
        assert isinstance(f, Font)

    def test_instantiation_path(self) -> None:
        vfb_path = Path(__file__).parent.parent.parent / "tests" / "data" / "empty.vfb"

        f = Font(str(vfb_path))
        assert len(fl) == 0
        fl.Add(f)
        assert len(fl) == 1
        assert f.file_name == str(vfb_path)

    def test_add_glyph(self) -> None:
        f = Font()
        assert len(f) == 0
        f.glyphs.append(Glyph())
        assert len(f) == 1

    def test_find_glyph(self) -> None:
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

    def test_features_readonly(self) -> None:
        f = Font()
        with pytest.raises(RuntimeError):
            f.features = []

    def test_features_iadd_freeze(self) -> None:
        f = Font()
        with pytest.raises(ReferenceError):
            f.features += Feature()

    def test_features_setitem(self) -> None:
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

    def test_features_setslice(self) -> None:
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

    def test_features_append(self) -> None:
        f = Font()
        fea = Feature()
        f.features.append(fea)
        assert len(f.features) == 1
        assert fea.parent == f

    def test_fontnames_readonly(self) -> None:
        f = Font()
        with pytest.raises(RuntimeError):
            f.fontnames = []

    def test_glyphs_readonly(self) -> None:
        f = Font()
        with pytest.raises(RuntimeError):
            f.glyphs = []

    def test_truetypetables_readonly(self) -> None:
        f = Font()
        with pytest.raises(RuntimeError):
            f.truetypetables = []

    def test_write_empty_from_scratch(self) -> None:
        f = Font()
        vfb_path = Path(__file__).parent.parent / "data" / "empty.scratch.vfb"
        f.Save(str(vfb_path))

    def test_SaveAFM(self) -> None:
        base_path = Path(__file__).parent.parent / "data" / "mini.vfb"
        f = Font(str(base_path))
        f.SaveAFM(str(base_path.with_suffix(".gen.afm")))
        with open(base_path.with_suffix(".gen.afm")) as afm:
            actual = afm.read()
        with open(base_path.with_suffix(".afm")) as afm:
            expected = afm.read()
        assert actual == expected

    def test_SaveAFM_expanded(self) -> None:
        base_path = Path(__file__).parent.parent / "data" / "mini.vfb"
        f = Font(str(base_path))
        assert f.classes == ["_LAT_a_LEFT: a' c", "_LAT_c_RIGHT: c' a", "_LAT_b: b'"]
        kerning = f.fake_get_afm_kerning(expand_kerning=True)
        assert kerning == [
            ("a", "period", -100),
            ("c", "period", -100),  # expanded pair
            ("period", "a", -90),
            ("period", "c", -120),
            ("period", "period", 10),
            ("space", "period", -80),
        ]
        f.fake_save_afm_expanded(str(base_path.with_suffix(".expanded.gen.afm")))
        with open(base_path.with_suffix(".expanded.gen.afm")) as afm:
            actual = afm.read()
        with open(base_path.with_suffix(".expanded.afm")) as afm:
            expected = afm.read()
        assert actual == expected

    def test_bounding_box(self) -> None:
        base_path = Path(__file__).parent.parent / "data" / "mini.vfb"
        f = Font(str(base_path))
        bbox = f.fake_bounding_rect()
        assert (bbox.ll.x, bbox.ll.y, bbox.ur.x, bbox.ur.y) == (66, -66, 531, 646)

    def test_classes(self) -> None:
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

    def test_classes_deserialize(self) -> None:
        base_path = Path(__file__).parent.parent / "data" / "classes_duplicate.vfb"
        f = Font(str(base_path))
        assert f.classes == [
            "_a: a'",
            "_a: a'",
            ".mtrx3: a'",
            ".mtrx4: ",
            ".mtrx5: ",
            "class6: ",
            "_kern7: ",
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

    def test_class_flags_persist(self) -> None:
        # Class flags should persist in the font when the class list is replaced
        f = Font()
        f.classes = ["caps: O", ".mtrx1: O", "_kern3: O'"]
        f.SetClassFlags(2, 1, 0)  # 3rd class is left
        assert (f.GetClassLeft(0), f.GetClassRight(0)) == (0, 0)
        assert (f.GetClassLeft(1), f.GetClassRight(1)) == (0, 0)
        assert (f.GetClassLeft(2), f.GetClassRight(2)) == (1, 0)
        assert (f.GetClassLeft(3), f.GetClassRight(3)) == (None, None)

        f.classes = ["caps: O", "_kern3: O'", ".mtrx1: O", "_A: A' Aacute"]
        # Class "_kern3" should still have the left flag, but it is #1 now
        assert (f.GetClassLeft(1), f.GetClassRight(1)) == (1, 0)
        assert (f.GetClassLeft(3), f.GetClassRight(3)) == (0, 0)
        assert (f.GetClassLeft(4), f.GetClassRight(4)) == (None, None)

        f.classes = ["caps: O", ".mtrx1: O", "_kern3: O'"]
        # 3rd class should still have the left flag
        assert (f.GetClassLeft(2), f.GetClassRight(2)) == (1, 0)
        assert (f.GetClassLeft(3), f.GetClassRight(3)) == (None, None)

    def test_encoding_deserialize(self) -> None:
        base_path = Path(__file__).parent.parent / "data" / "mini.vfb"
        f = Font(str(base_path))
        encoding = [e.name for e in f.encoding]
        assert encoding == [
            "_0000",
            "_0001",
            "_0002",
            "_0003",
            "_0004",
            "breve",
            "dotaccent",
            "_0007",
            "ring",
            "_0009",
            "hungarumlaut",
            "ogonek",
            "caron",
            "dotlessi",
            "_0014",
            "_0015",
            "_0016",
            "_0017",
            "_0018",
            "_0019",
            "_0020",
            "_0021",
            "_0022",
            "_0023",
            "_0024",
            "fraction",
            "fi",
            "fl",
            "Lslash",
            "lslash",
            "Zcaron",
            "zcaron",
            "space",
            "exclam",
            "quotedbl",
            "numbersign",
            "dollar",
            "percent",
            "ampersand",
            "quotesingle",
            "parenleft",
            "parenright",
            "asterisk",
            "plus",
            "comma",
            "hyphen",
            "period",
            "slash",
            "zero",
            "one",
            "two",
            "three",
            "four",
            "five",
            "six",
            "seven",
            "eight",
            "nine",
            "colon",
            "semicolon",
            "less",
            "equal",
            "greater",
            "question",
            "at",
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",
            "bracketleft",
            "backslash",
            "bracketright",
            "asciicircum",
            "underscore",
            "grave",
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            "h",
            "i",
            "j",
            "k",
            "l",
            "m",
            "n",
            "o",
            "p",
            "q",
            "r",
            "s",
            "t",
            "u",
            "v",
            "w",
            "x",
            "y",
            "z",
            "braceleft",
            "bar",
            "braceright",
            "asciitilde",
            "_0127",
            "Euro",
            "_0129",
            "quotesinglbase",
            "florin",
            "quotedblbase",
            "ellipsis",
            "dagger",
            "daggerdbl",
            "circumflex",
            "perthousand",
            "Scaron",
            "guilsinglleft",
            "OE",
            "_0141",
            "_0142",
            "_0143",
            "_0144",
            "quoteleft",
            "quoteright",
            "quotedblleft",
            "quotedblright",
            "bullet",
            "endash",
            "emdash",
            "tilde",
            "trademark",
            "scaron",
            "guilsinglright",
            "oe",
            "_0157",
            "_0158",
            "Ydieresis",
            "uni00A0",
            "exclamdown",
            "cent",
            "sterling",
            "currency",
            "yen",
            "brokenbar",
            "section",
            "dieresis",
            "copyright",
            "ordfeminine",
            "guillemotleft",
            "logicalnot",
            "minus",
            "registered",
            "macron",
            "degree",
            "plusminus",
            "twosuperior",
            "threesuperior",
            "acute",
            "mu",
            "paragraph",
            "periodcentered",
            "cedilla",
            "onesuperior",
            "ordmasculine",
            "guillemotright",
            "onequarter",
            "onehalf",
            "threequarters",
            "questiondown",
            "Agrave",
            "Aacute",
            "Acircumflex",
            "Atilde",
            "Adieresis",
            "Aring",
            "AE",
            "Ccedilla",
            "Egrave",
            "Eacute",
            "Ecircumflex",
            "Edieresis",
            "Igrave",
            "Iacute",
            "Icircumflex",
            "Idieresis",
            "Eth",
            "Ntilde",
            "Ograve",
            "Oacute",
            "Ocircumflex",
            "Otilde",
            "Odieresis",
            "multiply",
            "Oslash",
            "Ugrave",
            "Uacute",
            "Ucircumflex",
            "Udieresis",
            "Yacute",
            "Thorn",
            "germandbls",
            "agrave",
            "aacute",
            "acircumflex",
            "atilde",
            "adieresis",
            "aring",
            "ae",
            "ccedilla",
            "egrave",
            "eacute",
            "ecircumflex",
            "edieresis",
            "igrave",
            "iacute",
            "icircumflex",
            "idieresis",
            "eth",
            "ntilde",
            "ograve",
            "oacute",
            "ocircumflex",
            "otilde",
            "odieresis",
            "divide",
            "oslash",
            "ugrave",
            "uacute",
            "ucircumflex",
            "udieresis",
            "yacute",
            "thorn",
            "ydieresis",
        ]

    def test_blue_values_initialization(self) -> None:
        f = Font()
        assert f.blue_values_num == 0
        assert f.blue_values == [[]] * 16

    def test_set_blue_values_for_master(self) -> None:
        f = Font()
        # Modify the length of the list
        f.blue_values_num = 3
        assert f.blue_values == [[0, 0, 0]] * 16
        # Has no effect because it operates on a copy of the original list
        f.blue_values[0] = [1, 2, 3]
        assert f.blue_values == [[0, 0, 0]] * 16
        # Setting a value directly works
        f.blue_values[0][0] = -1
        assert f.blue_values[0] == [-1, 0, 0]

    def test_set_blue_values_internal(self) -> None:
        f = Font()
        # Default master (0)
        f.fake_set_master_blue_values([-10, 1])
        # Some other master (2)
        f.fake_set_master_blue_values([-15, 3], 2)
        assert f.blue_values == [
            [-10, 1],
            [0, 0],
            [-15, 3],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
        ]

    def test_axis_append_define(self) -> None:
        f = Font()
        f.DefineAxis("Optik", "OpticalSize", "Op")
        f.axis.append(("Fettegrad", "Wt", "Weight"))
        assert f.axis == [("Optik", "Op", "OpticalSize")]

    def test_build_axis_map_1(self) -> None:
        f = Font()
        f._axis = [("Weight", "Wt", "Weight")]
        f._axis_count = 1
        result = f.fake_master_map()
        assert result == [(0,), (1,)]

    def test_build_axis_map_2(self) -> None:
        f = Font()
        f._axis = [("Weight", "Wt", "Weight"), ("Width", "Wd", "Width")]
        f._axis_count = 2
        result = f.fake_master_map()
        assert result == [(0, 0), (1, 0), (0, 1), (1, 1)]

    def test_build_axis_map_3(self) -> None:
        f = Font()
        f._axis = [
            ("Weight", "Wt", "Weight"),
            ("Width", "Wd", "Width"),
            ("Optical Size", "Op", "Optical Size"),
        ]
        f._axis_count = 3
        result = f.fake_master_map()
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
        f._axis_count = 4
        result = f.fake_master_map()
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
