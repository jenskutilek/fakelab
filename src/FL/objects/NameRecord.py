from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from FL.objects.Font import Font


class NameRecord:
    """
    NameRecord - class to represent OpenType name table record

    Unicode-encoding syntax ('/XX' - for Mac name records
                   and '/XXXX' - for Windows and Unicode name records)
    must be used to assign characters with codes above 127.
    Refer to OpenType specification for information about constants used
    for platform, encoding, language and name IDs
    for newline, Use /000D/000A in Win records and /0D in Mac records. (Description
    revised)
    """

    __slots__ = ["_parent", "_nid", "_pid", "_eid", "_lid", "_name"]

    # Constructor

    def __init__(
        self,
        name_record_or_s__or_tup_or_nid: (
            NameRecord | str | tuple[int, int, int, int, str] | int | None
        ) = None,
        pid: int | None = None,
        eid: int | None = None,
        lid: int | None = None,
        s: str | None = None,
    ) -> None:
        self._parent = None

    # Attributes

    @property
    def parent(self) -> Font | None:
        return self._parent

    @property
    def nid(self) -> int:
        """
        name identifier

        Returns:
            int: _description_
        """
        return self._nid

    @nid.setter
    def nid(self, value: int) -> None:
        self._nid = value

    @property
    def pid(self) -> int:
        """
        platform identifier

        Returns:
            int: _description_
        """
        return self._pid

    @pid.setter
    def pid(self, value: int) -> None:
        self._pid = value

    @property
    def eid(self) -> int:
        """
        encoding identifier

        Returns:
            int: _description_
        """
        return self._eid

    @eid.setter
    def eid(self, value: int) -> None:
        self._eid = value

    @property
    def lid(self) -> int:
        """
        language identifier

        Returns:
            int: _description_
        """
        return self._lid

    @lid.setter
    def lid(self, value: int) -> None:
        self._lid = value

    @property
    def name(self) -> str:
        """
        name value

        Returns:
            str: _description_
        """
        # FIXME: What encoding are we dealing with here?
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    # Operations: none

    # Methods: none
