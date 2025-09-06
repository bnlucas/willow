from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Callable


class WillowProperty(property):
    """
    Custom property that stores Willow-specific metadata.

    Supports JSON serialization, validation, and custom (de)serializers.
    Fully compatible with @x.setter and @x.deleter.
    """

    def __init__(
        self,
        fget: Callable[..., Any],
        *,
        json: dict[str, Any] | None = None,
        ignore: bool = False,
        allow_none: bool = False,
        validator: Callable[[Any], bool] | None = None,
        serializer: Callable[[Any], Any] | None = None,
        deserializer: Callable[[Any], Any] | None = None,
    ):
        super().__init__(fget)
        self.__willow__ = {
            "json": json or {},
            "ignore": ignore,
            "allow_none": allow_none,
            "validator": validator,
            "serializer": serializer,
            "deserializer": deserializer,
        }

    def setter(self, fset: Callable[..., Any]) -> WillowProperty:
        new_prop = super().setter(fset)
        new_prop.__willow__ = self.__willow__  # type: ignore[attr-defined]
        return new_prop  # type: ignore

    def deleter(self, fdel: Callable[..., Any]) -> WillowProperty:
        new_prop = super().deleter(fdel)
        new_prop.__willow__ = self.__willow__  # type: ignore[attr-defined]
        return new_prop  # type: ignore


def willow_property(
    *,
    json: dict[str, Any] | None = None,
    ignore: bool = False,
    allow_none: bool = False,
    validator: Callable[[Any], bool] | None = None,
    serializer: Callable[[Any], Any] | None = None,
    deserializer: Callable[[Any], Any] | None = None,
) -> Callable[[Callable[..., Any]], WillowProperty]:
    """
    Decorator similar to @property, but attaches Willow metadata.

    Works with @x.setter and @x.deleter, and allows custom
    validation and serialization options.
    """

    def decorator(func: Callable[..., Any]) -> WillowProperty:
        return WillowProperty(
            func,
            json=json,
            ignore=ignore,
            allow_none=allow_none,
            validator=validator,
            serializer=serializer,
            deserializer=deserializer,
        )

    return decorator


__all__ = ("willow_property",)
