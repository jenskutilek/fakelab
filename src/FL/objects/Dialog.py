from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from FL.objects.Point import Point
    from FL.objects.Rect import Rect


__doc__ = "Class to represent a dialog"


class Dialog:
    """
    Dialog - class to represent Dialog

    Dialog.__doc__ reports only 'Dialog' ... so use this information with care)

    See 'yourFontLabFolder/Macros/Effects/digital.py' for an example
    """

    # Constructor

    def __init__(self, parent: object) -> None:
        """
        Class to represent a dialog.

        There is not a lot of documentations, but examples that use it pass the
        object to the parent parameter when constructing.

        ```
        class MyDialog:
            def __init__(self):
                self.d = Dialog(self)
                self.d.size = Point(300, 140)
                self.d.Center()
        ```

        Args:
            parent (object ): The parent.
        """
        pass

    # Attributes

    @property
    def size(self) -> "Point":
        raise NotImplementedError

    @size.setter
    def size(self, value: "Point") -> None:
        """
        Size of the dialog as a Point object

        Args:
            value (Point): _description_
        """
        raise NotImplementedError

    @property
    def title(self) -> str:
        raise NotImplementedError

    @title.setter
    def title(self, value: str) -> None:
        """
        Title of the dialog

        Args:
            value (str): _description_
        """
        raise NotImplementedError

    # Methods

    def Center(self) -> None:
        """
        Center dialog on screen
        """
        raise NotImplementedError

    def AddControl(
        self,
        ControlType: int,
        dimension: "Rect",
        identifier: str,
        ControlStyle: int,
        text: str,
    ) -> None:
        """
        Adds a control to the dialog, see `FLdict` for Type- and Style-constants

        Args:
            ControlType (int): The type, e.g. BUTTONCONTROL.
            dimension (Rect): The size of the control.
            identifier (str): The identifier of the control.
            ControlStyle (int): The style, e.g. STYLE_BUTTON.
        """
        raise NotImplementedError

    def GetValue(self, identifier: str) -> Any:
        """
        Get value from the specified control

        Args:
            identifier (str): _description_

        Returns:
            Any: _description_
        """
        raise NotImplementedError

    def PutValue(self, identifier: str) -> None:
        """
        Put value to the specified control

        Args:
            identifier (str): _description_
        """
        raise NotImplementedError

    def Enable(self, identifier: str, value: int) -> None:
        """
        Enable (value=1) or disable (value=0) the specified control

        Args:
            identifier (str): _description_
            value (int): _description_
        """
        raise NotImplementedError

    def Show(self, identifier: str, value: int) -> None:
        """
        Show (value=1) or hide (value=0) the specified control

        Args:
            identifier (str): _description_
            value (int): _description_
        """
        raise NotImplementedError

    def SetLabel(self, identifier: str, value: str) -> None:
        """
        Set the label of the specified control

        Args:
            identifier (str): _description_
            value (str): _description_
        """
        raise NotImplementedError

    def GetRect(self, identifier: str) -> "Rect":
        """
        Get dimension of the specified control as a Rect object

        Args:
            identifier (str): _description_
        """
        raise NotImplementedError

    def Repaint(self, identifier: str) -> None:
        """
        Redraw the specified (custom)control

        Args:
            identifier (str): _description_
        """
        raise NotImplementedError

    def Run(self) -> int:
        """
        Run the dialog

        Returns:
            int: _description_
        """
        # Return type is deduced from digital.py
        raise NotImplementedError

    def End(self, returnvalue: int | None = None):
        """
        End the dialog

        Args:
            returnvalue (int | None, optional): _description_. Defaults to None.
        """
        raise NotImplementedError
