from __future__ import annotations

from dataclasses import MISSING
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dataclasses import Field


def is_required(
    field: Field,
) -> bool:
    """
    Determine if a dataclass field is required.

    A field is required if it has neither a default value nor a default factory.

    :param field: The dataclass field to check.
    :return: True if the field is required, False otherwise.
    """
    return field.default is MISSING and field.default_factory is MISSING


__all__ = ("is_required",)
