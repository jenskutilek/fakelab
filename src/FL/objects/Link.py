from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from FL.objects.Glyph import Glyph


class Link:
    """
    Link - class to represent link
    """

    __slots__ = ["_node1", "_node2", "_parent"]

    # Constructor

    def __init__(
        self, link_or_index1: Link | int | None = None, index2: int | None = None
    ) -> None:
        self.set_defaults()

        # Process params

        if isinstance(link_or_index1, Link):
            # Copy constructor
            raise NotImplementedError

        elif isinstance(link_or_index1, int):
            self._node1 = link_or_index1

            if index2 is not None:
                self._node2 = index2

    def __repr__(self) -> str:
        p = self._parent or "orphan"
        return f"<Link: node1={self.node1}, node2={self.node2}, {p}>"

    # Attributes

    @property
    def parent(self) -> Glyph | None:
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
        # glyph's hhints or vhints property
        return None

    # Defaults

    def set_defaults(self):
        self._parent = None
        self._node1 = None
        self._node2 = None
