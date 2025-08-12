from __future__ import annotations

from collections import UserList
from typing import TYPE_CHECKING

from FL.fake.Base import Copyable
from FL.objects.EncodingRecord import EncodingRecord

if TYPE_CHECKING:
    from FL.objects.Font import Font


class Encoding(UserList[EncodingRecord], Copyable):
    """
    Encoding - class to represent Encoding
    """

    __slots__ = ["_parent", "data"]

    # Constructor

    def __init__(self, encoding_or_none: Encoding | None = None) -> None:
        """
        Encoding()         - generic constructor, creates Encoding
        Encoding(Encoding) - copy constructor

        Args:
            encoding_or_none (Encoding | None, optional): _description_. Defaults to None.
        """
        self._parent: Font | None = None
        self.data: list[EncodingRecord] = []
        if isinstance(encoding_or_none, Encoding):
            self._copy_constructor(encoding_or_none)
        # ??? We can't inspect a just initialized encoding in FL, it just crashes.
        # else:
        #     self._set_default()

    def __repr__(self) -> str:
        if self.parent is None:
            p = "orpahn"  # sic
        else:
            p = f'parent: "{self.parent.font_name or "(null)"}"'
        return f"<Encoding: {p}>"

    # Attributes

    @property
    def parent(self) -> Font | None:
        """
        Encoding's parent object, Font
        """
        return self._parent

    # Operations

    def __delitem__(self, i: int) -> None:
        """
        del Encoding[] - remove an element from the encoding
        """
        del self.data[i]

    def __getitem__(self, i: int) -> EncodingRecord:
        """
        Accesses individial EncodingRecord objects
        """
        return self.data[i]

    def __len__(self) -> int:
        """
        Return the number of EncodingRecords in the Encoding.
        """
        return len(self.data)

    # Methods

    def append(self, encoding_record: EncodingRecord) -> None:
        """
        Append an EncodingRecord to the end of the encoding.

        Args:
            encoding_record (EncodingRecord): _description_
        """
        self.data.append(encoding_record)

    def insert(self, index: int, encoding_record: EncodingRecord) -> None:
        """
        Insert an EncodingRecord at index.

        Args:
            index (int): _description_
            encoding_record (EncodingRecord): _description_
        """
        self.data.insert(index, encoding_record)

    def FillUnencoded(self) -> None:
        raise NotImplementedError

    def FillUnicodes(self) -> None:
        raise NotImplementedError

    def FindName(self, name: str) -> int:
        """
        Find a glyph name in the encoding and return its index or -1.

        Args:
            name (str): The glyph name
        """
        raise NotImplementedError

    def Load(self, filename: str) -> None:
        """
        Opens encoding from .ENC format.

        Args:
            filename (str): _description_
        """
        raise NotImplementedError

    def Save(self, filename: str, EncodingTitle: str, Id: int) -> None:
        """
        Saves encoding in .ENC format.

        Args:
            filename (str): _description_
            EncodingTitle (str): _description_
            Id (int): _description_
        """
        raise NotImplementedError

    # Internal

    def load_font_default(self) -> None:
        # How is the unicode derived? It is not stored in Encoding in the VFB.
        for name, uni in (
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
        ):
            rec = EncodingRecord()
            rec.name = name
            rec.unicode = uni
            self.append(rec)
