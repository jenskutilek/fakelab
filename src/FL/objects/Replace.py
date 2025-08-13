from __future__ import annotations

from typing import TYPE_CHECKING

from FL.fake.Base import Copyable
from FL.objects.Hint import Hint
from FL.objects.Node import Node

if TYPE_CHECKING:
    from FL.objects.Glyph import Glyph


TYPE_HORIZONTAL_HINT = 1
TYPE_VERTICAL_HINT = 2
TYPE_NODE = 255


__doc__ = "Class to represent an item of a hint replacment program"


class Replace(Copyable):
    """
    Replace - class to represent item of hint replacment program

    Replace.__doc__ reports only 'Replace' ... so use this information with care

    To use attribute object, Replase must have valid parent
    To assign a `Node`, Node must not be an orphan
    To assign a `Hint`, Hint must not be an orphan
    """

    """
    Example:
    for r in fl.glyph.replace_table:
        print r
    <Replace: HorizontalHint number 2, parent: "a">
    <Replace: VerticalHint number 0, parent: "a">
    <Replace: HorizontalHint number 0, parent: "a">
    <Replace: HintReplace at node 6, parent: "a">
    <Replace: HorizontalHint number 1, parent: "a">
    <Replace: VerticalHint number 0, parent: "a">
    <Replace: HorizontalHint number 2, parent: "a">
    """

    # Constructor

    def __init__(
        self,
        replace_or_hint_or_node_or_type: Replace | Hint | Node | int | None = None,
        index: int | None = None,
    ) -> None:
        """
        Replace()             - generic constructor, creates an empty replace item
        Replace(Replace)      - copy constructor
        Replace(Hint)
        Replace(Node)
        Replace(Int type,Int index)

        Args:
            replace_or_hint_or_node_or_type (Replace | Hint | Node | int | None, optional): _description_. Defaults to None.
            index (int | None, optional): _description_. Defaults to None.
        """
        self._parent: Glyph | None = None
        self._type = 0
        self._index = 0
        arg1 = replace_or_hint_or_node_or_type
        if arg1 is not None:
            if isinstance(arg1, Replace):
                self._copy_constructor(arg1)
            elif isinstance(arg1, Hint):
                # FIXME: How to determine if a hint is horizontal or vertical?
                self._type = TYPE_HORIZONTAL_HINT  # or TYPE_VERTICAL_HINT
            elif isinstance(arg1, Node):
                self._type = TYPE_NODE
            elif isinstance(arg1, int):
                self.type = arg1
                if isinstance(index, int):
                    self.index = index
            else:
                raise TypeError

    def __repr__(self) -> str:
        tp = {
            1: "HorizontalHint",
            2: "VerticalHint",
            # 255: "HintReplace",
        }

        parent = "orphan" if self.parent is None else f'parent: "{self.parent.name}"'

        if self.type == TYPE_NODE:
            return f"<Replace: HintReplace at node {self.index}, {parent}>"
        elif self.type in (TYPE_HORIZONTAL_HINT, TYPE_VERTICAL_HINT):
            return f"<Replace: {tp.get(self.type)} number {self.index}, {parent}>"
        else:
            return f"<Replace: Unknown replace type, index= {self.index}, {parent}>"

    @property
    def parent(self) -> Glyph | None:
        """
        Replace's parent object, `Glyph`

        Returns:
            Glyph | None: _description_
        """
        return self._parent

    @property
    def type(self) -> int:
        return self._type

    @type.setter
    def type(self, value: int) -> None:
        self._type = value

    @property
    def index(self) -> int:
        return self._index

    @index.setter
    def index(self, value: int) -> None:
        self._index = value

    # Operations: unknown

    # Methods: unknown
