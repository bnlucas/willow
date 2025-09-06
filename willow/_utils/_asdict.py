from __future__ import annotations

from typing import TYPE_CHECKING

from ._capture_member import capture_member

if TYPE_CHECKING:
    from typing import Any, MutableMapping

    from ..types import DictFactory, ListFactory, TWillowDataclass


def asdict(
    obj: TWillowDataclass,
    *,
    include_properties: bool = True,
    include_private: bool = False,
    dict_factory: DictFactory = dict,
    list_factory: ListFactory = list,
) -> MutableMapping[str, Any]:
    """
    Convert a dataclass instance to a dictionary, including optional properties.

    Recursively captures members using `capture_member`, respecting nested dataclasses
    and collection factories.

    :param obj: Dataclass instance to serialize.
    :param include_properties: Include property attributes if True.
    :param include_private: Include private members (names starting with '_') if True.
    :param dict_factory: Callable used to construct the resulting dictionary.
    :param list_factory: Callable used to construct nested lists.
    :return: Dictionary mapping member names to their values, including nested
             dataclasses.
    """
    data = dict_factory()
    members = obj._members(
        include_properties=include_properties,
        include_private=include_private,
    )

    for name, member in members.items():
        value = getattr(obj, name, None)
        data[name] = capture_member(
            member,
            value,
            dict_factory=dict_factory,
            list_factory=list_factory,
        )

    return data


__all__ = ("asdict",)
