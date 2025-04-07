from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from FL import Glyph, Matrix


class Guide:

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

        # Process params

        if isinstance(guide_or_position, Guide):
            # Copy constructor
            raise NotImplementedError

        elif isinstance(guide_or_position, int):
            self.position = guide_or_position
            if angle is not None:
                self.angle = angle  # XXX: or width?
        # else: Empty guide

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
