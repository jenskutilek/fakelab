from .Font import Font
from .FontLab import FakeLab
from .Glyph import Glyph
from .Node import Node
from .Point import Point
from .Rect import Rect
from .TTH import TTH
from .TTHCommand import TTHCommand
from .TTInfo import TTInfo


__all__ = [
    "Anchor",
    "AuditRecord",
    "Canvas",
    "Component",
    "Dialog",
    "Encoding",
    "EncodingRecord",
    "Feature",
    "Font",
    "FakeLab",
    "Glyph",
    "Guide",
    "Hint",
    "Image",
    "KerningPair",
    "Link",
    "Matrix",
    "NameRecord",
    "Node",
    "Options",
    "Point",
    "Rect",
    "Replace",
    "TrueTypeTable",
    "TTH",
    "TTHCommand",
    "TTHPoint",
    "TTInfo",
    "TTPoint",
    "TTStem",
]


# Classes below are only placeholders that do nothing.
# If you need any of them in your testing code, move them to a separate file
# and implement them as far as you need.


class Anchor(object):
    pass


class AuditRecord(object):
    pass


class Canvas(object):
    pass


class Component(object):
    pass


class Dialog(object):
    pass


class Encoding(object):
    pass


class EncodingRecord(object):
    pass


class Feature(object):
    pass


class Guide(object):
    pass


class Hint(object):
    pass


class Image(object):
    pass


class KerningPair(object):
    pass


class Link(object):
    pass


class Matrix(object):
    pass


class NameRecord(object):
    pass


class Options(object):
    pass


class Replace(object):
    pass


class TrueTypeTable(object):
    pass


class TTHPoint(object):
    pass


class TTPoint(object):
    pass


class TTStem(object):
    pass
