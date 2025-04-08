from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from FL.objects.Font import Font


class TrueTypeTable:
    """
    TrueTypeTable - class to represent custom OpenType table
    """

    __slots__ = ["_parent", "_tag", "_value"]

    # Constructor

    def __init__(
        self,
        truetypetable_or_tag: TrueTypeTable | str | None = None,
        value: str | None = None,
        valuelen: int | None = None,
    ) -> None:
        """
        TrueTypeTable()              - generic constructor, creates an empty
                                       TrueTypeTable record
        TrueTypeTable(TrueTypeTable) - copy constructor
        TrueTypeTable(string tag)    - creates table, assigns 'tag' and empty value
        TrueTypeTable(string tag, string value)
                                     - creates TrueType table and assigns values to both
                                       attributes
        TrueTypeTable(string tag, string value, integer valuelen)
                                     - creates TrueType table and assigns values to both
                                       attributes.
        'value' may include zeroes

        Args:
            truetypetable_or_tag (TrueTypeTable | str | None, optional): _description_. Defaults to None.
            value (str | None, optional): _description_. Defaults to None.
            valuelen (int | None, optional): _description_. Defaults to None.
        """
        self._parent: Font | None = None
        self.tag = ""
        self.value = ""  # FIXME: str vs. bytes?
        if truetypetable_or_tag is not None:
            if isinstance(truetypetable_or_tag, TrueTypeTable):
                # copy constructor
                self.tag = truetypetable_or_tag.tag
                self.value = truetypetable_or_tag.value
            else:
                self.tag = truetypetable_or_tag
                if value is not None:
                    self.value = value
                    if valuelen is not None:
                        # FIXME: Just a hunch, take valuelen bytes from value
                        self.value = value[:valuelen]

    def __repr__(self) -> str:
        parent = self._parent or "orphan"
        return f"<TTTable: tag={self.tag}, {parent}>"

    # Attributes

    @property
    def parent(self) -> Font | None:
        return self._parent

    @property
    def tag(self) -> str:
        return self._tag

    @tag.setter
    def tag(self, value: str) -> None:
        self._tag = value

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value: str) -> None:
        self._value = value
