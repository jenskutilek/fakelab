from __future__ import annotations

from typing import TYPE_CHECKING

from FL.objects.Point import Point

if TYPE_CHECKING:
    from FL.objects.Glyph import Glyph


class AuditRecord:
    """
    AuditRecord - class to represent Font Audit error record
    """

    __slots__ = ["_parent", "_x", "_y", "_id", "_description", "_index"]

    # Constructor

    def __init__(self, parent: Glyph, _called_from_FL: bool = False) -> None:
        """
        There is no explicit constructor for object of this type.

        Note that objects of this class cannot be created explicitly, they are only
        generated as a result of a Glyph.Audit() operation

        Args:
            parent (Glyph): The parent of the AuditRecord, a glyph.
        """
        self._parent: Glyph = parent
        self._x = 0
        self._y = 0
        self._id = ""
        self._description = ""
        self._index = -1
        if not _called_from_FL:
            raise RuntimeError(
                "There is no explicit constructor for object of this type"
            )

    # Additions for FakeLab

    @staticmethod
    def fake_create(parent: Glyph) -> AuditRecord:
        a = AuditRecord.__new__(AuditRecord)
        a._parent = parent
        a._x = 0
        a._y = 0
        a._id = ""
        a._description = ""
        a._index = -1
        return a

    # Attributes

    @property
    def parent(self) -> Glyph:
        """
        The audit record's parent object.

        Returns:
            Glyph: The parent glyph.
        """
        return self._parent

    @property
    def position(self) -> Point:
        """
        The position of the audit mark as a point.

        Returns:
            Point: The point.
        """
        return Point(self._x, self._y)

    @property
    def p(self) -> Point:
        """
        The position of the audit mark as a point.

        Returns:
            Point: The point.
        """
        return Point(self._x, self._y)

    @property
    def id(self) -> str:
        """
        The error name.

        Returns:
            str: The name.
        """
        return self._id

    @property
    def description(self) -> str:
        """
        The error description.

        Returns:
            str: The description.
        """
        return self._description

    @property
    def index(self) -> int:
        """
        The node index in the glyph to which error is attached.

        Returns:
            int: The node index.
        """
        return self._index

    # Methods

    def CanBeFixed(self) -> bool:
        """
        Returns:
            bool: True if this error can be automatically fixed.
        """
        raise NotImplementedError

    def Repair(self) -> None:
        """
        Try to automatically fix error.
        """
        raise NotImplementedError
