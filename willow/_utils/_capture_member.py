from __future__ import annotations

from typing import TYPE_CHECKING

from ._capture_obj import capture_obj

if TYPE_CHECKING:
    from typing import Any

    from ..types import DictFactory, ListFactory, Member, Stack
    from ..protocols import MemberCaptureProtocol


def capture_member(
    member: Member,
    value: Any,
    *,
    dict_factory: DictFactory = dict,
    list_factory: ListFactory = list,
    capture_fn: MemberCaptureProtocol | None = None,
) -> Any:
    """
    Recursively capture a member's value for serialization.

    Uses a stack-based approach to handle nested dataclasses, collections,
    and custom capture functions.

    :param member: The member to capture (field or property).
    :param value: Current value of the member.
    :param dict_factory: Callable used to construct dictionaries.
    :param list_factory: Callable used to construct lists.
    :param capture_fn: Optional callable to capture member values; defaults
           to `capture_obj`.
    :return: Serialized value suitable for dict or JSON representation.
    """
    stack: Stack = [(member, value, None, None, dict_factory, list_factory)]
    result: Any = None
    capture_fn = capture_fn or capture_obj

    while stack:
        current_member, current_value, parent, key, dict_fac, list_fac = stack.pop()
        captured_value = capture_fn(
            current_member,
            current_value,
            stack,
            dict_factory=dict_fac,
            list_factory=list_fac,
        )

        if parent is None:
            result = captured_value
        elif isinstance(parent, list) and key == "list_item":
            parent.append(captured_value)
        elif isinstance(parent, dict) and isinstance(key, str):
            parent[key] = captured_value

    return result


__all__ = ("capture_member",)
