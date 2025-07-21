from __future__ import annotations

from typing import TYPE_CHECKING

from FL.fake.Base import Copyable

if TYPE_CHECKING:
    from FL.objects.Glyph import Glyph
    from FL.objects.Matrix import Matrix


class Guide(Copyable):
    # Constructor

    def __init__(
        self, guide_or_position: Guide | int | None = None, angle: float = 0.0
    ) -> None:
        """
        Guide - class to represent guideline

        Guide()                - generic constructor, creates a Guide with zero coordinates
        Guide(Guide)           - copy constructor
        Guide(position)        - creates a Guide and assigns position
        Guide(position, angle) - creates a Guide and assigns position and width values

        Args:
            guide_or_position (Guide | int | None, optional): The guide to be copied,
                or the position of the guide. Defaults to None.
            angle (float, optional): The width. Defaults to 0.0.
        """
        self._parent: Glyph | None = None
        self.position: int = 0
        self.width: int = 0
        self.angle: float = 0.0
        self.positions: list[int] = [0]
        self.widths: list[int] = [0]

        # Without API:
        self._color: str | None = None
        self._name: str | None = None

        # Process params

        if isinstance(guide_or_position, Guide):
            self._copy_constructor(guide_or_position)

        elif isinstance(guide_or_position, int):
            self.position = guide_or_position
            if angle is not None:
                self.angle = angle  # XXX: or width?
        # else: Empty guide

    def __repr__(self) -> str:
        return f"<Guide pos: {self.position}, angle: {self.angle}>"

    @property
    def parent(self) -> Glyph | None:
        return self._parent

    # Methods

    def Transform(self, m: Matrix) -> None:
        """applies Matrix transformation to the Guide

        Args:
            m (Matrix): _description_
        """
        raise NotImplementedError

    def TransformLayer(self, m: Matrix, layernum: int) -> None:
        """applies Matrix transformation to the selected layer of the Guide

        Args:
            m (Matrix): _description_
        """
        raise NotImplementedError
