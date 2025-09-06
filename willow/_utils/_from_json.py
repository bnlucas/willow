from __future__ import annotations

from dataclasses import fields
from json import loads, JSONDecodeError
from typing import TYPE_CHECKING

from ._from_dict import from_dict
from ._resolve_field_key import resolve_field_key
from ..errors import DeserializeError

if TYPE_CHECKING:
    from json import JSONDecoder
    from typing import Any, Callable, Type

    from ..protocols import WillowDataclass


def from_json(
    cls: type[WillowDataclass],
    s: str | bytes | bytearray,
    *,
    wrapper: str | None = None,
    json_cls: Type[JSONDecoder] | None = None,
    object_hook: Callable[[dict[Any, Any]], Any] | None = None,
    parse_float: Callable[[str], Any] | None = None,
    parse_int: Callable[[str], Any] | None = None,
    parse_constant: Callable[[str], Any] | None = None,
    object_hook_pairs: Callable[[list[tuple[Any, Any]]], Any] | None = None,
) -> WillowDataclass:
    """
    Deserialize a JSON string or bytes into a dataclass instance.

    Supports optional JSON wrapper keys and custom JSON decoder hooks.
    Delegates field deserialization to `from_dict` and resolves keys
    using `resolve_field_key`.

    :param cls: The dataclass type to instantiate.
    :param s: JSON string, bytes, or bytearray to deserialize.
    :param wrapper: Optional top-level key to extract data from the JSON.
    :param json_cls: Optional custom JSON decoder class.
    :param object_hook: Optional callable for custom object decoding.
    :param parse_float: Optional callable for decoding floats.
    :param parse_int: Optional callable for decoding integers.
    :param parse_constant: Optional callable for decoding constants
           (NaN, Infinity, etc.).
    :param object_hook_pairs: Optional callable for decoding key-value pairs
           aslist of tuples.
    :raises DeserializeError: If JSON decoding fails or field deserialization fails.
    :return: An instance of `cls` populated with the deserialized data.
    """
    try:
        _data = loads(
            s,
            cls=json_cls,
            object_hook=object_hook,
            parse_float=parse_float,
            parse_int=parse_int,
            parse_constant=parse_constant,
            object_pairs_hook=object_hook_pairs,
        )

        _data = _data[wrapper] if wrapper else _data
        data = dict()

        for field in fields(cls):
            key = resolve_field_key(field, _data)

            if key not in _data:
                continue

            if field.name in data:
                raise KeyError(f"Duplicate key '{key}' for field '{field.name}'")

            data[field.name] = _data[key]

        return from_dict(cls, data)
    except JSONDecodeError as e:
        raise DeserializeError(
            f"Failed to deserialize JSON to '{cls.__name__}': {e}"
        ) from e


__all__ = ("from_json",)
