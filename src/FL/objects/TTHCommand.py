from __future__ import annotations


class TTHCommand:

    # Constructor

    def __init__(self, code: int, params: list[int]) -> None:
        self.code = code
        self._params = params

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

    # Operations: none

    # Methods: none
