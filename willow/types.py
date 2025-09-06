from __future__ import annotations

from dataclasses import Field
from typing import Any, Callable, MutableMapping, TypeVar

from .protocols import WillowDataclass

# Types representing dataclass members (fields or properties)
Member = Field | property

# Standard mutable dictionary type
MutableDict = MutableMapping[str, Any]

# Factory callables for dictionaries and lists
DictFactory = Callable[[], MutableDict]
ListFactory = Callable[[], list[Any]]

# Stack structures used for recursive serialization
StackParent = list[Any] | MutableDict | None
StackKey = str | Any | None
Stack = list[tuple[Member, Any, StackParent, StackKey, DictFactory, ListFactory]]

# Generic type for dataclass instances implementing WillowDataclass
TWillowDataclass = TypeVar("TWillowDataclass", bound=WillowDataclass)

__all__ = (
    "DictFactory",
    "ListFactory",
    "Member",
    "MutableDict",
    "Stack",
    "TWillowDataclass",
)
