from __future__ import annotations

from typing import TYPE_CHECKING

from FL.objects.Point import Point

if TYPE_CHECKING:
    from FL.objects.Glyph import Glyph


class AuditRecord:
    """
    ===============================================
    AuditRecord - class to represent Font Audit error record
    ===============================================

    Note that objects of this class cannot be created explicitly, they are only
    generated as a result of Glyph().Audit() operation
    """

    __slots__ = ["_parent", "_x", "_y", "_id", "_description", "_index"]

    def __init__(self, parent: Glyph) -> None:
        """
        Don't call this yourself

        Args:
            parent (Glyph): The parent of the AuditRecord, a `Glyph`
        """
        self._parent = parent
        self._x = 0
        self._y = 0
        self._id = ""
        self._description = ""
        self._index = -1

    # Attributes

    @property
    def parent(self) -> Glyph:
        """
        Parent object, Glyph

        Returns:
            Glyph: The parent glyph
        """
        return self._parent

    @property
    def position(self) -> Point:
        """
        Position of the audit mark as a Point object

        Returns:
            Point: The point
        """
        return Point(self._x, self._y)

    @property
    def p(self) -> Point:
        """
        Position of the audit mark as a Point object

        Returns:
            Point: The point
        """
        return Point(self._x, self._y)

    @property
    def id(self) -> str:
        """
        Name of the error

        Returns:
            str: The name
        """
        return self._id

    @property
    def description(self) -> str:
        """
        Description of the error

        Returns:
            str: The description
        """
        return self._description

    @property
    def index(self) -> int:
        """
        Node index in the glyph to which error is attched

        Returns:
            int: The node index
        """
        return self._index

    # Methods

    def CanBeFixed(self) -> bool:
        """
        Returns:
            bool: True if this error can be automatically fixed
        """
        raise NotImplementedError

    def Repair(self) -> None:
        """
        Tries to automatically fix error
        """
        raise NotImplementedError
