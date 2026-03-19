from typing import TYPE_CHECKING

from FL.constants import DIR_UNDEFINED
from FL.fake.Base import Copyable

if TYPE_CHECKING:
    from FL.objects.Glyph import Glyph


__doc__ = "Class to represent a link"


class Link(Copyable):
    """
    Link - class to represent link
    """

    __slots__ = ["_node1", "_node2", "_parent", "_stem_direction"]

    # Constructor

    def __init__(
        self, link_or_index1: "Link | int | None" = None, index2: int | None = None
    ) -> None:
        self.fake_set_defaults()

        # Process params

        if isinstance(link_or_index1, Link):
            self._copy_constructor(link_or_index1)

        elif isinstance(link_or_index1, int):
            self._node1 = link_or_index1

            if index2 is not None:
                self._node2 = index2

    # Defaults

    def fake_set_defaults(self) -> None:
        self._parent = None
        self._node1 = -1
        self._node2 = -1
        self._stem_direction = DIR_UNDEFINED

    def _copy_constructor(self, other: "Link") -> None:
        self.node1 = other.node1
        self.node2 = other.node2
        self._stem_direction = other._stem_direction

    def __repr__(self) -> str:
        p = self._parent or "orphan"
        return f"<Link: node1={self.node1}, node2={self.node2}, {p}>"

    # Attributes

    @property
    def parent(self) -> "Glyph | None":
        """
        Link's parent object, Glyph
        """
        return self._parent

    @property
    def node1(self) -> int:
        """
        indexes of the nodes that are linked: node1
        """
        return self._node1

    @node1.setter
    def node1(self, value: int) -> None:
        self._node1 = value

    @property
    def node2(self) -> int:
        """
        indexes of the nodes that are linked: node2
        """
        return self._node2

    @node2.setter
    def node2(self, value: int) -> None:
        self._node2 = value

    # Methods

    def ToHint(self) -> None:
        """
        Transforms link to Hint (and returns it as a result **wrong**) using parent as
        a source of node coordinates. Parent must exist
        """
        # This does *not* return the hint, but seems to append it to the
        # glyph's hhints or vhints property. It also deletes itself from the links attr.
        return None
