from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import cast, TYPE_CHECKING

from ..protocols import WillowDataclass

if TYPE_CHECKING:
    from typing import Any

    from ..types import DictFactory, ListFactory, Member, Stack


def capture_obj(
    member: Member,
    value: Any,
    stack: Stack,
    *,
    dict_factory: DictFactory = dict,
    list_factory: ListFactory = list,
) -> Any:
    """
    Recursively capture an object for serialization.

    Handles nested dataclasses, lists, tuples, and dictionaries
    by pushing elements onto a stack for processing.

    :param member: The member (field or property) being captured.
    :param value: Current value of the member.
    :param stack: Stack used for iterative depth-first traversal.
    :param dict_factory: Callable used to construct dictionaries.
    :param list_factory: Callable used to construct lists.
    :return: Serialized value suitable for dict or JSON representation.
    """
    if is_dataclass(value):
        if hasattr(value, "asdict"):
            return value.asdict(dict_factory=dict_factory)
        else:
            return asdict(cast(WillowDataclass, value))
    elif isinstance(value, (list, tuple)):
        items = list_factory()

        for item in reversed(value):
            stack.append((member, item, items, "list_item", dict_factory, list_factory))

        return items
    elif isinstance(value, dict):
        data = dict_factory()

        for k, v in value.items():
            stack.append((member, v, data, k, dict_factory, list_factory))

        return data
    else:
        return value


__all__ = ("capture_obj",)
