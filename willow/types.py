from __future__ import annotations

from typing import Any, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from .protocols import DataclassInstance


StackParent = list[Any] | dict[str, Any] | None
StackKey = str | Any | None
Stack = list[tuple[Any, StackParent, StackKey]]
"""
Type alias representing the serialization/deserialization stack.

Each item is a tuple of:
- current object being processed,
- parent container (list, dict, or None),
- key in the parent (str, Any, or None)
"""

TDataclassInstance = TypeVar("TDataclassInstance", bound=DataclassInstance)
"""
Type variable bound to any dataclass instance implementing the DataclassInstance
protocol. Used for generic typing in functions that operate on dataclass instances.
"""

__all__ = (
    "Stack",
    "TDataclassInstance",
)
