from __future__ import annotations

from typing import TYPE_CHECKING

from ._willow import WillowError

if TYPE_CHECKING:
    from typing import Any


class InclusionError(WillowError):
    """
    Error raised when an invalid inclusion rule is used during serialization.

    Attributes:
        include: The Include enum value or rule that caused the error.
    """

    def __init__(
        self,
        message: str,
        *,
        include: Any | None = None,
    ):
        self._include = include
        super().__init__(message)

    @property
    def include(self) -> Any:
        return self._include


__all__ = ("InclusionError",)
