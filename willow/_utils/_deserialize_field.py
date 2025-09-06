from __future__ import annotations

from typing import TYPE_CHECKING

from ..errors import DeserializeError
from ._deserialize_value import deserialize_value
from ._willow_metadata import willow_metadata

if TYPE_CHECKING:
    from dataclasses import Field
    from typing import Any, Type


def deserialize_field(
    field: Field,
    data: dict[str, Any],
    expected_type: Type,
) -> Any:
    """
    Deserialize a value from a dictionary for a specific dataclass field.

    Uses an optional custom deserializer specified in the field's metadata.
    If no custom deserializer is provided, falls back to `deserialize_value`.
    Raises `DeserializeError` if deserialization fails.

    :param field: The dataclass field to deserialize.
    :param data: Dictionary containing field values.
    :param expected_type: Expected type of the field value.
    :raises DeserializeError: If deserialization fails for the field.
    :return: Deserialized value for the field.
    """
    deserializer = willow_metadata(field, "deserializer")

    try:
        value = data[field.name]

        if callable(deserializer):
            return deserializer(value)

        return deserialize_value(value, expected_type)
    except Exception as e:
        raise DeserializeError(
            f"Failed to deserialize field '{field.name}'",
            field=field,
            value=data.get(field.name),
            error=e,
        ) from e


__all__ = ("deserialize_field",)
