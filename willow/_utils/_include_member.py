from __future__ import annotations

from typing import TYPE_CHECKING

from ..enums import Include
from ..errors import InclusionError

if TYPE_CHECKING:
    from ..types import Member, TWillowDataclass


def include_member(
    obj: TWillowDataclass,
    member: Member,
    value: object,
    include: Include,
) -> bool:
    """
    Evaluate whether a dataclass member should be included during serialization.

    Supports standard inclusion rules defined by the `Include` enum.

    Inclusion rules:
      - ALWAYS: Always include the member.
      - NON_NONE: Include only if the value is not None.
      - NON_EMPTY: Include if the value is truthy (non-empty for strings, collections).
      - NON_DEFAULT: Include only if the value differs from the default.

    :param obj: The dataclass instance containing the member.
    :param member: The field or property being evaluated.
    :param value: Current value of the member.
    :param include: Inclusion rule to apply.
    :return: True if the member passes the inclusion rule.
    :raises InclusionError: If NON_DEFAULT is used with a property or an unknown
            rule is provided.
    """
    if include is Include.ALWAYS:
        return True
    if include is Include.NON_NONE:
        return value is not None
    if include is Include.NON_EMPTY:
        if value is None:
            return False
        if isinstance(value, (str, bytes, list, tuple, set, dict)):
            return bool(value)
        return True
    if include is Include.NON_DEFAULT:
        if isinstance(member, property):
            raise InclusionError(
                "Cannot use Include.NON_DEFAULT with include_properties=True"
            )
        return value == getattr(obj, member.name)

    raise InclusionError(f"Unhandled Include rule: {include}", include=include)


__all__ = ("include_member",)
