from __future__ import annotations

from typing import TYPE_CHECKING

from ._serialize_obj import serialize_obj

if TYPE_CHECKING:
    from typing import Any, Callable

    from ..types import Stack


def serialize_field(
    obj: Any,
    serializer: Callable[[Any], Any] | None,
) -> Any:
    """
    Serialize a field value using an optional custom serializer or
    default object serialization.

    If a `serializer` callable is provided, it is applied to the object.
    Otherwise, the object is recursively serialized using `serialize_obj`.

    :param obj: The field value to serialize.
    :param serializer: Optional callable that takes the object and returns
           a serialized value.
    :return: Serialized representation of the object.
    """
    if callable(serializer):
        return serializer(obj)

    stack: Stack = [(obj, None, None)]
    result: Any = None

    while stack:
        current, parent, key = stack.pop()
        value = serialize_obj(current, stack)

        if parent is None:
            result = value
        elif isinstance(parent, list) and key == "list_item":
            parent.append(value)
        elif isinstance(parent, dict) and isinstance(key, str):
            parent[key] = value

    return result


__all__ = ("serialize_field",)
