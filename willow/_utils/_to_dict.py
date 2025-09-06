from __future__ import annotations

from typing import TYPE_CHECKING

from ._capture_member import capture_member
from ._include_member import include_member
from ._serialize_obj import serialize_obj
from ._willow_metadata import willow_metadata
from ..enums import Include

if TYPE_CHECKING:
    from ..types import DictFactory, ListFactory, MutableDict, TWillowDataclass


def to_dict(
    obj: TWillowDataclass,
    include: Include,
    *,
    include_properties: bool = True,
    include_private: bool = False,
    dict_factory: DictFactory = dict,
    list_factory: ListFactory = list,
) -> MutableDict:
    """
    Convert a dataclass instance into a dictionary according to inclusion rules.

    Fields are included or excluded based on the `Include` rule and optional
    metadata settings. Custom field-level serializers are respected if defined.

    :param obj: The dataclass instance to serialize.
    :param include: Inclusion rule specifying which fields to include.
    :param include_properties: Include properties as fields if True.
    :param include_private: Include private members (starting with '_') if True.
    :param dict_factory: Factory function to create dictionaries.
    :param list_factory: Factory function to create lists.
    :return: Dictionary representation of the instance.
    """
    data = dict_factory()
    members = obj._members(
        include_properties=include_properties,
        include_private=include_private,
    )

    for name, member in members.items():
        metadata = willow_metadata(member)

        if metadata.get("ignore", False):
            continue

        value = getattr(obj, name, None)

        if not include_member(obj, member, value, include):
            continue

        serializer = metadata.get("serializer")

        if serializer:
            data[name] = serializer(value)
        else:
            data[name] = capture_member(
                member,
                value,
                dict_factory=dict_factory,
                list_factory=list_factory,
                capture_fn=serialize_obj,
            )

    return data


__all__ = ("to_dict",)
