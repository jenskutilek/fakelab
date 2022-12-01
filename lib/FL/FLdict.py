from __future__ import annotations


# FLdict
from .objects.Node import nMOVE, nLINE, nCURVE, nOFF, nSHARP, nSMOOTH, nFIXED

## Canvas

### Brush-Style
cBRUSH_NULL = 1
cBRUSH_SOLID = 0

### Draw-Style
cDS_BLACK = 1
cDS_NOTOR = 2
cDS_NOTCOPY = 4
cDS_NOT = 6
cDS_XOR = 7
cDS_NOTAND = 8
cDS_AND = 9
cDS_NOTXOR = 10
cDS_COPY = 13
cDS_OR = 15
cDS_WHITE = 16

### Pen-Style
cPEN_DASH = 3
cPEN_DOT = 2
cPEN_NULL = 1
cPEN_SOLID = 0

## Colors
cRGB_BLACK = 0
cRGB_BLUE = 16711680
cRGB_GRAY = 8421504
cRGB_GREEN = 65280
cRGB_LTGRAY = 12632256
cRGB_RED = 255
cRGB_WHITE = 16777215
cRGB_YELLOW = 8454143

## Dialog

# -> see Dialog class

### ControlTypes
EDITCONTROL = 0
STATICCONTROL = 1
CHECKBOXCONTROL = 2
BUTTONCONTROL = 3
LISTCONTROL = 4
CHOICECONTROL = 5
PREVIEWCONTROL = 6

### ControlStyles
STYLE_BUTTON = 268435456
STYLE_CHECKBOX = 268435459
STYLE_CHOICE = 278921219
STYLE_CUSTOM = 276824064
STYLE_EDIT = 276824064
STYLE_FRAME = 268435474
STYLE_LABEL = 268435456
STYLE_LIST = 278921216

### ControlStyleModifier
cTO_BOTTOM = 8
cTO_CENTER = 1
cTO_LEFT = 0
cTO_RIGHT = 2
cTO_TOP = 0
cTO_VCENTER = 4

### ControlAlignment
aALIGN = -100
aAUTO = -105
aIDENT = -102
aIDENT2 = -103
aIDENT3 = -104
aNEXT = -101
aSAME = -106


## Message

OK = 1
Cancel = 2


## Node
# -> see Node class

# ### Type
# nLINE = 1
# nMOVE = 17
# nCURVE = 35
# nOFF = 65

# ### Alignment
# nSHARP = 0
# nSMOOTH = 4096
# nFIXED = 12288


## Transformation

TR_CODE_SHIFT = 0
TR_CODE_MIRROR = 1
TR_CODE_SCALE = 2
TR_CODE_ROTATE = 3
TR_CODE_SLANT = 4
TR_CODE_REMOVE = 5
TR_CODE_AUTOHINT = 6
TR_CODE_TT_AUTOHINT = 7
TR_CODE_AUTOREPLACE = 8
TR_CODE_TOLINKS = 9
TR_CODE_TOHINTS = 10
TR_CODE_DECOMPOSE = 11
TR_CODE_CONVERT3 = 12
TR_CODE_CONVERT2 = 13
TR_CODE_REVERSE_ALL = 14
TR_CODE_ALIGNMENT = 15
TR_CODE_EXTREMES = 16
TR_CODE_OVERLAP = 17
TR_CODE_WIDTH = 18
TR_CODE_BEARING = 19
TR_CODE_ALIGNWIDTH = 20
TR_CODE_AUTOSPACING = 21
TR_CODE_BOLD = 22
TR_CODE_COLLEGE = 23
TR_CODE_SHADOW = 24
TR_CODE_3D = 25
TR_CODE_3DROTATE = 26
TR_CODE_GRADIENT = 27
TR_CODE_RANDOM = 28
TR_CODE_ENVELOPE = 29
TR_CODE_MAKELAYER = 30
TR_CODE_OPTIMIZE = 31
TR_CODE_DROP_TTH = 32
TR_CODE_ADJUST = 33


SS_BITMAP = 14
SS_BLACKFRAME = 7
SS_BLACKRECT = 4
SS_CENTER = 1
SS_CENTERIMAGE = 512
SS_ELLIPSISMASK = 49152
SS_ENDELLIPSIS = 16384
SS_ENHMETAFILE = 15
SS_ETCHEDFRAME = 18
SS_ETCHEDHORZ = 16
SS_ETCHEDVERT = 17
SS_GRAYFRAME = 8
SS_GRAYRECT = 5
SS_ICON = 3
SS_LEFT = 0
SS_LEFTNOWORDWRAP = 12
SS_NOPREFIX = 128
SS_NOTIFY = 256
SS_OWNERDRAW = 13
SS_PATHELLIPSIS = 32768
SS_REALSIZEIMAGE = 2048
SS_RIGHT = 2
SS_RIGHTJUST = 1024
SS_SIMPLE = 11
SS_SUNKEN = 4096
SS_TYPEMASK = 31
SS_USERITEM = 10
SS_WHITEFRAME = 9
SS_WHITERECT = 6
SS_WORDELLIPSIS = 49152

WS_BORDER = 8388608
WS_CAPTION = 12582912
WS_CHILD = 1073741824
WS_CLIPCHILDREN = 33554432
WS_CLIPSIBLINGS = 67108864
WS_DISABLED = 134217728
WS_DLGFRAME = 4194304
WS_GROUP = 131072
WS_HSCROLL = 1048576
WS_MAXIMIZE = 16777216
WS_MAXIMIZEBOX = 65536
WS_MINIMIZE = 536870912
WS_MINIMIZEBOX = 131072
WS_OVERLAPPED = 0
WS_OVERLAPPEDWINDOW = 13565952
WS_POPUP = -2147483648
WS_POPUPWINDOW = -2138570752
WS_SYSMENU = 524288
WS_TABSTOP = 65536
WS_THICKFRAME = 262144
WS_VISIBLE = 268435456
WS_VSCROLL = 2097152

cRECT_3DDOWN = 2
cRECT_3DDOWN_FLAT = 6
cRECT_3DDOWN_SOLID = 3
cRECT_3DUP = 4
cRECT_3DUP_FLAT = 7
cRECT_3DUP_SOLID = 5
cRECT_BLACK_FRAME = 8
cRECT_BLACK_SOLID = 10
cRECT_BLACK_THICK_FRAME = 9
cRECT_ELLIPSE = 1
cRECT_FOCUS = 11
cRECT_GRAY_FRAME = 13
cRECT_GRAY_SOLID = 14
cRECT_INVERT = 19
cRECT_LTGRAY_SOLID = 15
cRECT_RECTANGLE = 0
cRECT_SIZE = 12
cRECT_WHITE_SOLID = 16
cRECT_YELLOW_FRAME = 17
cRECT_YELLOW_SOLID = 18
