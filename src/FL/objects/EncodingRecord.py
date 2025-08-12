from __future__ import annotations

from FL.fake.Base import Copyable


class EncodingRecord(Copyable):
    __slots__ = ["_name", "_unicode"]

    # Constructor

    def __init__(self, encoding_record: EncodingRecord | None = None) -> None:
        """
        EncodingRecord - class to represent EncodingRecord

        EncodingRecord()
            generic constructor, creates empty EncodingRecord
        EncodingRecord(EncodingRecord)
            copy constructor

        Args:
            encoding_record (EncodingRecord | None, optional): _description_. Defaults to None.
        """
        self.name = "(null)"
        self.unicode = 0
        if isinstance(encoding_record, EncodingRecord):
            self._copy_constructor(encoding_record)

    def __repr__(self) -> str:
        return f'<EncodingRecord: "{self.name}", unicode: {self.unicode}>'

    # Attributes

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def unicode(self) -> int:
        return self._unicode

    @unicode.setter
    def unicode(self, value: int) -> None:
        self._unicode = value

    # Operations

    # EncodingRecord has no operations

    # Methods

    # EncodingRecord has no methods
