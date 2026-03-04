__doc__ = """
Constants for font formats
"""

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


# Node type
nLINE = 1
nMOVE = 17
nCURVE = 35
nOFF = 65

# Alignment
nSHARP = 0
nSMOOTH = 4096  # tangent
nCLOSEPATH = 8192  # ? Undocumented: Closepath follows after node
nFIXED = 12288  # curve to curve smooth

vfb2json_node_types = {"line": 1, "move": 17, "curve": 35, "qcurve": 65}
json2vfb_node_types = {nLINE: "line", nMOVE: "move", nCURVE: "curve", nOFF: "qcurve"}

vfb2json_node_conns = {0: nSHARP, 1: nSMOOTH, 2: nCLOSEPATH, 3: nFIXED}
json2vfb_node_conns = {nSHARP: 0, nSMOOTH: 1, nCLOSEPATH: 2, nFIXED: 3}
