from __future__ import annotations

from typing import TYPE_CHECKING

from ._include_field import include_field
from ._serialize_field import serialize_field
from ..enums import Include

if TYPE_CHECKING:
    from typing import Any

    from ..types import TDataclassInstance


def to_dict(
    self: TDataclassInstance,
    include: Include,
) -> dict[str, Any]:
    """
    Serialize a dataclass instance to a dictionary.

    Fields are included or excluded based on the provided `Include` rule
    and optional metadata settings. Custom serializers can be applied
    using field metadata.

    :param self: Dataclass instance to serialize.
    :param include: Inclusion rule specifying which fields to include.
    :return: Dictionary representation of the instance.
    """
    data: dict[str, Any] = dict()

    for field in self._fields:
        cfg = field.metadata.get("willow", {})

        if cfg.get("ignore", False):
            continue

        value = getattr(self, field.name)

        if not include_field(field, value, include):
            continue

        data[field.name] = serialize_field(value, cfg.get("serializer"))

    return data


__all__ = ("to_dict",)
