from __future__ import annotations

from typing import TYPE_CHECKING

from vfbLib.truetype import TT_COMMAND_CONSTANTS, TT_COMMANDS

from FL.helpers.FLList import FLList
from FL.objects.Point import Point
from FL.objects.TTHCommand import TTHCommand

if TYPE_CHECKING:
    from FL.objects.Font import Font
    from FL.objects.Glyph import Glyph
    from FL.objects.Hint import Hint
    from FL.objects.TTHPoint import TTHPoint
    from FL.objects.TTHProblem import TTHProblem


__doc__ = "Class to represent a TrueType program"


class TTH:
    """
    TTH - class to represent a TrueType program
    """

    __slots__ = [
        "_font",
        "_glyph",
        "_top_zones",
        "_bottom_zones",
        "_base_top_zones",
        "_base_bottom_zones",
        "_hstems",
        "_vstems",
        "_base_hstems",
        "_base_vstems",
        "_zero_point",
        "_upm",
        "_ppm",
        "_outline",
        "_base_outline",
        "_commands",
        "_problems",
    ]

    # Constructor

    def __init__(self, g: Glyph | None = None, f: Font | None = None) -> None:
        """
        TTH()
            generic constructor, creates an empty TTH
        TTH(Glyph g)
            creates TTH, assigns 'g' as glyph and 'parent' of 'g' as font
        TTH(Glyph g, Font f)
            creates TTH, assigns 'g' as glyph and 'f' as font

        Args:
            g (Glyph | None, optional): _description_. Defaults to None.
            f (Font | None, optional): _description_. Defaults to None.
        """
        self.glyph = None
        self.font = None

        if g is not None:
            self.glyph = g
            if f is None:
                self.font = g.parent
            else:
                self.font = f

        self._top_zones: list[Hint] = FLList()
        self._bottom_zones: list[Hint] = FLList()
        self._base_top_zones: list[Hint] = FLList()
        self._base_bottom_zones: list[Hint] = FLList()
        self._hstems: list[int] = FLList()
        self._vstems: list[int] = FLList()
        self._base_hstems: list[int] = FLList()
        self._base_vstems: list[int] = FLList()
        self.zero_point = Point(0, 0)
        # self.zero_point._parent = self  # Needed?
        self.upm = 1000
        self.ppm = 0  # FL returns a random number
        self._outline: list[TTHPoint] = FLList()
        self._base_outline: list[TTHPoint] = FLList()
        self._commands: list[TTHCommand] = FLList()
        self._problems: list[TTHProblem] = FLList()

    def _raise(self, attr: str) -> None:
        raise RuntimeError(
            f'attempt to write to read-only attribute "{attr}" of class TTH'
        )

    def __repr__(self) -> str:
        return f"<TTH: Glyph: {self.glyph}, Font: {self.font}>"

    # Attributes

    @property
    def font(self) -> Font | None:
        return self._font

    @font.setter
    def font(self, value: Font | None) -> None:
        self._font = value

    @property
    def glyph(self) -> Glyph | None:
        return self._glyph

    @glyph.setter
    def glyph(self, value: Glyph | None) -> None:
        self._glyph = value

    @property
    def top_zones(self) -> list[Hint]:
        return self._top_zones

    @top_zones.setter
    def top_zones(self, value: list[Hint]) -> None:
        self._raise("top_zones")

    @property
    def bottom_zones(self) -> list[Hint]:
        return self._bottom_zones

    @bottom_zones.setter
    def bottom_zones(self, value: list[Hint]) -> None:
        self._raise("bottom_zones")

    @property
    def base_top_zones(self) -> list[Hint]:
        return self._base_top_zones

    @base_top_zones.setter
    def base_top_zones(self, value: list[Hint]) -> None:
        self._raise("base_top_zones")

    @property
    def base_bottom_zones(self) -> list[Hint]:
        return self._base_bottom_zones

    @base_bottom_zones.setter
    def base_bottom_zones(self, value: list[Hint]) -> None:
        self._raise("base_bottom_zones")

    @property
    def hstems(self) -> list[int]:
        return self._hstems

    @hstems.setter
    def hstems(self, value: list[int]) -> None:
        # TODO: Must set FLList()?
        self._hstems = value

    @property
    def vstems(self) -> list[int]:
        return self._vstems

    @vstems.setter
    def vstems(self, value: list[int]) -> None:
        # TODO: Must set FLList()?
        self._vstems = value

    @property
    def base_hstems(self) -> list[int]:
        return self._base_hstems

    @base_hstems.setter
    def base_hstems(self, value: list[int]) -> None:
        # TODO: Must set FLList()?
        self._base_hstems = value

    @property
    def base_vstems(self) -> list[int]:
        return self._base_vstems

    @base_vstems.setter
    def base_vstems(self, value: list[int]) -> None:
        # TODO: Must set FLList()?
        self._base_vstems = value

    @property
    def zero_point(self) -> Point:
        return self._zero_point

    @zero_point.setter
    def zero_point(self, value: Point) -> None:
        self._zero_point = value

    @property
    def upm(self) -> int:
        return self._upm

    @upm.setter
    def upm(self, value: int) -> None:
        self._upm = value

    @property
    def ppm(self) -> int:
        return self._ppm

    @ppm.setter
    def ppm(self, value: int) -> None:
        self._ppm = value

    @property
    def outline(self) -> list[TTHPoint]:
        return self._outline

    @outline.setter
    def outline(self, value: list[TTHPoint]) -> None:
        raise RuntimeError("class TTH has no attribute outline")

    @property
    def base_outline(self) -> list[TTHPoint]:
        return self._base_outline

    @base_outline.setter
    def base_outline(self, value: list[TTHPoint]) -> None:
        raise RuntimeError("class TTH has no attribute base_outline")

    @property
    def commands(self) -> list[TTHCommand]:
        return self._commands

    @commands.setter
    def commands(self, value: list[TTHCommand]) -> None:
        self._raise("commands")

    @property
    def problems(self) -> list[TTHProblem]:
        return self._problems

    @problems.setter
    def problems(self, value: list[TTHProblem]) -> None:
        self._raise("problems")

    # Operations

    def __len__(self) -> int:
        """
        returns number of commands
        """
        return len(self.commands)

    def __getitem__(self, index: int) -> TTHCommand:
        """
        accesses TTCommand list
        """
        return self.commands[index]

    # Methods

    def Init(self, g_or_f: Glyph | Font, f: Font | None = None) -> None:
        raise NotImplementedError

    def Initoutline(self) -> None:
        raise NotImplementedError

    def SetPPM(self, ppm: int) -> None:
        self.ppm = ppm

    def ResetProgram(self, direction: int | None = None) -> None:
        raise NotImplementedError

    def LoadProgram(self, g: Glyph | None = None) -> None:
        # Initialize TTH object with Glyph first or specify it explicitly
        if g is None:
            if self.glyph is None:
                raise ValueError(
                    "TTH.LoadProgram without glyph argument will send FontLab into an "
                    "infinite loop (if the TTH was not initialized with a Glyph)."
                )
            g = self.glyph

        # TODO: Does calling this with a glyph replace the current glyph?

        self.commands.clear()
        for i in g._tth:
            cmd = i["cmd"]
            cmd_int = TT_COMMAND_CONSTANTS[cmd]
            params = [i["params"][param] for param in TT_COMMANDS[cmd_int]["params"]]
            tthcmd = TTHCommand(cmd_int, *params)
            self.commands.append(tthcmd)

    def SaveProgram(self, g: Glyph | None = None) -> None:
        if g is None:
            if self.glyph is None:
                raise ValueError(
                    "TTH.LoadProgram without glyph argument will send FontLab into an "
                    "infinite loop (if the TTH was not initialized with a Glyph)."
                )
            g = self.glyph

        # TODO: Does calling this with a glyph replace the current glyph?

        raise NotImplementedError

    def SortProgram(self) -> None:
        raise NotImplementedError

    def RunProgram(self, i: int | None = None, j: int | None = None) -> None:
        raise NotImplementedError

    def RunCommand(self, tthcommand: TTHCommand) -> None:
        raise NotImplementedError

    def TestProgram(self) -> int:
        # Returns some kind of error code? 1 for an empty program e.g.
        raise NotImplementedError

    def BuildFromLinks(self, g: Glyph | None = None) -> None:
        if g is None:
            raise ValueError(
                "TTH.LoadProgram without glyph argument will send FontLab into an "
                "infinite loop (if the TTH was not initialized with a Glyph)."
            )
        raise NotImplementedError

    def ResetFinalDeltas(self, direction: int | None = None) -> None:
        raise NotImplementedError

    def ResetAllDeltas(self, direction: int | None = None) -> None:
        raise NotImplementedError

    def LoadFromTextFile(self, filename: str) -> int:
        """
        Load TTH from a text file.

        Args:
            filename (str): The path and filename of the text file.

        Returns:
            int: 0 on success, -1 on error.
        """
        raise NotImplementedError

    def SaveToTextFile(self, filename: str) -> None:
        """
        Save the TTH to a text file at path `filename`.

        Args:
            filename (str): The path and filename of the text file.

        Example file:

        .. code-block:: text

           34 POINTS
           439 412 17
           421 419 2
           382 427 2
           363 427 1
           318 427 2
           255 384 2
           220 322 2
           205 254 2
           205 225 1
           205 181 2
           248 135 2
           296 135 1
           320 135 2
           364 144 2
           388 152 1
           385 11 1
           354 2 2
           282 -7 2
           250 -7 1
           185 -7 2
           97 30 2
           51 90 2
           33 158 2
           33 194 1
           33 259 2
           73 390 2
           154 500 2
           287 569 2
           374 569 1
           405 569 2
           459 562 2
           482 554 1
           0 -17 17
           441 -17 17

           5 BOTTOMZONES
           344 10
           0 15
           -83 15
           -171 15
           -233 15

           10 TOPZONES
           815 8
           792 10
           730 15
           705 15
           675 15
           650 15
           600 15
           520 15
           497 15
           470 15

           19 HSTEMS
           140
           152
           158
           171
           220
           116
           85
           97
           109
           123
           130
           164
           145
           180
           200
           22222
           44444
           100
           44

           25 VSTEMS
           182
           195
           220
           152
           208
           91
           128
           139
           66
           100
           110
           117
           127
           135
           144
           148
           169
           179
           189
           200
           215
           225
           22222
           55555
           54

           0 PROGRAM
        """
        raise NotImplementedError
