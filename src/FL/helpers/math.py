from __future__ import annotations


def int32_to_unsigned(i: int) -> int:
    """
    Reinterpret a signed integer as unsigned
    """
    return int.from_bytes(
        i.to_bytes(4, signed=True, byteorder="big"), signed=False, byteorder="big"
    )


def uint32_to_signed(i: int) -> int:
    """
    Reinterpret an unsigned integer as signed
    """
    return int.from_bytes(
        i.to_bytes(4, signed=False, byteorder="big"), signed=True, byteorder="big"
    )
