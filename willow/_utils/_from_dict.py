from __future__ import annotations

from dataclasses import fields, MISSING
from dataclasses import Field  # noqa: F401
from typing import Any, get_type_hints, TYPE_CHECKING

from ..errors import DeserializeError
from ._deserialize_field import deserialize_field
from ._is_required import is_required
from ._willow_metadata import willow_metadata

if TYPE_CHECKING:
    from ..protocols import WillowDataclass


def from_dict(
    cls: type[WillowDataclass],
    data: dict[str, Any],
) -> WillowDataclass:
    """
    Deserialize a dictionary into a dataclass instance.

    Handles missing required fields, default values, and default factories.
    Field deserialization is delegated to `deserialize_field`.

    :param cls: The dataclass type to instantiate.
    :param data: Dictionary containing field values.
    :raises DeserializeError: If a required field is missing or default
            generation fails.
    :return: An instance of `cls` populated with data.
    """
    type_hints = get_type_hints(cls, globalns=globals())
    kwargs = dict()

    for field in fields(cls):
        if willow_metadata(field, "ignore", False):
            continue

        if field.name in data:
            kwargs[field.name] = deserialize_field(
                field, data, type_hints.get(field.name, Any)
            )
        elif is_required(field):
            raise DeserializeError(
                f"Missing required field '{field.name}'",
                field=field,
            )
        elif field.default is not MISSING:
            kwargs[field.name] = field.default
        elif field.default_factory is not MISSING:
            try:
                kwargs[field.name] = field.default_factory()
            except Exception as e:
                raise DeserializeError(
                    f"Failed to generate default for field '{field.name}'",
                    field=field,
                    value=None,
                    error=e,
                ) from e

    return cls(**kwargs)


__all__ = ("from_dict",)
