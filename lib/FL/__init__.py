from __future__ import annotations

from FL.FLdict import *
from FL.MenuCommands import *
from FL.objects import *

"""
FakeLab. A FontLab Studio 5 replacement for testing Python code.

Everything is only implemented so far as to make FontLab objects importable
outside of FontLab Studio 5, and run tests.
"""

# fl is pre-instantiated
fl = FakeLab()  # noqa: F405


# Font formats

# FontLab VFB font
ftFONTLAB = 0

# PC Type 1 font (binary/PFB)
ftTYPE1 = 1

# PC MultipleMaster font (PFB)
ftTYPE1_MM = 20

# PC Type 1 font (ASCII/PFA)
ftTYPE1ASCII = 2

# PC MultipleMaster font (ASCII/PFA)
ftTYPE1ASCII_MM = 21

# PC TrueType/TT OpenType font (TTF)
ftTRUETYPE = 3

# PS OpenType (CFF-based) font (OTF)
ftOPENTYPE = 6

# Mac Type 1 font (generates suitcase and LWFN file, optionally AFM)
ftMACTYPE1 = 23

# Mac TrueType font (generates suitcase)
ftMACTRUETYPE = 30

# Mac TrueType font (generates suitcase with resources in data fork)
ftMACTRUETYPE_DFONT = 31
