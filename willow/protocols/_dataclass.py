from __future__ import annotations

from dataclasses import dataclass, Field
from typing import Protocol, runtime_checkable


@runtime_checkable
@dataclass
class DataclassInstance(Protocol):
    """
    Protocol for dataclass-like instances.

    Ensures that implementing classes provide a `_fields` property returning
    the tuple of dataclass fields.
    """

    @property
    def _fields(self) -> tuple[Field, ...]:
        """
        Return a tuple of dataclass fields for the instance.

        :return: Tuple of `dataclasses.Field` objects.
        """
        ...


__all__ = ("DataclassInstance",)
