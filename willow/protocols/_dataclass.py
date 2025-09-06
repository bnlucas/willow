from __future__ import annotations

from dataclasses import dataclass, Field
from typing import Protocol, runtime_checkable, TYPE_CHECKING

if TYPE_CHECKING:
    from ..types import Member


@runtime_checkable
@dataclass
class WillowDataclass(Protocol):
    """
    Protocol representing dataclass-like objects with introspection utilities.

    Provides a consistent interface for accessing fields and members of
    dataclass instances, enabling serialization, validation, and updates
    in Willow-based mixins.
    """

    @property
    def _fields(self) -> tuple[Field, ...]:
        """
        Return all dataclass fields of the instance.

        Cached or computed dynamically in implementing classes.

        :return: Tuple of `dataclasses.Field` objects representing the fields.
        """
        ...

    def _members(
        self,
        include_properties: bool = True,
        include_private: bool = False,
    ) -> dict[str, Member]:
        """
        Return all members of the dataclass instance.

        Members include fields and optionally properties. Can filter out
        private attributes if `include_private` is False.

        :param include_properties: Include properties in the result.
        :param include_private: Include attributes starting with '_' if True.
        :return: Dictionary mapping member names to their corresponding objects.
        """
        ...


__all__ = ("WillowDataclass",)
