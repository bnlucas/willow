from __future__ import annotations

from typing import TYPE_CHECKING

from ._willow import WillowMixin

if TYPE_CHECKING:
    from dataclasses import Field
    from typing import Any


class Hashable(WillowMixin):
    """
    Mixin for dataclasses that provides a hash implementation based on field values.

    Enables instances to be used as dictionary keys or stored in sets.
    """

    __willow_hash: int | None = None

    def _on_field_update(
        self,
        field: Field,
        value: Any,
        old_value: Any,
    ) -> None:
        """
        Invalidate cached hash when a field value is updated.

        :param field: The dataclass field that was updated.
        :param value: The new value assigned to the field.
        :param old_value: The previous value of the field.
        """
        self.__willow_hash = None

    def __hash__(
        self,
    ) -> int:
        """
        Compute a hash value for the instance.

        The hash is derived from the tuple of the instance's current field values.
        Caches the result to avoid recomputation.

        :return: Integer hash of the instance.
        """
        if self.__willow_hash is None:
            self.__willow_hash = hash(tuple(self.asdict().values()))

        return self.__willow_hash


__all__ = ("Hashable",)
