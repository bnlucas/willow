from __future__ import annotations

from json import dumps
from typing import TYPE_CHECKING

from ..enums import Include
from ._to_dict import to_dict

if TYPE_CHECKING:
    from json import JSONEncoder
    from typing import Any, Callable, Type

    from ..types import TDataclassInstance


def to_json(
    self: TDataclassInstance,
    include: Include,
    *,
    wrapper: str | None = None,
    skip_keys: bool = False,
    ensure_ascii: bool = True,
    check_circular: bool = True,
    allow_nan: bool = True,
    json_cls: Type[JSONEncoder] | None = None,
    indent: int | None = None,
    separators: tuple[str, str] | None = None,
    default: Callable[[Any], Any] | None = None,
    sort_keys: bool = False,
    **kwargs: Any,
) -> str:
    """
    Serialize a dataclass instance to a JSON string.

    Fields are included or excluded based on the `Include` rule and
    field metadata. Optional JSON wrapper and custom serialization
    parameters are supported.

    :param self: Dataclass instance to serialize.
    :param include: Inclusion rule specifying which fields to include.
    :param wrapper: Optional key to wrap the serialized data in a dictionary.
    :param skip_keys: Skip keys that cannot be serialized if True.
    :param ensure_ascii: Escape non-ASCII characters if True.
    :param check_circular: Check for circular references.
    :param allow_nan: Allow NaN, Infinity, -Infinity in output.
    :param json_cls: Optional custom JSON encoder class.
    :param indent: Optional indentation level.
    :param separators: Optional separators for JSON output.
    :param default: Optional callable for objects not serializable by default.
    :param sort_keys: Sort dictionary keys if True.
    :param kwargs: Additional keyword arguments for the JSON encoder.
    :return: JSON string representation of the instance.
    """
    _data = to_dict(self, include)
    data = dict()

    for field in self._fields:
        if field.name not in _data:
            continue

        key = field.metadata.get("json", {}).get("key", field.name)

        if field.name in _data:
            data[key] = _data[field.name]

    data = {wrapper: data} if wrapper else data

    return dumps(
        data,
        skipkeys=skip_keys,
        ensure_ascii=ensure_ascii,
        check_circular=check_circular,
        allow_nan=allow_nan,
        cls=json_cls,
        indent=indent,
        separators=separators,
        default=default,
        sort_keys=sort_keys,
        **kwargs,
    )


__all__ = ("to_json",)
