from __future__ import annotations

import logging
from typing import Any

__doc__ = """
Base classes for custom list classes
"""


logger = logging.getLogger(__name__)


class Copyable:
    __slots__: list[str] = ["_parent"]

    def _copy_constructor(self, other: Any) -> None:
        from copy import deepcopy

        assert isinstance(other, type(self))

        tmp = deepcopy(other)
        for attr in self.__slots__:
            if attr == "_parent":
                # Parent is not copied
                self._parent: Any | None = None
            else:
                try:
                    setattr(self, attr, getattr(tmp, attr))
                except AttributeError:
                    logger.warning(f"Attribute not copied: {self}.{attr}")
                    pass
