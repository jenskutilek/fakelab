from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from FL.helpers.registry import FL_REGISTRY_KEY, option_keys, parse_registry_file

__doc__ = "Class to represent the FontLab options interface"


logger = logging.getLogger(__name__)


class Options:
    __slots__ = [
        "_AutoAlignVector",
        "_AutoMetricsClose",
        "_AutoMetricsLeft",
        "_AutoMetricsRight",
        "_AutoRemoveHints",
        "_AutoSave",
        "_AutoSaveTick",
        "_AutohintingHRatio",
        "_AutohintingMaxHWidth",
        "_AutohintingMaxVWidth",
        "_AutohintingMinHLen",
        "_AutohintingMinHWidth",
        "_AutohintingMinVLen",
        "_AutohintingMinVWidth",
        "_AutohintingRemoveHints",
        "_AutohintingVRatio",
        "_Backup",
        "_BitmapSize",
        "_ChartApplyTemplate",
        "_ChartAutoHide",
        "_ChartAutoUnicode",
        "_ChartCaptionFontCharSet",
        "_ChartCaptionFontName",
        "_ChartCaptionFontSize",
        "_ChartDoubleClick",
        "_ChartDragDrop",
        "_ChartPreviewMarks",
        "_ChartSampleSize",
        "_ChartShowNotes",
        "_ChartSorting",
        "_ChartStyle",
        "_ChartTemplateFontCharSet",
        "_ChartTemplateFontName",
        "_ChartTemplateFontSize",
        "_ChartUseTemplate",
        "_ClosepathArrowLen",
        "_CodepagesCount",
        "_ColorBitmap",
        "_ColorClosepath",
        "_ColorEcho",
        "_ColorHintsPen",
        "_ColorMaskPen",
        "_ColorSeacPen",
        "_ColorTemplate",
        "_ColorVMetrics",
        "_CopyHDMXData",
        "_CreateUnexistingCharacters",
        "_DefaultGlyph",
        "_DuplicateX",
        "_DuplicateY",
        "_EditBCPsFixed",
        "_EditBitmapStyle",
        "_EditChangeCursor",
        "_EditFollowScroll",
        "_EditGridX",
        "_EditGridY",
        "_EditHandleTool",
        "_EditHitDistance",
        "_EditLeaveEcho",
        "_EditNotFillOpen",
        "_EditRulers",
        "_EditScaleEPS",
        "_EditShowCross",
        "_EditShowPosition",
        "_EditSmallNodes",
        "_EditSmoothOutline",
        "_EraseSize",
        "_FitAscender",
        "_FitDescender",
        "_FontAudit",
        "_GlyphsBarOpen",
        "_HideAllLayers",
        "_HideToolbars",
        "_LockStyleEx",
        "_OTAddClasses",
        "_OTWriteGDEF",
        "_OptimizeAlign",
        "_OptimizeReduce",
        "_OverlapMode",
        "_PaintAutoTransform",
        "_PaintAutoView",
        "_PaintBrushBody",
        "_PaintBrushCap",
        "_PaintBrushJoin",
        "_PaintBrushRoundness",
        "_PaintBrushVectorX",
        "_PaintBrushVectorY",
        "_PaintBrushWidth",
        "_PaintColor",
        "_PaintMode",
        "_PaintStyleEx",
        "_PaintTextSize",
        "_PaintTool",
        "_PaintTracePolygon",
        "_PasteX",
        "_PasteY",
        "_PreviewExpanded",
        "_PreviewExpandedHeight",
        "_PreviewPPMs",
        "_PreviewPPMsExpanded",
        "_PreviewPointSize",
        "_PreviewSecondLine",
        "_PreviewSmooth",
        "_PreviewWidth",
        "_SamplePPM1",
        "_SamplePPM2",
        "_SnapStyleEx",
        "_T1AFM",
        "_T1Autohint",
        "_T1Decompose",
        "_T1Encoding",
        "_T1PFM",
        "_T1Terminal",
        "_T1Unicode",
        "_T1UseOS2",
        "_TTEAddCharacters",
        "_TTEApplyBBoxSavings",
        "_TTEAutoWinAscDesc",
        "_TTEAutohint",
        "_TTECmap10",
        "_TTEExportOT",
        "_TTEExportUnicode",
        "_TTEExportVOLT",
        "_TTEFontNames",
        "_TTEHint",
        "_TTEKeep",
        "_TTENoReorder",
        "_TTESubrize",
        "_TTEWriteBitmaps",
        "_TTEWriteKernFeature",
        "_TTEheadBBoxSavings",
        "_TTHHintingOptions",
        "_TTIAutohint",
        "_TTIConvert",
        "_TTIDecompose",
        "_TTIFontNames",
        "_TTIKeepHints",
        "_TTIReadBitmaps",
        "_TTIReadKernFeature",
        "_TTIReadOT",
        "_TTIScale1000",
        "_TTIStoreTables",
        "_TTToolReverseShift",
        "_TracerCurveFit",
        "_TracerCurves",
        "_TracerExtremePoints",
        "_TracerPresetMode",
        "_TracerStraightenAngle",
        "_TracerTolerance",
        "_TrackingDistance",
        "_TrackingMode",
        "_UnicodeRangePercent",
        "_VendorCode",
        # Not implemented in FontLab 4.5.2 Win:
        "_CacheTTPath",
        "_CacheTTUse",
        "_ContourSnapAllPoints",
        "_EditDeleteAlt",
        "_EditDoubleClickBitmap",
        "_EditEditSelection",
        "_EditNoToolbars",
        "_EditShowSelection",
        "_NamesFileName",
        "_OTReadMort",
        "_OTWriteMort",
        "_ShowMeterPanel",
        "_UnicodeStrings",
        # Undocumented
        "ATMPPM",
        "ATMScaler",
        "ATMSmooth",
        "AutohintingEngine",
        "ChartAutoActivateCodepage",
        "ChartCopyKerning",
        "ChartGenerate",
        "ChartGenerateRTL",
        "ColorBackground",
        "ColorBackgroundMask",
        "ColorBackgroundMetrics",
        "ColorForegroundMetrics",
        "ColorGlobalGuide",
        "ColorGrid",
        "ColorGroups",
        "ColorGuide",
        "_ColorMetrics",
        "ColorNeighbors",
        "ColorOutline",
        "ControlSwitch",
        "CustomDict",
        "_CustomMarkColor",
        "DSIG_KeyPath",
        "DSIG_Password",
        "DSIG_SertPath",
        "DSIG_TimeStamp",
        "DSIG_Use",
        "EditAllSmooth",
        "EditAutoSelectLayers",
        "EditBCVOpacity",
        "EditComponentsByOutline",
        "EditConnectMasters",
        "EditDoubleClickMask",
        "_EditInstantRefresh",
        "EditKeyboardEditBCP",
        "EditLayersExpanded",
        "EditPreviewKey",
        "EditShowAnchorNames",
        "EditShowMasterPoints",
        "EditShowMeasurementLine",
        "EditShowNodesSelection",
        "EditSmoothIsSmooth",
        "EditThickOutline",
        "EditUndoSelection",
        "EditZoomMode",
        "EmbeddingType",
        "EnableExtPythonEditor",
        "EnablePython",
        "EnableStickPanels",
        "EnableTooltips",
        "ExpandKernCodepage",
        "ExpandKernCount",
        "ExpandKernFlags",
        "ExtPythonEditor",
        "FileOpenSample",
        "FontAuditLive",
        "FontDialogName",
        "FontDialogSize",
        "FontExpanded",
        "FontFixedName",
        "FontFixedSize",
        "FontLabNodes",
        "FontPanelName",
        "FontPanelSize",
        "FontRulerName",
        "FontRulerSize",
        "FontSmallName",
        "FontSmallSize",
        "FontTableName",
        "FontTableSize",
        "GlyphNameSortMode",
        "GlyphsBarTop",
        "GroupCenter",
        "GroupDoubleClick",
        "GroupFill",
        "GroupKerning",
        "GroupMask",
        "GroupShapeFill",
        "GroupShapeMask",
        "GroupShapeOpacity",
        "GroupShiftX",
        "GroupShiftY",
        "GroupUseMetrics",
        "MacroFontName",
        "MaskMetrics",
        "MetricsBarExpanded0",
        "MetricsBarExpanded1",
        "MetricsBarExpanded2",
        "MetricsBarExpanded3",
        "MetricsBottomBar0",
        "MetricsBottomBar1",
        "MetricsBottomBar2",
        "MetricsBottomBar3",
        "MetricsShowBar0",
        "MetricsShowBar1",
        "MetricsShowBar2",
        "MetricsShowBar3",
        "MetricsShowTable0",
        "MetricsShowTable1",
        "MetricsShowTable2",
        "MetricsShowTable3",
        "MMExtrapolation",
        "OpenOutput",
        "OTAddMetricsClasses",
        "OTCompileFeatures",
        "OTGenerate",
        "OTOldContextRule",
        "OTPreviewSize",
        "OTSampleSize",
        "OutputFontName",
        "PaintJapanese",
        "PaintReverseBrushAutoColor",
        "PaintTextFont",
        "PreviewAlternativeArrows",
        "PreviewApplyTemplate",
        "PreviewAutoScroll",
        "PreviewAutoWrap",
        "PreviewBlueColor",
        "PreviewFilterKerning",
        "PreviewFilterMetrics",
        "PreviewFocusString",
        "PreviewHighlightKeyGlyphs",
        "PreviewKeepExceptions",
        "PreviewKerningIcons",
        "PreviewListWidth",
        "PreviewLockDependences",
        "PreviewLockStyle",
        "PreviewMode",
        "PreviewPaintStyle",
        "PreviewPanelTop",
        "PreviewProcessFeatures",
        "PreviewShowClassMembers",
        "PreviewShowReferences",
        "PreviewSize",
        "PreviewSnapStyle",
        "QuickZoomScale",
        "RemoveZeroKerning",
        "Shift10",
        "StyleInactiveMetrics",
        "StyleMetrics",
        "SyncronizeMasters",
        "T1ExportCompatibleCyrillic",
        "T1ExportEncoding",
        "T1FSType",
        "T1MatchEncoding",
        "_T1Sort",
        "T1UseOTFamilyName",
        "T1UseOTStyleName",
        "T1UseTrademarkName",
        "Template_BDF",
        "Template_Path",
        "Template_Use",
        "TTEDecompose",
        "TTESmartFontName",
        "TTESmartMacNames",
        "TTEStoreTables",
        "TTEVersionOS2",
        "_TTEVisual",
        "TTEWriteKernTable",
        "TTFScaler",
        "TTFSmooth",
        "TTHPPM",
        "TTIGenerateNames",
        "TTIReadBinaryOT",
        "TTIStoreBinaryOT",
        "UnicodeKeyboard",
    ]

    def __init__(self) -> None:
        """
        Generic constructor.
        """
        self.Load()

    def __del__(self) -> None:
        self.fake_save_options()

    def __repr__(self) -> str:
        return "<Options>"

    # Additions for FakeLab

    @property
    def fake_options_path(self) -> Path:
        return Path().home() / ".fakelab"

    def as_dict(self) -> dict[str, str | int]:
        d = {}
        for k in option_keys:
            d[k] = getattr(self, k)
        return d

    def fake_load_regfile(self, file_path: Path) -> None:
        """
        Load options from a registry file
        """
        logger.info(f"Loading options from {file_path.name}...")
        reg = parse_registry_file(file_path)
        for k, v in reg.items():
            if hasattr(self, k):
                setattr(self, k, v)
            else:
                logger.warning(f"Unsupported option while loading registry file: '{k}'")
        logger.info("...done.")

    def fake_save_regfile(self, file_path: Path) -> None:
        """
        Save options to a registry file
        """
        # TODO
        # header = f"Windows Registry Editor Version 5.00\n\n[{FL_REGISTRY_KEY}]\n"
        logger.info(f"Saving options to {file_path}...")
        raise NotImplementedError

    def fake_load_options(self) -> None:
        with open(self.fake_options_path, "rb") as f:
            data = json.load(f)
        for k, v in data.items():
            if hasattr(self, k):
                setattr(self, k, v)
            else:
                print(f"Ignored unknown attribute while loading options: {k}")

    def fake_save_options(self) -> None:
        with open(self.fake_options_path, "w", encoding="utf-8") as f:
            json.dump(self.as_dict(), f, ensure_ascii=False, indent=2)

    # Attributes

    # Grouped as in the Options dialog

    # ---------------
    # General Options
    # ---------------

    # -    Fonts
    # -    Folders and paths
    # -    Open and Save
    # -    EPS and bitmap background
    # -    Multiple Master
    # -    Unicode and OpenType

    # -----------
    # Font window
    # -----------

    # -    Glyph cell
    # -    Templates

    # ------------
    # Glyph window
    # ------------

    # -    Dimensions
    # -    Colors
    # -    Tracking
    # -    Shape groups and neighbors

    # --------------
    # Metrics window
    # --------------

    # -    Metrics window colors

    # ----------
    # Font Audit
    # ----------

    # -    Optimize

    # Opening Type 1

    # ---------------------------
    # Opening OpenType & TrueType
    # ---------------------------

    # -    TrueType/OpenType TT(.ttf)

    # -----------------
    # Generating Type 1
    # -----------------

    # -    Type 1 autohinting

    # ------------------------------
    # Generating OpenType & TrueType
    # ------------------------------

    @property
    def TTENoReorder(self) -> int:
        """
        Automatically reorder glyphs
        """
        return self._TTENoReorder

    @TTENoReorder.setter
    def TTENoReorder(self, value: int) -> None:
        self._TTENoReorder = value

    @property
    def TTEFontNames(self) -> int:
        """
        - 0 = Append OpenType name records to the names exported by default
        - 1 = Do not export OpenType name records
        - 2 = Export only OpenType name records - ignore default names
        """
        return self._TTEFontNames

    @TTEFontNames.setter
    def TTEFontNames(self, value: int) -> None:
        self._TTEFontNames = value

    @property
    def TTEExportUnicode(self) -> int:
        """
        Ignore Unicode indexes in the font

        checked
            Ignore Unicode indexes in the font
        option
            Use following codepage for first 256 glyphs:
            Do not reencode first 256 glyphs
        unchecked
            Export only first 256 glyphs of the selected codepage
        unchecked
            Put MS Char Set value into fsSelection field
        """
        return self._TTEExportUnicode

    @TTEExportUnicode.setter
    def TTEExportUnicode(self, value: int) -> None:
        self._TTEExportUnicode = value

    # TODO: TTESmartMacNames
    # Use the OpenType names as menu names on Macintosh

    # TODO: TTEStoreTables
    # Write stored custom TrueType/OpenType tables

    @property
    def TTEExportOT(self) -> int:
        """
        Export OpenType layout tables
        """
        return self._TTEExportOT

    @TTEExportOT.setter
    def TTEExportOT(self, value: int) -> None:
        self._TTEExportOT = value

    # TODO: OTCompileFeatures
    # Compile feature definitions

    # TODO: OTOldContextRule
    # Contextual substitutions in invalid legacy format
    # Use this option only if you know what you are doing

    @property
    def OTWriteGDEF(self) -> int:
        """
        Generate GDEF table
        """
        return self._OTWriteGDEF

    @OTWriteGDEF.setter
    def OTWriteGDEF(self, value: int) -> None:
        self._OTWriteGDEF = value

    @property
    def TTEExportVOLT(self) -> int:
        """
        Export VOLT data
        """
        return self._TTEExportVOLT

    @TTEExportVOLT.setter
    def TTEExportVOLT(self, value: int) -> None:
        self._TTEExportVOLT = value

    # ----------------------
    # -    Digital signature
    # ----------------------

    # DSIG_Use = 0  # Generate digital signature (DSIG table)
    # DSIG_SertPath = ""  # Path to the certificate file (.spc or .cer)
    # DSIG_KeyPath = ""  # Path to the private key file (.pvk
    # DSIG_Password = ""  # Use the following password every time
    # DSIG_TimeStamp = 0  # Generate the time stamp

    # --------------------------------
    # -    TrueType/OpenType TT (.ttf)
    # --------------------------------

    @property
    def TTEHint(self) -> int:
        """
        Export hinted TrueType fonts?
        """
        return self._TTEHint

    @TTEHint.setter
    def TTEHint(self, value: int) -> None:
        self._TTEHint = value

    @property
    def TTEKeep(self) -> int:
        """
        Write stored TrueType native hinting
        """
        return self._TTEKeep

    @TTEKeep.setter
    def TTEKeep(self, value: int) -> None:
        self._TTEKeep = value

    @property
    def TTEVisual(self) -> int:
        """
        Export visual TrueType hints?
        """
        return self._TTEVisual

    @TTEVisual.setter
    def TTEVisual(self, value: int) -> None:
        self._TTEVisual = value

    @property
    def TTEAutohint(self) -> int:
        """
        Autohint unhinted glyphs
        """
        return self._TTEAutohint

    @TTEAutohint.setter
    def TTEAutohint(self, value: int) -> None:
        self._TTEAutohint = value

    @property
    def TTEWriteBitmaps(self) -> int:
        """
        Export embedded bitmaps
        """
        return self._TTEWriteBitmaps

    @TTEWriteBitmaps.setter
    def TTEWriteBitmaps(self, value: int) -> None:
        self._TTEWriteBitmaps = value

    @property
    def CopyHDMXData(self) -> int:
        """
        Copy HDMX data from base to composite glyph
        """
        return self._CopyHDMXData

    @CopyHDMXData.setter
    def CopyHDMXData(self, value: int) -> None:
        self._CopyHDMXData = value

    @property
    def OTWriteMort(self) -> int:
        """
        Export "mort" table if possible?
        """
        return self._OTWriteMort

    @OTWriteMort.setter
    def OTWriteMort(self, value: int) -> None:
        self._OTWriteMort = value

    # TTEVersionOS2 = 3  # OS/2 table version 3

    @property
    def CacheTTUse(self) -> int:
        """
        Use CacheTT program to generate device metrics tables in TT fonts
        """
        return self._CacheTTUse

    @CacheTTUse.setter
    def CacheTTUse(self, value: int) -> None:
        self._CacheTTUse = value

    @property
    def CacheTTPath(self) -> str:
        """
        Location of the CacheTT.exe
        """
        return self._CacheTTPath

    @CacheTTPath.setter
    def CacheTTPath(self, value: str) -> None:
        self._CacheTTPath = value

    # -------------------------
    # -    TrueType Autohinting
    # -------------------------

    # ???

    # ----------------------------------
    # -    OpenType TT/TrueType Encoding
    # ----------------------------------

    # ??? See TTEExportUnicode

    # ----------------------------------
    # -    Generating OpenType PS (.otf)
    # ----------------------------------

    # TTEDecompose = 1  # Decompose all composites

    @property
    def TTESubrize(self) -> int:
        """
        Use subroutines to compress outlines in the CFF table
        """
        return self._TTESubrize

    @TTESubrize.setter
    def TTESubrize(self, value: int) -> None:
        self._TTESubrize = value

    # TTEAutohint? for OTF or TTF?
    # TTESmartFontName = 0  # Use the PostScript FontName as Full Name on Win?

    # ------------
    # -    Kerning
    # ------------

    # TTEWriteKernTable  # Export old-style non-OpenType "kern" table
    # ExpandKernFlags
    # ExpandKernCodepage
    # ExpandKernCount

    @property
    def TTEWriteKernFeature(self) -> int:
        """
        Generate OpenType "kern" feature if it is undefined or outdated?
        """
        return self._TTEWriteKernFeature

    @TTEWriteKernFeature.setter
    def TTEWriteKernFeature(self, value: int) -> None:
        self._TTEWriteKernFeature = value

    # -------------
    # Trace Options
    # -------------

    @property
    def TracerCurveFit(self) -> float:
        return self._TracerCurveFit

    @TracerCurveFit.setter
    def TracerCurveFit(self, value: int) -> None:
        self._TracerCurveFit = value

    @property
    def TracerCurves(self) -> int:
        return self._TracerCurves

    @TracerCurves.setter
    def TracerCurves(self, value: int) -> None:
        self._TracerCurves = value

    @property
    def TracerExtremePoints(self) -> int:
        return self._TracerExtremePoints

    @TracerExtremePoints.setter
    def TracerExtremePoints(self, value: int) -> None:
        self._TracerExtremePoints = value

    @property
    def TracerPresetMode(self) -> int:
        return self._TracerPresetMode

    @TracerPresetMode.setter
    def TracerPresetMode(self, value: int) -> None:
        self._TracerPresetMode = value

    @property
    def TracerStraightenAngle(self) -> int:
        return self._TracerStraightenAngle

    @TracerStraightenAngle.setter
    def TracerStraightenAngle(self, value: int) -> None:
        self._TracerStraightenAngle = value

    @property
    def TracerTolerance(self) -> int:
        return self._TracerTolerance

    @TracerTolerance.setter
    def TracerTolerance(self, value: int) -> None:
        self._TracerTolerance = value

    # Unsorted yet

    @property
    def AutoAlignVector(self) -> int:
        """
        Optimize - Auto-alignment level:

        - Do not align
        - Be very precise
        - Process normally
        - Align when possible
        - Extreme
        """
        return self._AutoAlignVector

    @AutoAlignVector.setter
    def AutoAlignVector(self, value: int) -> None:
        self._AutoAlignVector = value

    @property
    def AutoMetricsClose(self) -> int:
        return self._AutoMetricsClose

    @AutoMetricsClose.setter
    def AutoMetricsClose(self, value: int) -> None:
        self._AutoMetricsClose = value

    @property
    def AutoMetricsLeft(self) -> int:
        return self._AutoMetricsLeft

    @AutoMetricsLeft.setter
    def AutoMetricsLeft(self, value: int) -> None:
        self._AutoMetricsLeft = value

    @property
    def AutoMetricsRight(self) -> int:
        return self._AutoMetricsRight

    @AutoMetricsRight.setter
    def AutoMetricsRight(self, value: int) -> None:
        self._AutoMetricsRight = value

    @property
    def AutoRemoveHints(self) -> int:
        return self._AutoRemoveHints

    @AutoRemoveHints.setter
    def AutoRemoveHints(self, value: int) -> None:
        self._AutoRemoveHints = value

    @property
    def AutoSave(self) -> int:
        """
        Autosave fonts
        """
        return self._AutoSave

    @AutoSave.setter
    def AutoSave(self, value: int) -> None:
        self._AutoSave = value

    @property
    def AutoSaveTick(self) -> int:
        """
        Autosave fonts every _ minutes
        """
        return self._AutoSaveTick

    @AutoSaveTick.setter
    def AutoSaveTick(self, value: int) -> None:
        self._AutoSaveTick = value

    @property
    def AutohintingHRatio(self) -> float:
        return self._AutohintingHRatio

    @AutohintingHRatio.setter
    def AutohintingHRatio(self, value: float) -> None:
        self._AutohintingHRatio = value

    @property
    def AutohintingMaxHWidth(self) -> int:
        return self._AutohintingMaxHWidth

    @AutohintingMaxHWidth.setter
    def AutohintingMaxHWidth(self, value: int) -> None:
        self._AutohintingMaxHWidth = value

    @property
    def AutohintingMaxVWidth(self) -> int:
        return self._AutohintingMaxVWidth

    @AutohintingMaxVWidth.setter
    def AutohintingMaxVWidth(self, value: int) -> None:
        self._AutohintingMaxVWidth = value

    @property
    def AutohintingMinHLen(self) -> int:
        return self._AutohintingMinHLen

    @AutohintingMinHLen.setter
    def AutohintingMinHLen(self, value: int) -> None:
        self._AutohintingMinHLen = value

    @property
    def AutohintingMinHWidth(self) -> int:
        return self._AutohintingMinHWidth

    @AutohintingMinHWidth.setter
    def AutohintingMinHWidth(self, value: int) -> None:
        self._AutohintingMinHWidth = value

    @property
    def AutohintingMinVLen(self) -> int:
        return self._AutohintingMinVLen

    @AutohintingMinVLen.setter
    def AutohintingMinVLen(self, value: int) -> None:
        self._AutohintingMinVLen = value

    @property
    def AutohintingMinVWidth(self) -> int:
        return self._AutohintingMinVWidth

    @AutohintingMinVWidth.setter
    def AutohintingMinVWidth(self, value: int) -> None:
        self._AutohintingMinVWidth = value

    @property
    def AutohintingRemoveHints(self) -> int:
        return self._AutohintingRemoveHints

    @AutohintingRemoveHints.setter
    def AutohintingRemoveHints(self, value: int) -> None:
        self._AutohintingRemoveHints = value

    @property
    def AutohintingVRatio(self) -> float:
        return self._AutohintingVRatio

    @AutohintingVRatio.setter
    def AutohintingVRatio(self, value: float) -> None:
        self._AutohintingVRatio = value

    @property
    def Backup(self) -> int:
        """
        Create backup files
        """
        return self._Backup

    @Backup.setter
    def Backup(self, value: int) -> None:
        self._Backup = value

    @property
    def BitmapSize(self) -> int:
        """
        Bitmap height for the Create Bitmap command
        """
        return self._BitmapSize

    @BitmapSize.setter
    def BitmapSize(self, value: int) -> None:
        self._BitmapSize = value

    @property
    def ChartApplyTemplate(self) -> int:
        return self._ChartApplyTemplate

    @ChartApplyTemplate.setter
    def ChartApplyTemplate(self, value: int) -> None:
        self._ChartApplyTemplate = value

    @property
    def ChartAutoHide(self) -> int:
        return self._ChartAutoHide

    @ChartAutoHide.setter
    def ChartAutoHide(self, value: int) -> None:
        self._ChartAutoHide = value

    @property
    def ChartAutoUnicode(self) -> int:
        return self._ChartAutoUnicode

    @ChartAutoUnicode.setter
    def ChartAutoUnicode(self, value: int) -> None:
        self._ChartAutoUnicode = value

    @property
    def ChartCaptionFontCharSet(self) -> int:
        return self._ChartCaptionFontCharSet

    @ChartCaptionFontCharSet.setter
    def ChartCaptionFontCharSet(self, value: int) -> None:
        self._ChartCaptionFontCharSet = value

    @property
    def ChartCaptionFontName(self) -> str:
        return self._ChartCaptionFontName

    @ChartCaptionFontName.setter
    def ChartCaptionFontName(self, value: str) -> None:
        self._ChartCaptionFontName = value

    @property
    def ChartCaptionFontSize(self) -> int:
        return self._ChartCaptionFontSize

    @ChartCaptionFontSize.setter
    def ChartCaptionFontSize(self, value: int) -> None:
        self._ChartCaptionFontSize = value

    @property
    def ChartDoubleClick(self) -> int:
        return self._ChartDoubleClick

    @ChartDoubleClick.setter
    def ChartDoubleClick(self, value: int) -> None:
        self._ChartDoubleClick = value

    @property
    def ChartDragDrop(self) -> int:
        return self._ChartDragDrop

    @ChartDragDrop.setter
    def ChartDragDrop(self, value: int) -> None:
        self._ChartDragDrop = value

    @property
    def ChartPreviewMarks(self) -> int:
        return self._ChartPreviewMarks

    @ChartPreviewMarks.setter
    def ChartPreviewMarks(self, value: int) -> None:
        self._ChartPreviewMarks = value

    @property
    def ChartSampleSize(self) -> int:
        """
        Glyph cell - Each cell should have dimensions of _ pixels

        - 0: 16 x 16
        - 1: 24 x 24
        - 2: 32 x 32
        - 3: 48 x 48
        - 4: 64 x 64
        - 5: 96 x 96
        - 6: 128 x 128
        """
        return self._ChartSampleSize

    @ChartSampleSize.setter
    def ChartSampleSize(self, value: int) -> None:
        self._ChartSampleSize = value

    @property
    def ChartShowNotes(self) -> int:
        """
        Glyph cell - Show note icons
        """
        return self._ChartShowNotes

    @ChartShowNotes.setter
    def ChartShowNotes(self, value: int) -> None:
        self._ChartShowNotes = value

    @property
    def ChartSorting(self) -> int:
        return self._ChartSorting

    @ChartSorting.setter
    def ChartSorting(self, value: int) -> None:
        self._ChartSorting = value

    @property
    def ChartStyle(self) -> int:
        return self._ChartStyle

    @ChartStyle.setter
    def ChartStyle(self, value: int) -> None:
        self._ChartStyle = value

    @property
    def ChartTemplateFontCharSet(self) -> int:
        return self._ChartTemplateFontCharSet

    @ChartTemplateFontCharSet.setter
    def ChartTemplateFontCharSet(self, value: int) -> None:
        self._ChartTemplateFontCharSet = value

    @property
    def ChartTemplateFontName(self) -> str:
        return self._ChartTemplateFontName

    @ChartTemplateFontName.setter
    def ChartTemplateFontName(self, value: str) -> None:
        self._ChartTemplateFontName = value

    @property
    def ChartTemplateFontSize(self) -> int:
        return self._ChartTemplateFontSize

    @ChartTemplateFontSize.setter
    def ChartTemplateFontSize(self, value: int) -> None:
        self._ChartTemplateFontSize = value

    @property
    def ChartUseTemplate(self) -> int:
        return self._ChartUseTemplate

    @ChartUseTemplate.setter
    def ChartUseTemplate(self, value: int) -> None:
        self._ChartUseTemplate = value

    @property
    def ClosepathArrowLen(self) -> int:
        return self._ClosepathArrowLen

    @ClosepathArrowLen.setter
    def ClosepathArrowLen(self, value: int) -> None:
        self._ClosepathArrowLen = value

    @property
    def CodepagesCount(self) -> int:
        return self._CodepagesCount

    @CodepagesCount.setter
    def CodepagesCount(self, value: int) -> None:
        self._CodepagesCount = value

    @property
    def ColorBitmap(self) -> int:
        return self._ColorBitmap

    @ColorBitmap.setter
    def ColorBitmap(self, value: int) -> None:
        self._ColorBitmap = value

    @property
    def ColorClosepath(self) -> int:
        return self._ColorClosepath

    @ColorClosepath.setter
    def ColorClosepath(self, value: int) -> None:
        self._ColorClosepath = value

    @property
    def ColorEcho(self) -> int:
        return self._ColorEcho

    @ColorEcho.setter
    def ColorEcho(self, value: int) -> None:
        self._ColorEcho = value

    @property
    def ColorHintsPen(self) -> int:
        return self._ColorHintsPen

    @ColorHintsPen.setter
    def ColorHintsPen(self, value: int) -> None:
        self._ColorHintsPen = value

    @property
    def ColorMaskPen(self) -> int:
        return self._ColorMaskPen

    @ColorMaskPen.setter
    def ColorMaskPen(self, value: int) -> None:
        self._ColorMaskPen = value

    @property
    def ColorMetrics(self) -> int:
        return self._ColorMetrics

    @ColorMetrics.setter
    def ColorMetrics(self, value: int) -> None:
        self._ColorMetrics = value

    @property
    def ColorSeacPen(self) -> int:
        return self._ColorSeacPen

    @ColorSeacPen.setter
    def ColorSeacPen(self, value: int) -> None:
        self._ColorSeacPen = value

    @property
    def ColorTemplate(self) -> int:
        return self._ColorTemplate

    @ColorTemplate.setter
    def ColorTemplate(self, value: int) -> None:
        self._ColorTemplate = value

    @property
    def ColorVMetrics(self) -> int:
        return self._ColorVMetrics

    @ColorVMetrics.setter
    def ColorVMetrics(self, value: int) -> None:
        self._ColorVMetrics = value

    @property
    def CreateUnexistingCharacters(self) -> int:
        return self._CreateUnexistingCharacters

    @CreateUnexistingCharacters.setter
    def CreateUnexistingCharacters(self, value: int) -> None:
        self._CreateUnexistingCharacters = value

    @property
    def CustomMarkColor(self) -> int:
        return self._CustomMarkColor

    @CustomMarkColor.setter
    def CustomMarkColor(self, value: int) -> None:
        self._CustomMarkColor = value

    @property
    def DefaultGlyph(self) -> int:
        return self._DefaultGlyph

    @DefaultGlyph.setter
    def DefaultGlyph(self, value: int) -> None:
        self._DefaultGlyph = value

    @property
    def DuplicateX(self) -> int:
        return self._DuplicateX

    @DuplicateX.setter
    def DuplicateX(self, value: int) -> None:
        self._DuplicateX = value

    @property
    def DuplicateY(self) -> int:
        return self._DuplicateY

    @DuplicateY.setter
    def DuplicateY(self, value: int) -> None:
        self._DuplicateY = value

    @property
    def EditBCPsFixed(self) -> int:
        """
        Advanced - All BCPs are fixed
        """
        return self._EditBCPsFixed

    @EditBCPsFixed.setter
    def EditBCPsFixed(self, value: int) -> None:
        self._EditBCPsFixed = value

    @property
    def EditBitmapStyle(self) -> int:
        return self._EditBitmapStyle

    @EditBitmapStyle.setter
    def EditBitmapStyle(self, value: int) -> None:
        self._EditBitmapStyle = value

    @property
    def EditChangeCursor(self) -> int:
        return self._EditChangeCursor

    @EditChangeCursor.setter
    def EditChangeCursor(self, value: int) -> None:
        self._EditChangeCursor = value

    @property
    def EditFollowScroll(self) -> int:
        return self._EditFollowScroll

    @EditFollowScroll.setter
    def EditFollowScroll(self, value: int) -> None:
        self._EditFollowScroll = value

    @property
    def EditGridX(self) -> int:
        return self._EditGridX

    @EditGridX.setter
    def EditGridX(self, value: int) -> None:
        self._EditGridX = value

    @property
    def EditGridY(self) -> int:
        return self._EditGridY

    @EditGridY.setter
    def EditGridY(self, value: int) -> None:
        self._EditGridY = value

    @property
    def EditHandleTool(self) -> int:
        return self._EditHandleTool

    @EditHandleTool.setter
    def EditHandleTool(self, value: int) -> None:
        self._EditHandleTool = value

    @property
    def EditHitDistance(self) -> int:
        return self._EditHitDistance

    @EditHitDistance.setter
    def EditHitDistance(self, value: int) -> None:
        self._EditHitDistance = value

    @property
    def EditInstantRefresh(self) -> int:
        return self._EditInstantRefresh

    @EditInstantRefresh.setter
    def EditInstantRefresh(self, value: int) -> None:
        self._EditInstantRefresh = value

    @property
    def EditLeaveEcho(self) -> int:
        """
        Outline drawing - Leave echo while editing
        """
        return self._EditLeaveEcho

    @EditLeaveEcho.setter
    def EditLeaveEcho(self, value: int) -> None:
        self._EditLeaveEcho = value

    @property
    def EditNotFillOpen(self) -> int:
        """
        Outline drawing - Fill open contours
        """
        return self._EditNotFillOpen

    @EditNotFillOpen.setter
    def EditNotFillOpen(self, value: int) -> None:
        self._EditNotFillOpen = value

    @property
    def EditRulers(self) -> int:
        return self._EditRulers

    @EditRulers.setter
    def EditRulers(self, value: int) -> None:
        self._EditRulers = value

    @property
    def EditScaleEPS(self) -> int:
        return self._EditScaleEPS

    @EditScaleEPS.setter
    def EditScaleEPS(self, value: int) -> None:
        self._EditScaleEPS = value

    @property
    def EditShowCross(self) -> int:
        """
        Editing behaviour - Show crosshair cursor
        """
        return self._EditShowCross

    @EditShowCross.setter
    def EditShowCross(self, value: int) -> None:
        self._EditShowCross = value

    @property
    def EditShowPosition(self) -> int:
        return self._EditShowPosition

    @EditShowPosition.setter
    def EditShowPosition(self, value: int) -> None:
        self._EditShowPosition = value

    @property
    def EditSmallNodes(self) -> int:
        """
        Appearance - Small nodes
        """
        return self._EditSmallNodes

    @EditSmallNodes.setter
    def EditSmallNodes(self, value: int) -> None:
        self._EditSmallNodes = value

    @property
    def EditSmoothOutline(self) -> int:
        """
        Outline drawing - Smooth outline
        """
        return self._EditSmoothOutline

    @EditSmoothOutline.setter
    def EditSmoothOutline(self, value: int) -> None:
        self._EditSmoothOutline = value

    @property
    def EraseSize(self) -> int:
        return self._EraseSize

    @EraseSize.setter
    def EraseSize(self, value: int) -> None:
        self._EraseSize = value

    @property
    def FitAscender(self) -> int:
        return self._FitAscender

    @FitAscender.setter
    def FitAscender(self, value: int) -> None:
        self._FitAscender = value

    @property
    def FitDescender(self) -> int:
        return self._FitDescender

    @FitDescender.setter
    def FitDescender(self, value: int) -> None:
        self._FitDescender = value

    @property
    def FontAudit(self) -> int:
        return self._FontAudit

    @FontAudit.setter
    def FontAudit(self, value: int) -> None:
        self._FontAudit = value

    @property
    def GlyphsBarOpen(self) -> int:
        return self._GlyphsBarOpen

    @GlyphsBarOpen.setter
    def GlyphsBarOpen(self, value: int) -> None:
        self._GlyphsBarOpen = value

    @property
    def HideAllLayers(self) -> int:
        return self._HideAllLayers

    @HideAllLayers.setter
    def HideAllLayers(self, value: int) -> None:
        self._HideAllLayers = value

    @property
    def HideToolbars(self) -> int:
        return self._HideToolbars

    @HideToolbars.setter
    def HideToolbars(self, value: int) -> None:
        self._HideToolbars = value

    @property
    def LockStyleEx(self) -> int:
        return self._LockStyleEx

    @LockStyleEx.setter
    def LockStyleEx(self, value: int) -> None:
        self._LockStyleEx = value

    @property
    def OTAddClasses(self) -> int:
        """
        Add all glyph classes to OpenType feature definition code
        """
        return self._OTAddClasses

    @OTAddClasses.setter
    def OTAddClasses(self, value: int) -> None:
        self._OTAddClasses = value

    @property
    def OptimizeAlign(self) -> int:
        return self._OptimizeAlign

    @OptimizeAlign.setter
    def OptimizeAlign(self, value: int) -> None:
        self._OptimizeAlign = value

    @property
    def OptimizeReduce(self) -> int:
        return self._OptimizeReduce

    @OptimizeReduce.setter
    def OptimizeReduce(self, value: int) -> None:
        self._OptimizeReduce = value

    @property
    def OverlapMode(self) -> int:
        return self._OverlapMode

    @OverlapMode.setter
    def OverlapMode(self, value: int) -> None:
        self._OverlapMode = value

    @property
    def PaintAutoTransform(self) -> int:
        return self._PaintAutoTransform

    @PaintAutoTransform.setter
    def PaintAutoTransform(self, value: int) -> None:
        self._PaintAutoTransform = value

    @property
    def PaintAutoView(self) -> int:
        return self._PaintAutoView

    @PaintAutoView.setter
    def PaintAutoView(self, value: int) -> None:
        self._PaintAutoView = value

    @property
    def PaintBrushBody(self) -> int:
        return self._PaintBrushBody

    @PaintBrushBody.setter
    def PaintBrushBody(self, value: int) -> None:
        self._PaintBrushBody = value

    @property
    def PaintBrushCap(self) -> int:
        return self._PaintBrushCap

    @PaintBrushCap.setter
    def PaintBrushCap(self, value: int) -> None:
        self._PaintBrushCap = value

    @property
    def PaintBrushJoin(self) -> int:
        return self._PaintBrushJoin

    @PaintBrushJoin.setter
    def PaintBrushJoin(self, value: int) -> None:
        self._PaintBrushJoin = value

    @property
    def PaintBrushRoundness(self) -> int:
        return self._PaintBrushRoundness

    @PaintBrushRoundness.setter
    def PaintBrushRoundness(self, value: int) -> None:
        self._PaintBrushRoundness = value

    @property
    def PaintBrushVectorX(self) -> float:
        return self._PaintBrushVectorX

    @PaintBrushVectorX.setter
    def PaintBrushVectorX(self, value: float) -> None:
        self._PaintBrushVectorX = value

    @property
    def PaintBrushVectorY(self) -> float:
        return self._PaintBrushVectorY

    @PaintBrushVectorY.setter
    def PaintBrushVectorY(self, value: float) -> None:
        self._PaintBrushVectorY = value

    @property
    def PaintBrushWidth(self) -> int:
        return self._PaintBrushWidth

    @PaintBrushWidth.setter
    def PaintBrushWidth(self, value: int) -> None:
        self._PaintBrushWidth = value

    @property
    def PaintColor(self) -> int:
        return self._PaintColor

    @PaintColor.setter
    def PaintColor(self, value: int) -> None:
        self._PaintColor = value

    @property
    def PaintMode(self) -> int:
        return self._PaintMode

    @PaintMode.setter
    def PaintMode(self, value: int) -> None:
        self._PaintMode = value

    @property
    def PaintStyleEx(self) -> int:
        return self._PaintStyleEx

    @PaintStyleEx.setter
    def PaintStyleEx(self, value: int) -> None:
        self._PaintStyleEx = value

    @property
    def PaintTextSize(self) -> int:
        return self._PaintTextSize

    @PaintTextSize.setter
    def PaintTextSize(self, value: int) -> None:
        self._PaintTextSize = value

    @property
    def PaintTool(self) -> int:
        return self._PaintTool

    @PaintTool.setter
    def PaintTool(self, value: int) -> None:
        self._PaintTool = value

    @property
    def PaintTracePolygon(self) -> int:
        return self._PaintTracePolygon

    @PaintTracePolygon.setter
    def PaintTracePolygon(self, value: int) -> None:
        self._PaintTracePolygon = value

    @property
    def PasteX(self) -> int:
        return self._PasteX

    @PasteX.setter
    def PasteX(self, value: int) -> None:
        self._PasteX = value

    @property
    def PasteY(self) -> int:
        return self._PasteY

    @PasteY.setter
    def PasteY(self, value: int) -> None:
        self._PasteY = value

    @property
    def PreviewExpanded(self) -> int:
        return self._PreviewExpanded

    @PreviewExpanded.setter
    def PreviewExpanded(self, value: int) -> None:
        self._PreviewExpanded = value

    @property
    def PreviewExpandedHeight(self) -> int:
        return self._PreviewExpandedHeight

    @PreviewExpandedHeight.setter
    def PreviewExpandedHeight(self, value: int) -> None:
        self._PreviewExpandedHeight = value

    @property
    def PreviewPPMs(self) -> str:
        return self._PreviewPPMs

    @PreviewPPMs.setter
    def PreviewPPMs(self, value: str) -> None:
        self._PreviewPPMs = value

    @property
    def PreviewPPMsExpanded(self) -> str:
        return self._PreviewPPMsExpanded

    @PreviewPPMsExpanded.setter
    def PreviewPPMsExpanded(self, value: str) -> None:
        self._PreviewPPMsExpanded = value

    @property
    def PreviewPointSize(self) -> str:
        return self._PreviewPointSize

    @PreviewPointSize.setter
    def PreviewPointSize(self, value: str) -> None:
        self._PreviewPointSize = value

    @property
    def PreviewSecondLine(self) -> str:
        return self._PreviewSecondLine

    @PreviewSecondLine.setter
    def PreviewSecondLine(self, value: str) -> None:
        self._PreviewSecondLine = value

    @property
    def PreviewSmooth(self) -> int:
        return self._PreviewSmooth

    @PreviewSmooth.setter
    def PreviewSmooth(self, value: int) -> None:
        self._PreviewSmooth = value

    @property
    def PreviewWidth(self) -> int:
        return self._PreviewWidth

    @PreviewWidth.setter
    def PreviewWidth(self, value: int) -> None:
        self._PreviewWidth = value

    @property
    def SamplePPM1(self) -> int:
        return self._SamplePPM1

    @SamplePPM1.setter
    def SamplePPM1(self, value: int) -> None:
        self._SamplePPM1 = value

    @property
    def SamplePPM2(self) -> int:
        return self._SamplePPM2

    @SamplePPM2.setter
    def SamplePPM2(self, value: int) -> None:
        self._SamplePPM2 = value

    @property
    def SnapStyleEx(self) -> int:
        return self._SnapStyleEx

    @SnapStyleEx.setter
    def SnapStyleEx(self, value: int) -> None:
        self._SnapStyleEx = value

    @property
    def T1AFM(self) -> int:
        return self._T1AFM

    @T1AFM.setter
    def T1AFM(self, value: int) -> None:
        """
        Make AFM and INF files
        """
        self._T1AFM = value

    @property
    def T1Autohint(self) -> int:
        """
        Autohint unhinted glyphs
        """
        return self._T1Autohint

    @T1Autohint.setter
    def T1Autohint(self, value: int) -> None:
        self._T1Autohint = value

    @property
    def T1Decompose(self) -> int:
        return self._T1Decompose

    @T1Decompose.setter
    def T1Decompose(self, value: int) -> None:
        self._T1Decompose = value

    @property
    def T1Encoding(self) -> int:
        return self._T1Encoding

    @T1Encoding.setter
    def T1Encoding(self, value: int) -> None:
        """
        Encoding options:

        - Always write custom encoding
        - Always write standard encoding
        - Export Unicode codepage if codepage mode is active
        - Select encoding automatically
        """
        self._T1Encoding = value

    @property
    def T1PFM(self) -> int:
        """
        Make PFM file
        """
        return self._T1PFM

    @T1PFM.setter
    def T1PFM(self, value: int) -> None:
        self._T1PFM = value

    @property
    def T1Sort(self) -> int:
        """
        Automatically sort glyphs
        """
        return self._T1Sort

    @T1Sort.setter
    def T1Sort(self, value: int) -> None:
        self._T1Sort = value

    @property
    def T1Terminal(self) -> int:
        """
        Open Type 1 Export Terminal
        """
        return self._T1Terminal

    @T1Terminal.setter
    def T1Terminal(self, value: int) -> None:
        self._T1Terminal = value

    @property
    def T1Unicode(self) -> int:
        return self._T1Unicode

    @T1Unicode.setter
    def T1Unicode(self, value: int) -> None:
        self._T1Unicode = value

    @property
    def T1UseOS2(self) -> int:
        return self._T1UseOS2

    @T1UseOS2.setter
    def T1UseOS2(self, value: int) -> None:
        self._T1UseOS2 = value

    @property
    def TTEAddCharacters(self) -> int:
        return self._TTEAddCharacters

    @TTEAddCharacters.setter
    def TTEAddCharacters(self, value: int) -> None:
        self._TTEAddCharacters = value

    @property
    def TTEApplyBBoxSavings(self) -> int:
        return self._TTEApplyBBoxSavings

    @TTEApplyBBoxSavings.setter
    def TTEApplyBBoxSavings(self, value: int) -> None:
        self._TTEApplyBBoxSavings = value

    @property
    def TTEAutoWinAscDesc(self) -> int:
        return self._TTEAutoWinAscDesc

    @TTEAutoWinAscDesc.setter
    def TTEAutoWinAscDesc(self, value: int) -> None:
        self._TTEAutoWinAscDesc = value

    @property
    def TTECmap10(self) -> int:
        """
        option:   - Use following codepage to build cmap(1,0) table:
                    [Current codepage in the Font Window]

        Returns:
            int: _description_
        """
        return self._TTECmap10

    @TTECmap10.setter
    def TTECmap10(self, value: int) -> None:
        self._TTECmap10 = value

    @property
    def TTEheadBBoxSavings(self) -> int:
        return self._TTEheadBBoxSavings

    @TTEheadBBoxSavings.setter
    def TTEheadBBoxSavings(self, value: int) -> None:
        self._TTEheadBBoxSavings = value

    @property
    def TTHHintingOptions(self) -> int:
        return self._TTHHintingOptions

    @TTHHintingOptions.setter
    def TTHHintingOptions(self, value: int) -> None:
        self._TTHHintingOptions = value

    @property
    def TTIAutohint(self) -> int:
        """
        Autohint font
        """
        return self._TTIAutohint

    @TTIAutohint.setter
    def TTIAutohint(self, value: int) -> None:
        self._TTIAutohint = value

    @property
    def TTIConvert(self) -> int:
        """
        Convert TrueType curves into PostScript curves
        """
        return self._TTIConvert

    @TTIConvert.setter
    def TTIConvert(self, value: int) -> None:
        self._TTIConvert = value

    @property
    def TTIDecompose(self) -> int:
        """
        Decompose composites
        """
        return self._TTIDecompose

    @TTIDecompose.setter
    def TTIDecompose(self, value: int) -> None:
        self._TTIDecompose = value

    @property
    def TTIFontNames(self) -> int:
        """
        - Read only non-English name records
        - Do not read OpenType name records
        - Read all OpenType name records
        """
        return self._TTIFontNames

    @TTIFontNames.setter
    def TTIFontNames(self, value: int) -> None:
        self._TTIFontNames = value

    @property
    def TTIKeepHints(self) -> int:
        """
        Store TrueType native hinting
        """
        return self._TTIKeepHints

    @TTIKeepHints.setter
    def TTIKeepHints(self, value: int) -> None:
        self._TTIKeepHints = value

    @property
    def TTIReadBitmaps(self) -> int:
        """
        Import embedded bitmaps
        """
        return self._TTIReadBitmaps

    @TTIReadBitmaps.setter
    def TTIReadBitmaps(self, value: int) -> None:
        self._TTIReadBitmaps = value

    @property
    def TTIReadKernFeature(self) -> int:
        """
        Import kerning from the "kern" feature
        """
        return self._TTIReadKernFeature

    @TTIReadKernFeature.setter
    def TTIReadKernFeature(self, value: int) -> None:
        self._TTIReadKernFeature = value

    @property
    def TTIReadOT(self) -> int:
        """
        Interpret OpenType layout tables
        """
        return self._TTIReadOT

    @TTIReadOT.setter
    def TTIReadOT(self, value: int) -> None:
        self._TTIReadOT = value

    @property
    def TTIScale1000(self) -> int:
        """
        Scale the font to 1000 UPM
        """
        return self._TTIScale1000

    @TTIScale1000.setter
    def TTIScale1000(self, value: int) -> None:
        self._TTIScale1000 = value

    @property
    def TTIStoreTables(self) -> int:
        """
        Store custom TrueType/OpenType tables
        """
        return self._TTIStoreTables

    @TTIStoreTables.setter
    def TTIStoreTables(self, value: int) -> None:
        self._TTIStoreTables = value

    @property
    def TTToolReverseShift(self) -> int:
        """
        Shift key constrains setting of the delta instruction's direction?
        """
        return self._TTToolReverseShift

    @TTToolReverseShift.setter
    def TTToolReverseShift(self, value: int) -> None:
        self._TTToolReverseShift = value

    @property
    def TrackingDistance(self) -> int:
        """
        Tracking offset: _ % of UPM

        Stored value is 10x that in the UI
        """
        return self._TrackingDistance

    @TrackingDistance.setter
    def TrackingDistance(self, value: int) -> None:
        self._TrackingDistance = value

    @property
    def TrackingMode(self) -> int:
        return self._TrackingMode

    @TrackingMode.setter
    def TrackingMode(self, value: int) -> None:
        self._TrackingMode = value

    @property
    def UnicodeRangePercent(self) -> int:
        return self._UnicodeRangePercent

    @UnicodeRangePercent.setter
    def UnicodeRangePercent(self, value: int) -> None:
        self._UnicodeRangePercent = value

    @property
    def VendorCode(self) -> str:
        return self._VendorCode

    @VendorCode.setter
    def VendorCode(self, value: str) -> None:
        self._VendorCode = value

    # Not implemented in FontLab 4.5.2 Win:

    @property
    def ContourSnapAllPoints(self) -> int:
        return self._ContourSnapAllPoints

    @ContourSnapAllPoints.setter
    def ContourSnapAllPoints(self, value: int) -> None:
        self._ContourSnapAllPoints = value

    @property
    def EditDeleteAlt(self) -> int:
        return self._EditDeleteAlt

    @EditDeleteAlt.setter
    def EditDeleteAlt(self, value: int) -> None:
        self._EditDeleteAlt = value

    @property
    def EditDoubleClickBitmap(self) -> int:
        return self._EditDoubleClickBitmap

    @EditDoubleClickBitmap.setter
    def EditDoubleClickBitmap(self, value: int) -> None:
        self._EditDoubleClickBitmap = value

    @property
    def EditEditSelection(self) -> int:
        return self._EditEditSelection

    @EditEditSelection.setter
    def EditEditSelection(self, value: int) -> None:
        self._EditEditSelection = value

    @property
    def EditNoToolbars(self) -> None:
        raise AttributeError  # In FLS 5

    @EditNoToolbars.setter
    def EditNoToolbars(self, value: Any) -> None:
        self._EditNoToolbars = value

    @property
    def EditShowSelection(self) -> int:
        """
        Show selected nodes in inactive masters
        """
        return self._EditShowSelection

    @EditShowSelection.setter
    def EditShowSelection(self, value: int) -> None:
        self._EditShowSelection = value

    @property
    def NamesFileName(self) -> str:
        """
        Default Unicode-Name mapping table?

        (Not stored in registry file, or not stored == standard.nam?)
        """
        return self._NamesFileName

    @NamesFileName.setter
    def NamesFileName(self, value: str) -> None:
        self._NamesFileName = value

    @property
    def OTReadMort(self) -> int:
        """
        Interpret GX/AAT mort & morx tables
        """
        return self._OTReadMort

    @OTReadMort.setter
    def OTReadMort(self, value: int) -> None:
        self._OTReadMort = value

    @property
    def ShowMeterPanel(self) -> int:
        """
        Editing behavior - Show meter panel when Meter tool is activated
        """
        return self._ShowMeterPanel

    @ShowMeterPanel.setter
    def ShowMeterPanel(self, value: int) -> None:
        self._ShowMeterPanel = value

    @property
    def UnicodeStrings(self) -> int:
        """
        Allow to enter Unicode strings in dialogs

        Windows 2000 or Windows XP required ;)
        """
        return self._UnicodeStrings

    @UnicodeStrings.setter
    def UnicodeStrings(self, value: int) -> None:
        self._UnicodeStrings = value

    # Methods

    def Init(self) -> None:
        """
        Reset FontLab Options to default settings
        """
        # These are not FL's default settings right now,
        # but sensible defaults set by an experienced user *cough*
        self.AutoAlignVector = 1
        self.AutohintingHRatio = 2.0
        self.AutohintingMaxHWidth = 0x00000082
        self.AutohintingMaxVWidth = 0x00000082
        self.AutohintingMinHLen = 0x0000001E
        self.AutohintingMinHWidth = 0x00000028
        self.AutohintingMinVLen = 0x0000001E
        self.AutohintingMinVWidth = 0x00000028
        self.AutohintingRemoveHints = 1
        self.AutohintingVRatio = 2.0
        self.AutoMetricsClose = 0x0000000A
        self.AutoMetricsLeft = 0x0000001E
        self.AutoMetricsRight = 0x0000001E
        self.AutoRemoveHints = 1
        self.AutoSave = 0
        self.AutoSaveTick = 0x0000000A
        self.Backup = 1
        self.BitmapSize = 0x000007D0
        self.CacheTTPath = ""
        self.CacheTTUse = 0
        self.ChartApplyTemplate = 0
        self.ChartAutoHide = 0
        self.ChartAutoUnicode = 1
        self.ChartCaptionFontCharSet = 0
        self.ChartCaptionFontName = "Geneva"
        self.ChartCaptionFontSize = 0x0000005A
        self.ChartDoubleClick = 1
        self.ChartDragDrop = 1
        self.ChartPreviewMarks = 1
        self.ChartSampleSize = 2
        self.ChartShowNotes = 1
        self.ChartSorting = 2
        self.ChartStyle = 0x000009F3
        self.ChartTemplateFontCharSet = 0
        self.ChartTemplateFontName = "Symbola"
        self.ChartTemplateFontSize = 0x000000F0
        self.ChartUseTemplate = 1
        self.ClosepathArrowLen = 0x00000008
        self.CodepagesCount = 0x00000098
        self.ColorBitmap = 0xFFB8B8C8
        self.ColorClosepath = 0x00C0C0C0
        self.ColorEcho = 0xFF8C8C8C
        self.ColorHintsPen = 0xFF008000
        self.ColorMaskPen = 0x01CE753E
        self.ColorSeacPen = 0xFF808080
        self.ColorTemplate = 0xFFFFC0C0
        self.ColorVMetrics = 0xFF808080
        self.ContourSnapAllPoints = 0
        self.CopyHDMXData = 1  # Copy HDMX data from base to composite glyph
        self.CreateUnexistingCharacters = 0
        self.DefaultGlyph = 0x00000041
        self.DuplicateX = 0x00000064
        self.DuplicateY = 0x00000064
        self.EditBCPsFixed = 1
        self.EditBitmapStyle = 0
        self.EditChangeCursor = 1
        self.EditDeleteAlt = 0
        self.EditDoubleClickBitmap = 1
        self.EditEditSelection = 0
        self.EditFollowScroll = 1
        self.EditGridX = 0x00000032
        self.EditGridY = 0x00000032
        self.EditHandleTool = 1
        self.EditHitDistance = 3
        self.EditInstantRefresh = 0
        self.EditLeaveEcho = 1
        self.EditNotFillOpen = 1
        # self.EditNoToolbars = value
        self.EditRulers = 1
        self.EditScaleEPS = 0
        self.EditShowCross = 1
        self.EditShowPosition = 3
        self.EditShowSelection = 1
        self.EditSmallNodes = 0
        self.EditSmoothOutline = 1
        self.EraseSize = 5
        self.FitAscender = 0x000003E8
        self.FitDescender = 0xFFFFFE70
        self.FontAudit = 0xFFFF7FFF
        self.GlyphsBarOpen = 1
        self.HideAllLayers = 0
        self.HideToolbars = 0
        self.LockStyleEx = 0
        # self.NamesFileName = value
        self.OptimizeAlign = 1
        self.OptimizeReduce = 1
        self.OTAddClasses = 1
        self.OTReadMort = 0
        self.OTWriteGDEF = 0
        self.OTWriteMort = 0
        self.OverlapMode = 2
        self.PaintAutoTransform = 0
        self.PaintAutoView = 0
        self.PaintBrushBody = 0
        self.PaintBrushCap = 0
        self.PaintBrushJoin = 1
        self.PaintBrushRoundness = 0x0320
        self.PaintBrushVectorX = 0x00000068
        self.PaintBrushVectorY = 0x000003E2
        self.PaintBrushWidth = 0x00000078
        self.PaintColor = 3
        self.PaintMode = 2
        self.PaintStyleEx = 0x30849893
        self.PaintTextSize = 0x0000012C
        self.PaintTool = 6
        self.PaintTracePolygon = 0
        self.PasteX = 0
        self.PasteY = 0
        self.PreviewExpanded = 1
        self.PreviewExpandedHeight = 0x000003E8
        self.PreviewPointSize = "5-36, 38, 40, 42, 48"
        self.PreviewPPMs = "5-36, 38, 40, 42, 48"
        self.PreviewPPMsExpanded = "8-40"
        self.PreviewSecondLine = "Tonn Hauvonid DHLYENO"
        self.PreviewSmooth = 0
        self.PreviewWidth = 0x0000033B
        self.SamplePPM1 = 0x07FFFFC0
        self.SamplePPM2 = 0
        self.ShowMeterPanel = 1
        self.SnapStyleEx = 0xF
        self.T1AFM = 0
        self.T1Autohint = 0
        self.T1Decompose = 0
        self.T1Encoding = 1
        self.T1PFM = 0
        self.T1Terminal = 0
        self.T1Unicode = 1
        self.T1UseOS2 = 0
        self.TracerCurveFit = 0x00004E20
        self.TracerCurves = 1
        self.TracerExtremePoints = 1
        self.TracerPresetMode = 0
        self.TracerStraightenAngle = 3
        self.TracerTolerance = 3
        self.TrackingDistance = 0x32
        self.TrackingMode = 0
        self.TTEAddCharacters = 0
        self.TTEApplyBBoxSavings = 1
        self.TTEAutohint = 0
        self.TTEAutoWinAscDesc = 1
        self.TTECmap10 = 0
        self.TTEExportOT = 1
        self.TTEExportUnicode = 1
        self.TTEExportVOLT = 0
        self.TTEFontNames = 2
        self.TTEheadBBoxSavings = 0x40
        self.TTEHint = 1
        self.TTEKeep = 0
        self.TTENoReorder = 1
        self.TTESubrize = 1
        self.TTEVisual = 1
        self.TTEWriteBitmaps = 0
        self.TTEWriteKernFeature = 0
        self.TTHHintingOptions = 0x00001107
        self.TTIAutohint = 0
        self.TTIConvert = 0
        self.TTIDecompose = 0
        self.TTIFontNames = 2
        self.TTIKeepHints = 1
        self.TTIReadBitmaps = 1
        self.TTIReadKernFeature = 1
        self.TTIReadOT = 1
        self.TTIScale1000 = 0
        self.TTIStoreTables = 0
        self.TTToolReverseShift = 1
        self.UnicodeRangePercent = 0
        self.UnicodeStrings = 1
        self.VendorCode = "pyrs"

        # Not documented

        self.ATMPPM = 0x0000002A
        self.ATMScaler = 0x61747375
        self.ATMSmooth = 1
        self.AutohintingEngine = 0  # Autohinting engine: 0 = FontLab, 1 = Adobe
        self.ChartAutoActivateCodepage = 1  # Automaticall activate related codepage ...
        self.ChartCopyKerning = 0  # Kerning information is copied with the glyph
        self.ChartGenerate = 1  # Create Glyphs command generates them if possible?
        self.ChartGenerateRTL = 0  # All generated ligatures are right-to-left
        self.ColorBackground = 0xFFFFFFFF
        self.ColorBackgroundMask = 0xFFFFF0FF
        self.ColorBackgroundMetrics = 0xFFFFFFF0
        self.ColorForegroundMetrics = 0xFF000000
        self.ColorGlobalGuide = 0xFFFF0000
        self.ColorGrid = 0xFFE7E7E7
        self.ColorGroups = 0xFFE0E0E0
        self.ColorGuide = 0xFF0000FF
        self.ColorMetrics = 0x008C8C8C
        self.ColorNeighbors = 0xFF404040
        self.ColorOutline = 0xFF000000
        self.ColorTemplate = 0xFFFFC0C0
        self.ControlSwitch = 0
        self.CustomDict = "*"
        self.CustomMarkColor = 0x00000028
        self.DSIG_KeyPath = ""  # Path to the private key file (.pvk
        self.DSIG_Password = ""  # Use the following password every time
        self.DSIG_SertPath = ""  # Path to the certificate file (.spc or .cer)
        self.DSIG_TimeStamp = 0  # Generate the time stamp
        self.DSIG_Use = 0  # Generate digital signature (DSIG table)
        self.EditAllSmooth = 1  # Mask and inactive masters are smooth too
        self.EditAutoSelectLayers = 1
        self.EditBCVOpacity = 0x00000032
        self.EditComponentsByOutline = 0  # Comp. are selected only by click to contour
        self.EditConnectMasters = 0  # Appear. - Connect selected nodes in all masters
        self.EditDoubleClickMask = 1  # Double-click on background to change its prop.?
        self.EditInstantRefresh = 0
        self.EditKeyboardEditBCP = 1  # When curve is selected keyboard adjusts BCPs
        self.EditLayersExpanded = 1
        self.EditPreviewKey = 0x000000C0
        self.EditShowAnchorNames = 1  # Appearance - Show anchor names
        self.EditShowMasterPoints = 1
        self.EditShowMeasurementLine = 1
        self.EditShowNodesSelection = 1
        self.EditSmoothIsSmooth = 1  # Keep smooth connection smooth at all times
        self.EditThickOutline = 0  # Outline drawing - Thick outline
        self.EditUndoSelection = 0  # Editing b. - Sel. in the Glyph window is undoable
        self.EditZoomMode = 0x00000007
        self.EmbeddingType = 0x00000004
        self.EnableExtPythonEditor = 1
        self.EnablePython = 1
        self.EnableStickPanels = 0
        self.EnableTooltips = 1
        self.ExpandKernCodepage = "MS Windows 1252 Western (ANSI)"
        self.ExpandKernCount = 0x00002AA7
        self.ExpandKernFlags = 0x00000012
        self.ExtPythonEditor = "/Applications/TextMate.app"
        self.FileOpenSample = "ABRaeg123"
        self.FontAuditLive = 0  # Live FontAudit checks
        self.FontDialogName = "Lucida Grande"
        self.FontDialogSize = 0x0000005A
        self.FontExpanded = 1
        self.FontFixedName = "Lucida Grande"
        self.FontFixedSize = 0x00000050
        self.FontLabNodes = 0  # Small nodes?
        self.FontPanelName = "Lucida Grande"
        self.FontPanelSize = 0x0000005A
        self.FontRulerName = "Lucida Grande"
        self.FontRulerSize = 0x0000005A
        self.FontSmallName = ".TiniNumbers"
        self.FontSmallSize = 0x00000046
        self.FontTableName = "Lucida Grande"
        self.FontTableSize = 0x00000050
        self.GlyphNameSortMode = 1
        self.GlyphsBarTop = 1
        self.GroupCenter = 0
        self.GroupDoubleClick = 1
        self.GroupFill = 0
        self.GroupKerning = 1
        self.GroupMask = 0
        self.GroupShapeFill = 0
        self.GroupShapeMask = 0
        self.GroupShapeOpacity = 0x00000019
        self.GroupShiftX = 0
        self.GroupShiftY = 0
        self.GroupUseMetrics = 0
        self.MacroFontName = "Andale Mono"
        self.MaskMetrics = 1
        self.MetricsBarExpanded0 = 0
        self.MetricsBarExpanded1 = 1
        self.MetricsBarExpanded2 = 1
        self.MetricsBarExpanded3 = 1
        self.MetricsBottomBar0 = 0
        self.MetricsBottomBar1 = 1
        self.MetricsBottomBar2 = 1
        self.MetricsBottomBar3 = 1
        self.MetricsShowBar0 = 1
        self.MetricsShowBar1 = 1
        self.MetricsShowBar2 = 1
        self.MetricsShowBar3 = 1
        self.MetricsShowTable0 = 0
        self.MetricsShowTable1 = 1
        self.MetricsShowTable2 = 1
        self.MetricsShowTable3 = 1
        self.MMExtrapolation = 0  # Enable Multiple Master extrapolation
        self.OpenOutput = 1  # Automatically open Output panel if message is waiting
        self.OTAddMetricsClasses = 0  # Do not add metrics classes
        self.OTCompileFeatures = 1  # Compile feature definitions
        self.OTGenerate = 0  # Generate basic OpenType features for Type 1 fonts?
        self.OTOldContextRule = 0  # Contextual substitutions in invalid legacy format
        self.OTPreviewSize = 0x00000080
        self.OTSampleSize = 0x00000060
        self.OutputFontName = "Andale Mono"
        self.PaintJapanese = 0
        self.PaintReverseBrushAutoColor = 0
        self.PaintTextFont = "Arial"
        self.PreviewAlternativeArrows = 0
        self.PreviewApplyTemplate = 1
        self.PreviewAutoScroll = 1
        self.PreviewAutoWrap = 1
        self.PreviewBlueColor = 0xFF1A1D1E
        self.PreviewFilterKerning = 0
        self.PreviewFilterMetrics = 1
        self.PreviewFocusString = 1
        self.PreviewHighlightKeyGlyphs = 0
        self.PreviewKeepExceptions = 1
        self.PreviewKerningIcons = 1
        self.PreviewListWidth = 0x000000C8
        self.PreviewLockDependences = 1
        self.PreviewLockStyle = 0
        self.PreviewMode = 2
        self.PreviewPaintStyle = 0x00000100
        self.PreviewPanelTop = 1
        self.PreviewProcessFeatures = 0
        self.PreviewShowClassMembers = 1
        self.PreviewShowReferences = 1
        self.PreviewSize = 0x000000A0
        self.PreviewSnapStyle = 0x00000010
        self.QuickZoomScale = 0x00001D4C
        self.RemoveZeroKerning = 0
        self.Shift10 = 0x0000000A
        self.StyleInactiveMetrics = 2
        self.StyleMetrics = 1
        self.SyncronizeMasters = 1
        self.T1ExportCompatibleCyrillic = 0
        self.T1ExportEncoding = 0
        self.T1FSType = 0  # Export /FSType (font embedding) parameter
        self.T1MatchEncoding = 0  # Find matching encoding table if possible
        self.T1Sort = 0
        self.T1UseOTFamilyName = 0
        self.T1UseOTStyleName = 0
        self.T1UseTrademarkName = 0
        self.Template_BDF = ""
        self.Template_Path = ""
        self.Template_Use = 0
        self.TTEDecompose = 1  # Decompose all composites
        self.TTESmartFontName = 0  # Use the PostScript FontName as Full Name on Win?
        self.TTESmartMacNames = 1  # Use the OpenType names as menu names on Macintosh
        self.TTEStoreTables = 0  # Write stored custom TrueType/OpenType tables
        self.TTEVersionOS2 = 3  # OS/2 table version 3
        self.TTEVisual = 1  # Export visual TrueType hints
        self.TTEWriteKernTable = 0  # Export old-style non-OpenType "kern" table
        self.TTFScaler = 0x6D737363
        self.TTFSmooth = 0
        self.TTHPPM = 0x00000013
        self.TTIGenerateNames = 1
        self.TTIReadBinaryOT = 1  # Read OpenType layout tables (GPOS, GSUB, GDEF)
        self.TTIStoreBinaryOT = 1  # Store binary OpenType layout tables
        self.UnicodeKeyboard = 0
        self.UnicodeRangePercent = 0

    def Load(self) -> None:
        """
        Read FontLab Options from registry
        """
        self.Init()
        if self.fake_options_path.exists():
            self.fake_load_options()
        else:
            self.fake_save_options()

    def Save(self) -> None:
        """
        Save FontLab Options in registry
        """
        self.fake_save_options()
