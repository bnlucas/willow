from __future__ import annotations


class WillowError(Exception):
    """
    Base exception for errors related to the Willow dataclass utilities.

    Can be used to catch all custom exceptions raised by Willow mixins and helpers.
    """

    pass


__all__ = ("WillowError",)
