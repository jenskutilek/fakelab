from __future__ import annotations

import array
from typing import TYPE_CHECKING

from vfbLib.typing import BackgroundImageDict, BitmapDataDict

from FL.objects.Point import Point

if TYPE_CHECKING:
    from FL.objects.Glyph import Glyph
    from FL.objects.Rect import Rect


class Image:
    __slots__ = [
        "_data",
        "_empty",
        "_size",
        "_traceenabled",
        "_height",
        "_width",
        # Non-API
        "_flag",
        "_origin",
        "_preview",
        "_size_units",
    ]

    def __init__(
        self, width_or_image: int | Image | None = None, height: int | None = None
    ) -> None:
        """
        Image - class to represent image

        Image() - generic constructor, creates an Image with zero coordinates
        Image(Image) - copy constructor
        Image(int width, int height) - creates an Image of given size
        """
        self._empty = True
        self._data = array.array("H")
        self._size = len(self._data)
        self._width = 0
        self._height = 0
        self._traceenabled = True

        # Non-API
        self._flag = 0
        self._origin = Point()
        self._size_units = Point()

        if isinstance(width_or_image, int):
            self._width = width_or_image
            if not isinstance(height, int):
                raise TypeError
            self._height = height
            self._empty = True
        elif isinstance(width_or_image, Image):
            # copy constructor
            image = width_or_image
            self._width = image.width
            self._height = image.height
            self._empty = bool(image.empty)
            self._traceenabled = bool(image.traceenabled)
            self._data = array.array("H", image.data)
            self._size = image.size
        # else empty image

    # Additions for FakeLab

    def fake_deserialize(self, data: BackgroundImageDict) -> None:
        x, y = data["origin"]
        self._origin.x = x
        self._origin.y = y
        x, y = data["size_units"]
        self._size_units.x = x
        self._size_units.y = y
        x, y = data["size_pixels"]
        self._width = x
        self._height = y
        self._flag = data["bitmap"]["flag"]
        self._data = array.array("H", data["bitmap"]["data"])
        self._empty = False

    def fake_serialize(self) -> BackgroundImageDict | None:
        if self._empty:
            return None

        d = BackgroundImageDict(
            origin=(
                int(self._origin.x),
                int(self._origin.y),
            ),
            size_units=(
                int(self._size_units.x),
                int(self._size_units.y),
            ),
            size_pixels=(self.width, self.height),
            bitmap=BitmapDataDict(flag=self._flag, data=self.data),
        )
        return d

    # Attributes

    @property
    def width(self) -> int:
        """
        Dimensions of the image

        Returns:
            int: The width of the image in pixels
        """
        return self._width

    @width.setter
    def width(self, value: int) -> None:
        raise RuntimeError("Class Image does not have writable attributes")

    @property
    def height(self) -> int:
        """
        Dimensions of the image

        Returns:
            int: The height of the image in pixels
        """
        return self._height

    @height.setter
    def height(self, value: int) -> None:
        raise RuntimeError("Class Image does not have writable attributes")

    @property
    def empty(self) -> int:
        """
        The empty status of the image

        Returns:
            int: Whether the image is empty
        """
        return int(self._empty)

    @empty.setter
    def empty(self, value: int) -> None:
        raise RuntimeError("Class Image does not have writable attributes")

    @property
    def size(self) -> int:
        """
        The size of the image buffer

        Returns:
            int: The size of the image buffer
        """
        return len(self.data)

    @size.setter
    def size(self, value: int) -> None:
        raise RuntimeError("Class Image does not have writable attributes")

    @property
    def data(self) -> list[int]:
        """
        Access the image buffer

        Returns:
            list[int] | None: _description_
        """
        return [i for i in self._data]

    @data.setter
    def data(self, value: bytes | None) -> None:
        # if value is None:
        #     self._data = array.array("H", [0] * self.width * self.height)
        # else:
        #     self._data = array.array("H", value)
        # Does nothing
        pass

    @property
    def traceenabled(self) -> int:
        """
        There is a possibility to trace the image with the Trace command

        Returns:
            int: Whether the image can be traced
        """
        return int(self._traceenabled)

    @traceenabled.setter
    def traceenabled(self, value: int) -> None:
        raise RuntimeError("Class Image does not have writable attributes")

    # Methods

    def Create(self, width: int, height: int) -> None:
        """
        Creates a blank image of given size.

        Args:
            width (int): The width in pixels
            height (int): The height in pixels
        """
        raise NotImplementedError

    def Trace(self, glyph: Glyph) -> None:
        """
        Traces the image with the current option and adds it to the glyph

        Args:
            glyph (Glyph): The glyph to which the traced outline will be added
        """
        raise NotImplementedError

    def Clear(self) -> None:
        """
        Clears the image
        """
        # (not reported by docstring)
        raise NotImplementedError

    def GetPixel(self, p: Point) -> int:
        # (not reported by docstring)
        raise NotImplementedError

    def HLine(self, x0: int, x1: int, y: int, color: int) -> None:
        # (not reported by docstring)
        raise NotImplementedError

    def ImageBlt(self, dest: Image, source_rect: Rect, dest_point: Point) -> None:
        # (not reported by docstring)
        raise NotImplementedError

    def Invert(self) -> None:
        # (not reported by docstring)
        raise NotImplementedError

    def SetPixel(self, p: Point) -> None:
        # (not reported by docstring)
        raise NotImplementedError
