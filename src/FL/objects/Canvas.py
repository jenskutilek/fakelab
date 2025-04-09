from __future__ import annotations

from typing import TYPE_CHECKING, Any

from FL.fake.Base import Copyable

if TYPE_CHECKING:
    from FL.objects.Glyph import Glyph
    from FL.objects.Image import Image
    from FL.objects.Point import Point
    from FL.objects.Rect import Rect
    from FL.objects.WeightVector import WeightVector


class Canvas(Copyable):
    """
    Canvas - class to represent screen paint area and operations

    This class can perform automatic coordinates transformations, so you can draw in
    Glyph coordinate space or, if you prefer, in screen coordinates directly.

    Use constants defined for FontLab module in `Fldict` to assign attributes to
    `Canvas` object
    """

    __slots__ = [
        "_bk_color",
        "_bk_mode",
        "_brush_color",
        "_brush_style",
        "_delta",
        "_draw_style",
        "_pen_color",
        "_pen_style",
        "_scale",
        "_text_color",
    ]

    # Constructor

    def __init__(self, canvas: Canvas | None = None) -> None:
        """
        Never create Canvas object explicitly - they must be obtained from the FontLab's
        window classes

        Canvas()       - generic constructor, creates an empty Canvas
        Canvas(Canvas) - copy constructor
        """
        self._bk_color = 0
        self._bk_mode = 0
        self._brush_color = 0
        self._brush_style = 0
        self._delta = Point()
        self._draw_style = 0
        self._pen_color = 0
        self._pen_style = 0
        self._scale = Point()
        self._text_color = 0

        if isinstance(canvas, Canvas):
            self._copy_constructor(canvas)

    # Attributes

    @property
    def delta(self) -> Point:
        """
        Horizontal shift during coordinates transformation

        Returns:
            Point: _description_
        """
        return self._delta

    @property
    def scale(self) -> Point:
        """
        Scaling during coordinates transformation

        Returns:
            Point: _description_
        """
        return self._scale

    @property
    def parent(self) -> Any:
        """
        parent object

        Returns:
            Any: The parent
        """
        raise NotImplementedError

    @property
    def draw_style(self) -> None:
        raise AttributeError

    @draw_style.setter
    def draw_style(self, value: int) -> None:
        """
        Sets current drawing mode (copy, XOR, invert etc.)

        Args:
            value (int): _description_
        """
        self._draw_style = value

    @property
    def pen_color(self) -> None:
        raise AttributeError

    @pen_color.setter
    def pen_color(self, value: int) -> None:
        """
        Sets current pen color

        Args:
            value (int): _description_
        """
        self._pen_color = value

    @property
    def pen_style(self) -> None:
        raise AttributeError

    @pen_style.setter
    def pen_style(self, value: int) -> None:
        """
        Sets current pen style (solid, dashed etc.)

        Args:
            value (int): _description_
        """
        self._pen_style = value

    @property
    def brush_color(self) -> None:
        raise AttributeError

    @brush_color.setter
    def brush_color(self, value: int) -> None:
        """
        Sets current brush color

        Args:
            value (int): _description_
        """
        self._brush_color = value

    @property
    def brush_style(self) -> None:
        raise AttributeError

    @brush_style.setter
    def brush_style(self, value: int) -> None:
        """
        Sets current brush style (solid, patterned etc.)

        Args:
            value (int): _description_
        """
        self._brush_style = value

    @property
    def text_color(self) -> None:
        raise AttributeError

    @text_color.setter
    def text_color(self, value: int) -> None:
        """
        Sets color for a text

        Args:
            value (int): _description_
        """
        self._text_color = value

    @property
    def bk_color(self) -> None:
        raise AttributeError

    @bk_color.setter
    def bk_color(self, value: int) -> None:
        """
        Sets color for a text background

        Args:
            value (int): _description_
        """
        self._bk_color = value

    @property
    def bk_mode(self) -> None:
        raise AttributeError

    @bk_mode.setter
    def bk_mode(self, value: int) -> None:
        """
        Sets background mode for a text output (transparent or opaque)

        Args:
            value (int): _description_
        """
        self._bk_mode = value

    # Methods

    def MoveTo(self, p_or_x: Point | float, y: float | None = None) -> None:
        """
        Moves current position to p or (x, y) coordinates

        Args:
            p_or_x (Point | float): _description_
            y (float | None, optional): _description_. Defaults to None.
        """
        raise NotImplementedError

    def LineTo(self, p_or_x: Point | float, y: float | None = None) -> None:
        """
        Draws a straight line to the position p or (x, y) coordinates

        Args:
            p_or_x (Point | float): _description_
            y (float | None, optional): _description_. Defaults to None.
        """
        raise NotImplementedError

    def CurveTo(self, p0: Point, p1: Point, p2: Point) -> None:
        """
        Draws a 3th-order Bezier curve from the current point to points p0, p1, p2

        Args:
            p0 (Point): _description_
            p1 (Point): _description_
            p2 (Point): _description_
        """
        raise NotImplementedError

    def SplineTo(self, p0: Point, p1: Point) -> None:
        """
        Draws a 2th-order Bezier curve from the current point to points p0, p1

        Args:
            p0 (Point): _description_
            p1 (Point): _description_
        """
        raise NotImplementedError

    def Ellipse(
        self,
        r_or_p0_or_x0: Rect | Point | float,
        p1_or_y0: Point | float | None = None,
        x1: float | None = None,
        y1: float | None = None,
    ) -> None:
        """
        Draws a filled ellipse defined by the Rect r, points p0 and p1 or set of
        coordinates

        Args:
            r_or_p0_or_x0 (Rect | Point | float): _description_
            p1_or_y0 (Point | float | None, optional): _description_. Defaults to None.
            x1 (float | None, optional): _description_. Defaults to None.
            y1 (float | None, optional): _description_. Defaults to None.
        """
        raise NotImplementedError

    def Rectangle(
        self,
        r_or_p0_or_x0: Rect | Point | float,
        p1_or_y0: Point | float | None = None,
        x1: float | None = None,
        y1: float | None = None,
    ) -> None:
        """
        Draws a filled rectangle defined by the Rect r, points p0 and p1 or set of
        coordinates

        Args:
            r_or_p0_or_x0 (Rect | Point | float): _description_
            p1_or_y0 (Point | float | None, optional): _description_. Defaults to None.
            x1 (float | None, optional): _description_. Defaults to None.
            y1 (float | None, optional): _description_. Defaults to None.
        """
        raise NotImplementedError

    def Convert(self, p: Point):
        """
        Converts coordinates from the source coordinate space

        Args:
            p (Point): _description_
        """
        raise NotImplementedError

    def UnConvert(self, p: Point):
        """
        Converts screen coordinates to the currently defined coordinate space

        Args:
            p (Point): _description_
        """
        raise NotImplementedError

    def FitGlyph(self, r: Rect, g: Glyph, w: WeightVector | None = None) -> None:
        """
        Recalculates parameters of coordinate conversion function to fit glyph g into
        rectangle r using currently selected options.

        Args:
            r (Rect): _description_
            g (Glyph): _description_
            w (WeightVector): _description_
        """
        raise NotImplementedError

    def FillGlyph(self, g: Glyph, w: WeightVector | None = None) -> None:
        """
        Fills the glyph g using current coordinate transformation.

        Args:
            g (Glyph): _description_
            w (WeightVector | None, optional): _description_. Defaults to None.
        """
        raise NotImplementedError

    def OutlineGlyph(self, g: Glyph, w: WeightVector | None = None) -> None:
        """
        Draws the glyph g outline using current coordinate transformation.

        Args:
            g (Glyph): _description_
            w (WeightVector | None, optional): _description_. Defaults to None.
        """
        raise NotImplementedError

    def TextOut(
        self, p_or_x: Point | float, s_or_y: str | float, s: str | None = None
    ) -> None:
        """
        Draws the string s in the position p or (x, y)

        Args:
            p_or_x (Point | float): _description_
            s_or_y (str | float): _description_
            s (str | None, optional): _description_. Defaults to None.
        """
        raise NotImplementedError

    def PutImage(self, i: Image, p: Point, mode: int | None = None) -> None:
        """
        Puts Image i at the selected point

        Args:
            i (Image): _description_
            p (Point): _description_
            mode (int | None, optional): _description_. Defaults to None.
        """
        raise NotImplementedError
