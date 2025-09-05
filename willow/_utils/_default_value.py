from __future__ import annotations

from dataclasses import MISSING
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dataclasses import Field
    from typing import Any


def default_value(
    field: Field,
) -> Any:
    """
    Retrieve the default value of a dataclass field.

    Returns the value from `default_factory` if set, otherwise from `default`.
    Returns `None` if neither is set.

    :param field: The dataclass field to inspect.
    :return: The default value of the field.
    """
    if field.default_factory is not MISSING:
        return field.default_factory()
    elif field.default is not MISSING:
        return field.default
    else:
        return None


__all__ = ("default_value",)
