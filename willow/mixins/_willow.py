from __future__ import annotations

from dataclasses import asdict, fields
from typing import TYPE_CHECKING

from ..protocols import DataclassInstance

if TYPE_CHECKING:
    from dataclasses import Field
    from typing import Any


class WillowMixin(DataclassInstance):
    """
    Mixin providing utility methods for dataclass instances.

    Caches results of `asdict` and `fields` to improve repeated access.
    """

    __asdict_cache: dict[str, Any] | None = None
    __fields_cache: tuple[Field, ...] | None = None

    def _asdict(
        self,
        *,
        dict_factory: Any = dict,
        refresh: bool = False,
    ) -> dict[str, Any]:
        """
        Return a dictionary representation of the dataclass instance.

        This method caches the result to avoid recomputation on subsequent calls.

        :param dict_factory: Callable that constructs the returned dictionary.
        :param refresh: If True, recompute the dictionary even if a cached value exists.
        :return: A dictionary mapping field names to their values.
        """
        if refresh or self.__asdict_cache is None:
            self.__asdict_cache = asdict(self, dict_factory=dict_factory)

        return self.__asdict_cache

    @property
    def _fields(
        self,
    ) -> tuple[Field, ...]:
        """
        Return a tuple of dataclass fields for the instance.

        This property caches the result to avoid recomputation.

        :return: Tuple of `dataclasses.Field` objects for the dataclass.
        """
        if self.__fields_cache is None:
            self.__fields_cache = fields(self)

        return self.__fields_cache


__all__ = ("WillowMixin",)
