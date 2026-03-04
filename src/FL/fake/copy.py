import logging
from copy import deepcopy
from typing import Any

logger = logging.getLogger(__name__)


def copy_fl_object(source: Any, target: Any) -> None:
    assert isinstance(target, type(source))
    tmp = deepcopy(source)
    for attr in target.__slots__:
        if attr == "_parent":
            # Parent is not copied
            target._parent = None
        else:
            try:
                setattr(target, attr, getattr(tmp, attr))
            except AttributeError:
                logger.warning(f"Attribute not copied: {target}.{attr}")
                pass
