from __future__ import annotations


class EncodingRecord:
    def __init__(self, encoding_record_or_none: EncodingRecord | None = None) -> None:
        """
        EncodingRecord - class to represent EncodingRecord

        EncodingRecord()
            generic constructor, creates empty EncodingRecord
        EncodingRecord(EncodingRecord)
            copy constructor
        """
        self.name: str | None = None
        self.unicode: int = -1
        if isinstance(encoding_record_or_none, EncodingRecord):
            # Copy constructor
            self.name = encoding_record_or_none.name
            self.unicode = encoding_record_or_none.unicode

    def __repr__(self) -> str:
        return f'<EncodingRecord: "{self.name}", unicode: {self.unicode}>'
