from __future__ import annotations

from FL.helpers.tth import TT_COMMANDS, TT_COMMAND_CONSTANTS


class TTHCommand:
    """
    TTHCommand - class to represent visual TrueType instruction
    """

    __slots__ = ["_code", "_params"]

    # Constructor

    def __init__(self, code: int, *args: int) -> None:
        """
        Creates command, assigns command code and one or more parameters

        Args:
            code (int): The command code.
            *args (int): Zero or more parameters.

        See FL.helpers.tth.TT_COMMANDS for valid command codes and their matching
        parameters.
        """
        if 1 <= code <= 23:
            self.code = code
            self._params = list(args)
        else:
            raise RuntimeError(
                "Incorrect instruction code. "
                "Value must be within the range from 1 to 23"
            )
        if len(args) > 5:
            raise RuntimeError(
                "Incorrect # of args to: "
                "TTHCommand(Int Code[,<up to 5 Int parameters>])"
            )
        if len(args) == 0:
            # If there are too few args, the params are initialized with garbage ...
            self._params = [1632632832]

    def __repr__(self) -> str:
        cmd = TT_COMMANDS.get(self.code, {}).get("name", "UNKNOWN").upper()
        return f"<TTHCommand: {cmd}{self.params}>"

    # Attributes

    @property
    def code(self) -> int:
        return self._code

    @code.setter
    def code(self, value: int) -> None:
        self._code = value

    @property
    def params(self) -> list[int]:
        return self._params

    @params.setter
    def params(self, value: list[int]) -> None:
        raise RuntimeError(
            'Attempt to write read only attribute "params" of class TTHCommand'
        )

    # Operations: none

    # Methods: none


"""
FINALDELTAV 23
FINALDELTAH 22
MIDDLEDELTAV 21
MIDDLEDELTAH 20 
RINGINTERPOLATEV (19)
RINGINTERPOLATEH (18)
RINGLINKV (17)
RINGLINKH (16)
POINTTORINGXY (15)
INTERPOLATEV 14
INTERPOLATEH 13
RINGTOGRIDV (12)
RINGTOGRIDH (11)
POINTTORINGV (10)
POINTTORINGH (9)
ALIGNV 8
ALIGNH 7
DOUBLELINKV 6
DOUBLELINKH 5
SINGLELINKV 4
SINGLELINKH 3
ALIGNBOTTOM 2
ALIGNTOP 1
NOTHING
Incorrect instruction code. Value must be within the range from 1 to 23

Incorrect # of args to: TTHCommand(Int Code[,<up to 5 Int parameters>])

TTHCommand

)>

class TTHCommand has no attribute %s
"""
