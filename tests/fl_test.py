from __future__ import annotations

import unittest
from pathlib import Path

from vfbLib.json import save_vfb_json

from FL import FakeLab, Font, fl
from FL.constants import ftFONTLAB, ftOPENTYPE, ftTRUETYPE

# fl is pre-instantiated, take care not to modify the global state


def get_vfb_path(filename: str) -> Path:
    return Path(__file__).parent / "data" / filename


def save_vfb_json_file(filename: str) -> None:
    vfb_path = get_vfb_path(filename)
    save_vfb_json(vfb_path)


class FLTests(unittest.TestCase):
    def test_instantiation(self) -> None:
        assert isinstance(fl, FakeLab)

    def test_no_font(self) -> None:
        fk = FakeLab()
        assert fk.font is None

    def test_no_font_no_glyph(self) -> None:
        fk = FakeLab()
        assert fk.glyph is None

    def test_font_no_glyph(self) -> None:
        fk = FakeLab()
        fk.Add(Font())
        assert isinstance(fk.font, Font)
        assert fk.glyph is None

    def test_load_empty(self) -> None:
        fk = FakeLab()
        fk.Open(str(get_vfb_path("empty.vfb")))
        assert isinstance(fk.font, Font)
        assert fk.ifont == 0
        enc = [(e.name, e.unicode) for e in fk.font.encoding]
        assert enc == [
            ("_0000", -1),
            ("_0001", -1),
            ("_0002", -1),
            ("_0003", -1),
            ("_0004", -1),
            ("breve", 728),
            ("dotaccent", 729),
            ("_0007", -1),
            ("ring", 730),
            ("_0009", -1),
            ("hungarumlaut", 733),
            ("ogonek", 731),
            ("caron", 711),
            ("dotlessi", 305),
            ("_0014", -1),
            ("_0015", -1),
            ("_0016", -1),
            ("_0017", -1),
            ("_0018", -1),
            ("_0019", -1),
            ("_0020", -1),
            ("_0021", -1),
            ("_0022", -1),
            ("_0023", -1),
            ("_0024", -1),
            ("fraction", 8260),
            ("fi", 64257),
            ("fl", 64258),
            ("Lslash", 321),
            ("lslash", 322),
            ("Zcaron", 381),
            ("zcaron", 382),
            ("space", 32),
            ("exclam", 33),
            ("quotedbl", 34),
            ("numbersign", 35),
            ("dollar", 36),
            ("percent", 37),
            ("ampersand", 38),
            ("quotesingle", 39),
            ("parenleft", 40),
            ("parenright", 41),
            ("asterisk", 42),
            ("plus", 43),
            ("comma", 44),
            ("hyphen", 45),
            ("period", 46),
            ("slash", 47),
            ("zero", 48),
            ("one", 49),
            ("two", 50),
            ("three", 51),
            ("four", 52),
            ("five", 53),
            ("six", 54),
            ("seven", 55),
            ("eight", 56),
            ("nine", 57),
            ("colon", 58),
            ("semicolon", 59),
            ("less", 60),
            ("equal", 61),
            ("greater", 62),
            ("question", 63),
            ("at", 64),
            ("A", 65),
            ("B", 66),
            ("C", 67),
            ("D", 68),
            ("E", 69),
            ("F", 70),
            ("G", 71),
            ("H", 72),
            ("I", 73),
            ("J", 74),
            ("K", 75),
            ("L", 76),
            ("M", 77),
            ("N", 78),
            ("O", 79),
            ("P", 80),
            ("Q", 81),
            ("R", 82),
            ("S", 83),
            ("T", 84),
            ("U", 85),
            ("V", 86),
            ("W", 87),
            ("X", 88),
            ("Y", 89),
            ("Z", 90),
            ("bracketleft", 91),
            ("backslash", 92),
            ("bracketright", 93),
            ("asciicircum", 94),
            ("underscore", 95),
            ("grave", 96),
            ("a", 97),
            ("b", 98),
            ("c", 99),
            ("d", 100),
            ("e", 101),
            ("f", 102),
            ("g", 103),
            ("h", 104),
            ("i", 105),
            ("j", 106),
            ("k", 107),
            ("l", 108),
            ("m", 109),
            ("n", 110),
            ("o", 111),
            ("p", 112),
            ("q", 113),
            ("r", 114),
            ("s", 115),
            ("t", 116),
            ("u", 117),
            ("v", 118),
            ("w", 119),
            ("x", 120),
            ("y", 121),
            ("z", 122),
            ("braceleft", 123),
            ("bar", 124),
            ("braceright", 125),
            ("asciitilde", 126),
            ("_0127", -1),
            ("Euro", 8364),
            ("_0129", -1),
            ("quotesinglbase", 8218),
            ("florin", 402),
            ("quotedblbase", 8222),
            ("ellipsis", 8230),
            ("dagger", 8224),
            ("daggerdbl", 8225),
            ("circumflex", 710),
            ("perthousand", 8240),
            ("Scaron", 352),
            ("guilsinglleft", 8249),
            ("OE", 338),
            ("_0141", -1),
            ("_0142", -1),
            ("_0143", -1),
            ("_0144", -1),
            ("quoteleft", 8216),
            ("quoteright", 8217),
            ("quotedblleft", 8220),
            ("quotedblright", 8221),
            ("bullet", 8226),
            ("endash", 8211),
            ("emdash", 8212),
            ("tilde", 732),
            ("trademark", 8482),
            ("scaron", 353),
            ("guilsinglright", 8250),
            ("oe", 339),
            ("_0157", -1),
            ("_0158", -1),
            ("Ydieresis", 376),
            ("uni00A0", 160),
            ("exclamdown", 161),
            ("cent", 162),
            ("sterling", 163),
            ("currency", 164),
            ("yen", 165),
            ("brokenbar", 166),
            ("section", 167),
            ("dieresis", 168),
            ("copyright", 169),
            ("ordfeminine", 170),
            ("guillemotleft", 171),
            ("logicalnot", 172),
            ("minus", 8722),
            ("registered", 174),
            ("macron", 175),
            ("degree", 176),
            ("plusminus", 177),
            ("twosuperior", 178),
            ("threesuperior", 179),
            ("acute", 180),
            ("mu", 181),
            ("paragraph", 182),
            ("periodcentered", 183),
            ("cedilla", 184),
            ("onesuperior", 185),
            ("ordmasculine", 186),
            ("guillemotright", 187),
            ("onequarter", 188),
            ("onehalf", 189),
            ("threequarters", 190),
            ("questiondown", 191),
            ("Agrave", 192),
            ("Aacute", 193),
            ("Acircumflex", 194),
            ("Atilde", 195),
            ("Adieresis", 196),
            ("Aring", 197),
            ("AE", 198),
            ("Ccedilla", 199),
            ("Egrave", 200),
            ("Eacute", 201),
            ("Ecircumflex", 202),
            ("Edieresis", 203),
            ("Igrave", 204),
            ("Iacute", 205),
            ("Icircumflex", 206),
            ("Idieresis", 207),
            ("Eth", 208),
            ("Ntilde", 209),
            ("Ograve", 210),
            ("Oacute", 211),
            ("Ocircumflex", 212),
            ("Otilde", 213),
            ("Odieresis", 214),
            ("multiply", 215),
            ("Oslash", 216),
            ("Ugrave", 217),
            ("Uacute", 218),
            ("Ucircumflex", 219),
            ("Udieresis", 220),
            ("Yacute", 221),
            ("Thorn", 222),
            ("germandbls", 223),
            ("agrave", 224),
            ("aacute", 225),
            ("acircumflex", 226),
            ("atilde", 227),
            ("adieresis", 228),
            ("aring", 229),
            ("ae", 230),
            ("ccedilla", 231),
            ("egrave", 232),
            ("eacute", 233),
            ("ecircumflex", 234),
            ("edieresis", 235),
            ("igrave", 236),
            ("iacute", 237),
            ("icircumflex", 238),
            ("idieresis", 239),
            ("eth", 240),
            ("ntilde", 241),
            ("ograve", 242),
            ("oacute", 243),
            ("ocircumflex", 244),
            ("otilde", 245),
            ("odieresis", 246),
            ("divide", 247),
            ("oslash", 248),
            ("ugrave", 249),
            ("uacute", 250),
            ("ucircumflex", 251),
            ("udieresis", 252),
            ("yacute", 253),
            ("thorn", 254),
            ("ydieresis", 255),
        ]

    def test_generate_otf(self) -> None:
        fk = FakeLab()
        fk.Open(str(get_vfb_path("mini.vfb")))
        fk.GenerateFont(0, ftOPENTYPE, str(get_vfb_path("mini.gen.otf")))

    def test_generate_ttf(self) -> None:
        fk = FakeLab()
        fk.Open(str(get_vfb_path("mini.vfb")))
        fk.GenerateFont(0, ftTRUETYPE, str(get_vfb_path("mini.gen.ttf")))

    def test_generate_vfb(self) -> None:
        fk = FakeLab()
        fk.Open(str(get_vfb_path("mini.vfb")))
        fk.GenerateFont(ftFONTLAB, str(get_vfb_path("mini.gen.vfb")))
        save_vfb_json_file("mini.gen.vfb")
