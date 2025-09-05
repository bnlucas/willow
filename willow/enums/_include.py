from __future__ import annotations

from enum import Enum, auto


class Include(Enum):
    """
    Enum specifying inclusion rules for serialization.

    - NON_NULL: Include fields that are not None.
    - NON_DEFAULT: Include fields that differ from their default value.
    - ALWAYS: Always include fields.
    """

    NON_NULL = auto()
    NON_DEFAULT = auto()
    ALWAYS = auto()


__all__ = ("Include",)
