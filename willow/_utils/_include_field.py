from __future__ import annotations

from typing import TYPE_CHECKING

from ..enums import Include
from ._default_value import default_value

if TYPE_CHECKING:
    from dataclasses import Field
    from typing import Any


def include_field(
    field: Field,
    value: Any,
    include: Include,
) -> bool:
    """
    Determine whether a dataclass field should be included during serialization.

    Inclusion is based on the specified `Include` rule and the field's value.

    :param field: The dataclass field being evaluated.
    :param value: The current value of the field.
    :param include: Inclusion rule
           (`Include.NON_NULL`, `Include.NON_DEFAULT`, or `Include.ALWAYS`).
    :return: True if the field should be included, False otherwise.
    """
    if include == Include.NON_NULL and value is None:
        return False
    elif include == Include.NON_DEFAULT and value == default_value(field):
        return False
    else:
        return True


__all__ = ("include_field",)
