from __future__ import annotations

from typing import get_args, TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Type


def get_type(
    expected_type: Type,
    fallback: tuple[Type, ...],
) -> tuple[Type, ...]:
    """
    Retrieve the type arguments of a generic type, or return a fallback.

    :param expected_type: The type from which to extract type arguments.
    :param fallback: Fallback tuple of types if `expected_type` has no arguments.
    :return: Tuple of type arguments or the fallback.
    """
    return get_args(expected_type) if get_args(expected_type) else fallback


__all__ = ("get_type",)
