from __future__ import annotations

from FL.objects.Component import Component
from FL.objects.Font import Font
from FL.objects.FontLab import FakeLab
from FL.objects.Glyph import Glyph
from FL.objects.Hint import Hint
from FL.objects.KerningPair import KerningPair
from FL.objects.Link import Link
from FL.objects.Matrix import Matrix
from FL.objects.Node import Node
from FL.objects.Options import Options
from FL.objects.Point import Point
from FL.objects.Rect import Rect
from FL.objects.TTH import TTH
from FL.objects.TTHCommand import TTHCommand
from FL.objects.TTHPoint import TTHPoint
from FL.objects.TTInfo import TTInfo
from FL.objects.TTPoint import TTPoint


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


class Image(object):
    pass


class NameRecord(object):
    pass


class Replace(object):
    pass


class TrueTypeTable(object):
    pass


class TTStem(object):
    pass
