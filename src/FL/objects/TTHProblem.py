from __future__ import annotations


class TTHProblem:
    """
    TTHProblem - class to represent TrueType problems
    """

    __slots__ = ["_id", "_command", "_direction"]

    # Constructor

    def __init__(self, _called_from_FL: bool = False) -> None:
        """
        Class `TTHProblem` is auxiliary and cannot be created explicitly
        """
        # Those values have not been checked against FL
        self._id = 0
        self._command = 0
        self._direction = 0
        if not _called_from_FL:
            raise RuntimeError(
                "Class TTHProblem is auxiliary and cannot be created explicitly"
            )

    def __repr__(self) -> str:
        return f"<TTHProblem: Id: {self.id}, Command: {self.command}, Direction: {self.direction}>"

    # Additions for FakeLab

    @staticmethod
    def fake_create() -> TTHProblem:
        p = TTHProblem.__new__(TTHProblem)
        return p

    # Attributes

    @property
    def id(self) -> int:
        return self._id

    @property
    def command(self) -> int:
        return self._command

    @property
    def direction(self) -> int:
        return self._direction
