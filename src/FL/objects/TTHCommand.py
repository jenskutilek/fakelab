from __future__ import annotations

from FL.helpers.tth import TT_COMMANDS, TT_COMMAND_CONSTANTS


class TTHCommand:
    """
    TTHCommand - class to represent visual TrueType instruction
    """

    __slots__ = ["_code", "_params"]

    # Constructor

    def __init__(self, code: int | None = None, *args: int) -> None:
        """
        Creates command, assigns command code and one or more parameters

        Args:
            code (int): The command code.
            *args (int): Zero or more parameters.

        See FL.helpers.tth.TT_COMMANDS for valid command codes and their matching
        parameters.
        """
        if code is None or len(args) >= 5:
            # More than 4 params will cause a RuntimeError, even though it should be
            # at > 5 according to the message
            raise RuntimeError(
                "Incorrect # of args to: "
                "TTHCommand(Int Code[,<up to 5 Int parameters>])"
            )

        if 1 <= code <= 23:
            self._code = code
            self._params = list(args)
            # Invalid codes will make FontLab 5 enter an infinite loop
            # Here, we just throw an exception
            if code not in TT_COMMANDS:
                raise ValueError(
                    "Codes 9, 10, 11, 12, 15, 16, 17, 18, 19 "
                    "will send FontLab into an infinite loop."
                )
        else:
            raise RuntimeError(
                "Incorrect instruction code. "
                "Value must be within the range from 1 to 23"
            )
        if len(args) == 0:
            # If there are too few args, the params are initialized with garbage ...
            self._params = [1632632832]

    def __repr__(self) -> str:
        cmd = TT_COMMANDS.get(self.code, {}).get("name", "NOTHING").upper()
        return f"<TTHCommand: {cmd}{tuple(self.params)}>"

    # Attributes

    @property
    def code(self) -> int:
        return self._code

    @code.setter
    def code(self, value: int) -> None:
        raise RuntimeError("class TTHCommand has no attribute code")

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
