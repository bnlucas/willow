from __future__ import annotations

from dataclasses import asdict, is_dataclass
from datetime import datetime, date, time
from enum import Enum
from typing import cast, TYPE_CHECKING
from uuid import UUID

from ..protocols import DataclassInstance

if TYPE_CHECKING:
    from typing import Any

    from ..types import Stack


def serialize_obj(
    obj: Any,
    stack: Stack,
) -> Any:
    """
    Recursively serialize an object to a JSON-compatible structure.

    Handles dataclasses, lists, tuples, dicts, enums, datetime objects, and UUIDs.
    Uses a stack to manage recursion without deep function calls.

    :param obj: The object to serialize.
    :param stack: Stack used for recursive serialization.
    :return: Serialized representation of the object.
    """
    if is_dataclass(obj):
        if hasattr(obj, "to_dict"):
            return obj.to_dict()
        elif hasattr(obj, "_asdict"):
            return obj._asdict()
        else:
            return asdict(cast(DataclassInstance, obj))
    elif isinstance(obj, (list, tuple)):
        items = list[Any]()

        for item in reversed(obj):
            stack.append((item, items, "list_item"))

        return items
    elif isinstance(obj, dict):
        data = dict[str, Any]()

        for k, v in obj.items():
            stack.append((v, data, k))

        return data
    elif isinstance(obj, Enum):
        return obj.value
    elif isinstance(obj, (datetime, date, time)):
        return obj.isoformat()
    elif isinstance(obj, UUID):
        return str(obj)
    else:
        return obj


__all__ = ("serialize_obj",)
