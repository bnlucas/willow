from __future__ import annotations

from typing import Any, TypeVar, cast, TYPE_CHECKING

if TYPE_CHECKING:
    from ..types import Member


T = TypeVar("T")


def willow_metadata(
    member: Member,
    path: str | None = None,
    default: T | None = None,
) -> Any:
    """
    Retrieve Willow-specific metadata from a dataclass field or property.

    Supports nested lookups using dot-separated paths, e.g., "json.key".

    :param member: The dataclass field or property to inspect.
    :param path: Optional dot-separated path to a nested value within the
                 Willow metadata.
    :param default: Value to return if the key/path is not found.
    :return: The requested metadata value, or `default` if missing.
    """
    if isinstance(member, property):
        willow = cast(dict[str, Any], getattr(member, "__willow__", {}))
    else:
        willow = cast(dict[str, Any], member.metadata.get("willow", {}))

    if path is None:
        return willow

    current: Any = willow
    for part in path.split("."):
        if isinstance(current, dict):
            current = current.get(part, default)
            if current is default:
                break
        else:
            return default

    return current


__all__ = ("willow_metadata",)
