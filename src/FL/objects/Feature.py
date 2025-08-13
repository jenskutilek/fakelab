from __future__ import annotations

from typing import TYPE_CHECKING

from FL.fake.Base import Copyable

if TYPE_CHECKING:
    from FL.objects.Font import Font


__doc__ = "Class to represent an OpenType feature-definition record"


class Feature(Copyable):  # Or TagObject?
    """
    OpenType feature-definition record
    """

    __slots__ = ["_parent", "_tag", "_value"]

    # Constructor

    def __init__(
        self, feature_or_tag: Feature | str | None = None, value: str | None = None
    ) -> None:
        """
        Feature()
            generic constructor, creates an empty Feature record
        Feature(Feature)
            copy constructor
        Feature(string tag)
            creates feature, assigns 'tag' and empty value
        Feature(string tag, string value)
            creates feature and assigns values to both attributes

        Args:
            feature_or_tag (Feature | str | None, optional): _description_. Defaults to None.
            value (str | None, optional): _description_. Defaults to None.
        """
        self._parent: Font | None = None
        self._tag = ""
        self._value: str | None = None

        # Process params

        if isinstance(feature_or_tag, Feature):
            self._copy_constructor(feature_or_tag)

        elif isinstance(feature_or_tag, str):
            self.tag = feature_or_tag
            if value is not None:
                self.value = value
        # else: Empty Feature

    @property
    def parent(self) -> Font | None:
        """
        Returns:
            Font | None: The parent Font object, or None.
        """
        return self._parent

    @property
    def tag(self) -> str:
        """
        Returns:
            str: The four-character feature tag.
        """
        return self._tag

    @tag.setter
    def tag(self, value: str) -> None:
        self._tag = value

    @property
    def value(self) -> str | None:
        """
        Returns:
            str | None: The feature code in AFDKO syntax.
        """
        return self._value

    @value.setter
    def value(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("CXX: type error.")
        self._value = value
