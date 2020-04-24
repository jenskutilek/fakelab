"""
FakeLab. A FontLab Studio 5 replacement for testing Python code.

Everything is only implemented so far as to make FontLab objects importable
outside of FontLab Studio 5, and run tests.
"""
from .FLdict import *
from .MenuCommands import *
from .objects import *


# fl is pre-instantiated
fl = FakeLab()


# Font formats

ftFONTLAB = 0             # FontLab VFB font
ftTYPE1 = 1               # PC Type 1 font (binary/PFB)
ftTYPE1_MM = 20           # PC MultipleMaster font (PFB)
ftTYPE1ASCII = 2          # PC Type 1 font (ASCII/PFA)
ftTYPE1ASCII_MM = 21      # PC MultipleMaster font (ASCII/PFA)
ftTRUETYPE = 3            # PC TrueType/TT OpenType font (TTF)
ftOPENTYPE = 6            # PS OpenType (CFF-based) font (OTF)
ftMACTYPE1 = 23           # Mac Type 1 font (generates suitcase and LWFN file, optionally AFM)
ftMACTRUETYPE = 30        # Mac TrueType font (generates suitcase)
ftMACTRUETYPE_DFONT = 31  # Mac TrueType font (generates suitcase with resources in data fork)
