from __future__ import annotations


class Uni:
    """
    Uni - class to represent Unicode index

    This class is necessary to distinguish integers and Unicode indexes. Integers are
    usually read as glyph indexes, so it is necessary to create Uni objects to access
    glyph by Unicode index

    Please note that this is not the same that is implemented in Python 2.x
    """

    __slots__ = ["_value"]

    # Constructor

    def __init__(self, uni_or_int_or_hex: Uni | int | str | None = None) -> None:
        """
        Uni() - generic constructor, creates an empty Uni record (bullshit)
        Uni(Uni) - copy constructor
        Uni(uni: int) - creates Uni object and assigns integer value
        Uni(uni_hex: string) - creates Uni object and reads value from the string in hex form
        """
        if uni_or_int_or_hex is None:
            # The error message is bullshit, but here we are:
            raise RuntimeError(
                "Incorrect # of args to: \n Uni()\n Uni(float x,float y)\n Uni(Uni P)"
            )
        if isinstance(uni_or_int_or_hex, Uni):
            # copy constructor
            self.value = uni_or_int_or_hex.value
        elif isinstance(uni_or_int_or_hex, str):
            self.value = int(uni_or_int_or_hex, base=16)
        elif isinstance(uni_or_int_or_hex, int):
            self.value = uni_or_int_or_hex

    def __repr__(self) -> str:
        return f"uni{self.value:04x}"

    # Attributes

    @property
    def value(self) -> int:
        """Unicode index"""
        return self._value

    @value.setter
    def value(self, value: int) -> None:
        self._value = value

    # Operations

    def __eq__(self, other: object) -> bool:
        """
        Compares two Unicode indexes in Uni or integer form

        Args:
            other (Uni | int): The object or integer to compare to.

        Returns:
            bool: Whether both objects represent the same Unicode index.
        """
        if isinstance(other, Uni):
            return self.value == other.value

        if isinstance(other, int):
            return self.value == other

        return False

    # Methods: none
