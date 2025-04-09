from __future__ import annotations

from typing import TYPE_CHECKING

from FL.fake.Base import Copyable

if TYPE_CHECKING:
    from FL.objects.TTGasp import TTGasp
    from FL.objects.TTStem import TTStem
    from FL.objects.TTVdmx import TTVdmx


class TTInfo(Copyable):
    """
    TTInfo - class to represent TrueType Information

    All information about TTInfo is based on an eMail from Yuri and was valid for
    FontLab 4.0
    """

    __slots__ = [
        "_hstem_data",
        "_vstem_data",
        "_prep",
        "_fpgm",
        "_cvt",
        "_gasp",
        "_hdmx",
        "_vdmx",
        "_max_zones",
        "_max_twilight_points",
        "_max_storage",
        "_max_function_defs",
        "_max_instruction_defs",
        "_max_stack_elements",
        "_head_creation",
        "_head_flags",
        "_head_font_direction_hint",
        "_head_lowest_rec_ppem",
        "_head_mac_style",
        "_head_units_per_em",
        "_hhea_ascender",
        "_hhea_descender",
        "_hhea_line_gap",
        "_os2_us_weight_class",
        "_os2_us_width_class",
        "_os2_fs_type",
        "_os2_y_subscript_x_size",
        "_os2_y_subscript_y_size",
        "_os2_y_subscript_x_offset",
        "_os2_y_subscript_y_offset",
        "_os2_y_superscript_x_size",
        "_os2_y_superscript_y_size",
        "_os2_y_superscript_x_offset",
        "_os2_y_superscript_y_offset",
        "_os2_y_strikeout_size",
        "_os2_y_strikeout_position",
        "_os2_s_family_class",
        "_os2_ul_code_page_range1",
        "_os2_ul_code_page_range2",
        "_os2_s_typo_ascender",
        "_os2_s_typo_descender",
        "_os2_s_typo_line_gap",
        "_os2_fs_selection",
        "_os2_us_win_ascent",
        "_os2_us_win_descent",
        # Non-API additions:
        "_stemsnaplimit",
        "_zoneppm",
        "_codeppm",
    ]

    # Constructor

    def __init__(self, ttinfo: TTInfo | None = None) -> None:
        """
        Never create TTInfo object explicitly - they must be obtained from the FontLab's
        `Font` classes.

        Args:
            ttinfo (TTInfo | None): Copy attributes from `TTInfo` or create an empty
                `TTInfo`
        """
        if ttinfo is None:
            self._set_defaults()
        else:
            self._copy_constructor(ttinfo)

    @property
    def hstem_data(self) -> list[TTStem]:
        """
        list of horizontal TrueType-Stems 'VExTTStemArray'

        Returns:
            list[TTStem]: _description_
        """
        return self._hstem_data

    @hstem_data.setter
    def hstem_data(self, value: list[TTStem]) -> None:
        self._hstem_data = value

    @property
    def vstem_data(self) -> list[TTStem]:
        """
        list of vertical TrueType-Stems 'VExTTStemArray'

        Returns:
            list[TTStem]: _description_
        """
        return self._vstem_data

    @vstem_data.setter
    def vstem_data(self, value: list[TTStem]) -> None:
        self._vstem_data = value

    @property
    def prep(self) -> list[int]:
        """
        CVT Program: list 'VSICharArray'

        Returns:
            list[int]: _description_
        """
        return self._prep

    @prep.setter
    def prep(self, value: list[int]) -> None:
        self._prep = value

    @property
    def fpgm(self) -> list[int]:
        """
        Font program: list 'VSICharArray'

        Returns:
            list[int]: _description_
        """
        return self._fpgm

    @fpgm.setter
    def fpgm(self, value: list[int]) -> None:
        self._fpgm = value

    @property
    def cvt(self) -> list[int]:
        """
        Control Value Table: list 'VSICharArray'

        Returns:
            list[int]: _description_
        """
        return self._cvt

    @cvt.setter
    def cvt(self, value: list[int]) -> None:
        self._cvt = value

    @property
    def gasp(self) -> list[TTGasp]:  # FL gives type as "VSArray"
        """
        Grid-fitting/Scan-conversion: list of smoothing control records 'VSITTGaspArray'

        Returns:
            list[TTGasp]: _description_
        """
        return self._gasp

    @gasp.setter
    def gasp(self, value: list[TTGasp]) -> None:
        self._gasp = value

    @property
    def hdmx(self) -> list[int]:
        """
        Horizontal device metrics: list 'VSBByteArray'

        Returns:
            list[int]: _description_
        """
        return self._hdmx

    @hdmx.setter
    def hdmx(self, value: list[int]) -> None:
        self._hdmx = value

    @property
    def vdmx(self) -> list[TTVdmx]:
        """
        Vertical device metrics: list 'VSITTVdmxArray'

        Returns:
            list[TTVdmx]: _description_
        """
        return self._vdmx

    @vdmx.setter
    def vdmx(self, value: list[TTVdmx]) -> None:
        self._vdmx = value

    @property
    def max_zones(self) -> int:
        return self._max_zones

    @max_zones.setter
    def max_zones(self, value: int) -> None:
        self._max_zones = value

    @property
    def max_twilight_points(self) -> int:
        return self._max_twilight_points

    @max_twilight_points.setter
    def max_twilight_points(self, value: int) -> None:
        self._max_twilight_points = value

    @property
    def max_storage(self) -> int:
        return self._max_storage

    @max_storage.setter
    def max_storage(self, value: int) -> None:
        self._max_storage = value

    @property
    def max_function_defs(self) -> int:
        return self._max_function_defs

    @max_function_defs.setter
    def max_function_defs(self, value: int) -> None:
        self._max_function_defs = value

    @property
    def max_instruction_defs(self) -> int:
        return self._max_instruction_defs

    @max_instruction_defs.setter
    def max_instruction_defs(self, value: int) -> None:
        self._max_instruction_defs = value

    @property
    def max_stack_elements(self) -> int:
        return self._max_stack_elements

    @max_stack_elements.setter
    def max_stack_elements(self, value: int) -> None:
        self._max_stack_elements = value

    @property
    def head_creation(self) -> list[int]:
        # [-467938523, 0]
        # Some kind of large int split into two?
        return self._head_creation

    @head_creation.setter
    def head_creation(self, value: list[int]) -> None:
        self._head_creation = value

    @property
    def head_flags(self) -> int:
        return self._head_flags

    @head_flags.setter
    def head_flags(self, value: int) -> None:
        self._head_flags = value

    @property
    def head_font_direction_hint(self) -> int:
        return self._head_font_direction_hint

    @head_font_direction_hint.setter
    def head_font_direction_hint(self, value: int) -> None:
        self._head_font_direction_hint = value

    @property
    def head_lowest_rec_ppem(self) -> int:
        return self._head_lowest_rec_ppem

    @head_lowest_rec_ppem.setter
    def head_lowest_rec_ppem(self, value: int) -> None:
        self._head_lowest_rec_ppem = value

    @property
    def head_mac_style(self) -> int:
        return self._head_mac_style

    @head_mac_style.setter
    def head_mac_style(self, value: int) -> None:
        self._head_mac_style = value

    @property
    def head_units_per_em(self) -> int:
        return self._head_units_per_em

    @head_units_per_em.setter
    def head_units_per_em(self, value: int) -> None:
        self._head_units_per_em = value

    @property
    def hhea_ascender(self) -> int:
        return self._hhea_ascender

    @hhea_ascender.setter
    def hhea_ascender(self, value: int) -> None:
        self._hhea_ascender = value

    @property
    def hhea_descender(self) -> int:
        return self._hhea_descender

    @hhea_descender.setter
    def hhea_descender(self, value: int) -> None:
        self._hhea_descender = value

    @property
    def hhea_line_gap(self) -> int:
        return self._hhea_line_gap

    @hhea_line_gap.setter
    def hhea_line_gap(self, value: int) -> None:
        self._hhea_line_gap = value

    @property
    def os2_us_weight_class(self) -> int:
        return self._os2_us_weight_class

    @os2_us_weight_class.setter
    def os2_us_weight_class(self, value: int) -> None:
        self._os2_us_weight_class = value

    @property
    def os2_us_width_class(self) -> int:
        return self._os2_us_width_class

    @os2_us_width_class.setter
    def os2_us_width_class(self, value: int) -> None:
        self._os2_us_width_class = value

    @property
    def os2_fs_type(self) -> int:
        return self._os2_fs_type

    @os2_fs_type.setter
    def os2_fs_type(self, value: int) -> None:
        self._os2_fs_type = value

    @property
    def os2_y_subscript_x_size(self) -> int:
        return self._os2_y_subscript_x_size

    @os2_y_subscript_x_size.setter
    def os2_y_subscript_x_size(self, value: int) -> None:
        self._os2_y_subscript_x_size = value

    @property
    def os2_y_subscript_y_size(self) -> int:
        return self._os2_y_subscript_y_size

    @os2_y_subscript_y_size.setter
    def os2_y_subscript_y_size(self, value: int) -> None:
        self._os2_y_subscript_y_size = value

    @property
    def os2_y_subscript_x_offset(self) -> int:
        return self._os2_y_subscript_x_offset

    @os2_y_subscript_x_offset.setter
    def os2_y_subscript_x_offset(self, value: int) -> None:
        self._os2_y_subscript_x_offset = value

    @property
    def os2_y_subscript_y_offset(self) -> int:
        return self._os2_y_subscript_y_offset

    @os2_y_subscript_y_offset.setter
    def os2_y_subscript_y_offset(self, value: int) -> None:
        self._os2_y_subscript_y_offset = value

    @property
    def os2_y_superscript_x_size(self) -> int:
        return self._os2_y_superscript_x_size

    @os2_y_superscript_x_size.setter
    def os2_y_superscript_x_size(self, value: int) -> None:
        self._os2_y_superscript_x_size = value

    @property
    def os2_y_superscript_y_size(self) -> int:
        return self._os2_y_superscript_y_size

    @os2_y_superscript_y_size.setter
    def os2_y_superscript_y_size(self, value: int) -> None:
        self._os2_y_superscript_y_size = value

    @property
    def os2_y_superscript_x_offset(self) -> int:
        return self._os2_y_superscript_x_offset

    @os2_y_superscript_x_offset.setter
    def os2_y_superscript_x_offset(self, value: int) -> None:
        self._os2_y_superscript_x_offset = value

    @property
    def os2_y_superscript_y_offset(self) -> int:
        return self._os2_y_superscript_y_offset

    @os2_y_superscript_y_offset.setter
    def os2_y_superscript_y_offset(self, value: int) -> None:
        self._os2_y_superscript_y_offset = value

    @property
    def os2_y_strikeout_size(self) -> int:
        return self._os2_y_strikeout_size

    @os2_y_strikeout_size.setter
    def os2_y_strikeout_size(self, value: int) -> None:
        self._os2_y_strikeout_size = value

    @property
    def os2_y_strikeout_position(self) -> int:
        return self._os2_y_strikeout_position

    @os2_y_strikeout_position.setter
    def os2_y_strikeout_position(self, value: int) -> None:
        self._os2_y_strikeout_position = value

    @property
    def os2_s_family_class(self) -> int:
        return self._os2_s_family_class

    @os2_s_family_class.setter
    def os2_s_family_class(self, value: int) -> None:
        self._os2_s_family_class = value

    @property
    def os2_ul_code_page_range1(self) -> int:
        return self._os2_ul_code_page_range1

    @os2_ul_code_page_range1.setter
    def os2_ul_code_page_range1(self, value: int) -> None:
        self._os2_ul_code_page_range1 = value

    @property
    def os2_ul_code_page_range2(self) -> int:
        return self._os2_ul_code_page_range2

    @os2_ul_code_page_range2.setter
    def os2_ul_code_page_range2(self, value: int) -> None:
        self._os2_ul_code_page_range2 = value

    @property
    def os2_s_typo_ascender(self) -> int:
        return self._os2_s_typo_ascender

    @os2_s_typo_ascender.setter
    def os2_s_typo_ascender(self, value: int) -> None:
        self._os2_s_typo_ascender = value

    @property
    def os2_s_typo_descender(self) -> int:
        return self._os2_s_typo_descender

    @os2_s_typo_descender.setter
    def os2_s_typo_descender(self, value: int) -> None:
        self._os2_s_typo_descender = value

    @property
    def os2_s_typo_line_gap(self) -> int:
        return self._os2_s_typo_line_gap

    @os2_s_typo_line_gap.setter
    def os2_s_typo_line_gap(self, value: int) -> None:
        self._os2_s_typo_line_gap = value

    @property
    def os2_fs_selection(self) -> int:
        return self._os2_fs_selection

    @os2_fs_selection.setter
    def os2_fs_selection(self, value: int) -> None:
        self._os2_fs_selection = value

    @property
    def os2_us_win_ascent(self) -> int:
        return self._os2_us_win_ascent

    @os2_us_win_ascent.setter
    def os2_us_win_ascent(self, value: int) -> None:
        self._os2_us_win_ascent = value

    @property
    def os2_us_win_descent(self) -> int:
        return self._os2_us_win_descent

    @os2_us_win_descent.setter
    def os2_us_win_descent(self, value: int) -> None:
        self._os2_us_win_descent = value

    # Internal

    def _set_defaults(self) -> None:
        # Defaults for an empty TTInfo
        self.hstem_data = []
        self.vstem_data = []
        self.prep = []
        self.fpgm = []
        self.cvt = []
        self.gasp = []
        self.vdmx = []
        self.max_zones = 0
        self.max_twilight_points = 0
        self.max_storage = 0
        self.max_function_defs = 0
        self.max_instruction_defs = 0
        self.max_stack_elements = 0
        self.head_creation = [-467938523, 0]
        self.head_flags = 131072
        self.head_font_direction_hint = 2
        self.head_lowest_rec_ppem = 9
        self.head_mac_style = 0
        self.head_units_per_em = 2048
        self.hhea_ascender = 1536
        self.hhea_descender = -512
        self.hhea_line_gap = 18
        self.os2_us_weight_class = 400
        self.os2_us_width_class = 5
        self.os2_fs_type = 4
        self.os2_y_subscript_x_size = 1433
        self.os2_y_subscript_y_size = 1331
        self.os2_y_subscript_x_offset = 0
        self.os2_y_subscript_y_offset = 286
        self.os2_y_superscript_x_size = 1433
        self.os2_y_superscript_y_size = 1331
        self.os2_y_superscript_x_offset = 0
        self.os2_y_superscript_y_offset = 976
        self.os2_y_strikeout_size = 102
        self.os2_y_strikeout_position = 512
        self.os2_s_family_class = 0
        self.os2_ul_code_page_range1 = 0
        self.os2_ul_code_page_range2 = 0
        self.os2_s_typo_ascender = 1536
        self.os2_s_typo_descender = -512
        self.os2_s_typo_line_gap = 0
        self.os2_fs_selection = 0
        self.os2_us_win_ascent = 0
        self.os2_us_win_descent = 0

        # Not in API:
        self._stemsnaplimit: int = 68  # 68/64 pixel
        self._zoneppm: int = 48  # Zones active until ppm
        self._codeppm: int = 0  # Gridfitting active until ppm (0 = no limit)
