from __future__ import annotations

from typing import TYPE_CHECKING

from ._willow_metadata import willow_metadata

if TYPE_CHECKING:
    from dataclasses import Field
    from typing import Any


def resolve_field_key(
    field: Field,
    data: dict[str, Any],
) -> str:
    """
    Determine the correct key in a dictionary for a given dataclass field.

    Checks the field's JSON metadata for a specified key or aliases.
    Returns the first matching key found in the data, falling back to
    the field's name if no matches are found.

    :param field: The dataclass field for which to resolve the key.
    :param data: Dictionary of data being deserialized.
    :return: The key to use from the dictionary for this field.
    """
    metadata = willow_metadata(field, "json", {})
    key: str | None = metadata.get("key")

    if key and key in data:
        return key

    aliases = metadata.get("aliases", [])
    if isinstance(aliases, str):
        aliases = [aliases]

    for alias in aliases:
        if alias in data:
            return alias

    return field.name


__all__ = ("resolve_field_key",)
