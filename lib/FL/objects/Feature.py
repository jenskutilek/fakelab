from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from FL.objects.Font import Font


class Feature:  # Or TagObject?
    def __init__(
        self, feature_or_tag: Feature | str | None = None, value: str | None = None
    ) -> None:
        self._parent: Font | None = None
        self.tag: str = ""
        self.value: str | None = None

        # Process params

        if isinstance(feature_or_tag, Feature):
            # Copy constructor
            raise NotImplementedError

        elif isinstance(feature_or_tag, str):
            self.tag = feature_or_tag
            if value is not None:
                self.value = value
        # else: Empty Feature

    @property
    def parent(self) -> Font | None:
        return self._parent
