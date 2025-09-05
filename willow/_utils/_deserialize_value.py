from __future__ import annotations

from dataclasses import is_dataclass
from datetime import datetime, date, time
from enum import Enum
from typing import get_args, get_origin, Union, TYPE_CHECKING
from uuid import UUID

from ._get_type import get_type

if TYPE_CHECKING:
    from typing import Any, Callable, Type


TYPE_TRANSFORMERS: dict[Type, Callable[[Any], Any]] = {
    datetime: datetime.fromisoformat,
    date: date.fromisoformat,
    time: time.fromisoformat,
    UUID: UUID,
}


def _deserialize(
    value: Any,
    expected_type: Type,
    origin: Any,
) -> Any:
    """
    Internal helper to deserialize a value into a specified type.

    Handles dataclasses with `from_dict`, lists, tuples, dictionaries,
    enums, datetime/date/time objects, UUIDs, and other standard types.

    :param value: The value to deserialize.
    :param expected_type: The type to which the value should be deserialized.
    :param origin: The origin type, obtained via `typing.get_origin`.
    :return: The deserialized value.
    """
    if is_dataclass(expected_type) and hasattr(expected_type, "from_dict"):
        return expected_type.from_dict(value)
    elif origin in (list, tuple):
        (item_type,) = get_type(expected_type, (Any,))

        return [deserialize_value(item, item_type) for item in value]
    elif origin is dict:
        key_type, value_type = get_type(expected_type, (str, Any))

        return dict(
            (deserialize_value(k, key_type), deserialize_value(v, value_type))
            for k, v in value.items()
        )
    elif issubclass(expected_type, Enum):
        return expected_type(value)

    transformer = TYPE_TRANSFORMERS.get(expected_type)

    if callable(transformer):
        return transformer(value)

    return expected_type(value) if expected_type is not Any else value


def deserialize_value(value: Any, expected_type: Type) -> Any:
    """
    Deserialize a value into the expected type, including optional types.

    Handles optional (Union with None) types and delegates complex types
    to `_deserialize`.

    :param value: The value to deserialize.
    :param expected_type: The expected type of the value.
    :return: The deserialized value.
    """
    if isinstance(value, expected_type):
        return value

    origin = get_origin(expected_type)
    args = get_args(expected_type)

    if origin is Union and type(None) in args and value is None:
        return None

    return _deserialize(value, expected_type, origin)


__all__ = ("deserialize_value",)
