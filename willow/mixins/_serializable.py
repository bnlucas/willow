from __future__ import annotations

from typing import TYPE_CHECKING

from ..enums import Include
from .._utils import to_dict, to_json, from_dict, from_json
from ._willow import WillowMixin

if TYPE_CHECKING:
    from json import JSONEncoder, JSONDecoder
    from typing import Any, Callable, ClassVar, Type

    from ..protocols import DataclassInstance


class Serializable(WillowMixin):
    """
    Mixin for dataclasses providing dictionary and JSON serialization/deserialization.

    Features:
      - Convert instances to/from dicts and JSON strings.
      - Supports class-level defaults via `__json_wrapper__` and `__inclusion__`.
      - Allows per-call overrides for JSON wrapper and inclusion rules.
      - Respects custom field-level serializers and deserializers.

    ClassVars:
      __json_wrapper__ : str | None
          Optional default JSON wrapper key for serialized output.
      __inclusion__ : Include | None
          Default inclusion rule for fields (`ALWAYS`, `NON_NULL`, `NON_DEFAULT`).
    """

    __json_wrapper__: ClassVar[str | None] = None
    __inclusion__: ClassVar[Include | None] = Include.ALWAYS

    @classmethod
    def from_dict(cls, data: dict) -> DataclassInstance:
        """
        Create an instance of the class from a dictionary.

        Respects field metadata and type hints.
        Fields marked with `willow.ignore=True` are skipped.

        :param data: Dictionary containing field values.
        :return: Instance populated from the dictionary.
        """
        return from_dict(cls, data)

    @classmethod
    def from_json(
        cls,
        s: str | bytes | bytearray,
        *,
        wrapper: str | None = None,
        json_cls: Type[JSONDecoder] | None = None,
        object_hook: Callable[[dict[Any, Any]], Any] | None = None,
        parse_float: Callable[[str], Any] | None = None,
        parse_int: Callable[[str], Any] | None = None,
        parse_constant: Callable[[str], Any] | None = None,
        object_hook_pairs: Callable[[list[tuple[Any, Any]]], Any] | None = None,
    ) -> DataclassInstance:
        """
        Create an instance from a JSON string.

        :param s: JSON string, bytes, or bytearray.
        :param wrapper: Optional JSON wrapper key. Defaults to `__json_wrapper__`.
        :param json_cls: Optional JSON decoder class.
        :param object_hook: Optional callable for decoding objects.
        :param parse_float: Optional callable to parse floats.
        :param parse_int: Optional callable to parse integers.
        :param parse_constant: Optional callable to handle NaN/Infinity.
        :param object_hook_pairs: Optional callable for decoding key-value pairs.
        :return: Instance populated from the JSON data.
        """
        wrapper = wrapper or getattr(cls, "__json_wrapper__")
        return from_json(
            cls,
            s,
            wrapper=wrapper,
            json_cls=json_cls,
            object_hook=object_hook,
            parse_float=parse_float,
            parse_int=parse_int,
            parse_constant=parse_constant,
            object_hook_pairs=object_hook_pairs,
        )

    def to_dict(self) -> dict:
        """
        Serialize the instance to a dictionary.

        Uses class-level inclusion rule `__inclusion__` by default,
        but can be overridden by per-call logic if needed.

        :return: Dictionary representation of the instance.
        """
        include = getattr(self, "__inclusion__", Include.ALWAYS)
        return to_dict(self, include)

    def to_json(
        self,
        *,
        wrapper: str | None = None,
        include: Include = Include.ALWAYS,
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
        Serialize the instance to a JSON string.

        Allows per-call control of:
          - `wrapper`: JSON wrapper key, defaults to `__json_wrapper__`.
          - `include`: Field inclusion rules, defaults to `__inclusion__`.

        Supports additional standard JSON encoder arguments.

        :param wrapper: Optional JSON wrapper key. Defaults to `__json_wrapper__`.
        :param include: Optional field inclusion rule. Defaults to `__inclusion__`.
        :param skip_keys: Skip keys that cannot be serialized.
        :param ensure_ascii: Escape non-ASCII characters.
        :param check_circular: Check for circular references.
        :param allow_nan: Allow NaN, Infinity, -Infinity.
        :param json_cls: Optional JSON encoder class.
        :param indent: Optional indentation for JSON.
        :param separators: Optional key-value separators.
        :param default: Callable for non-serializable objects.
        :param sort_keys: Sort keys if True.
        :param kwargs: Additional keyword arguments for JSON encoder.
        :return: JSON string representation.
        """
        wrapper = wrapper or getattr(type(self), "__json_wrapper__")
        include = include or getattr(type(self), "__inclusion__", Include.ALWAYS)

        return to_json(
            self,
            include,
            wrapper=wrapper,
            skip_keys=skip_keys,
            ensure_ascii=ensure_ascii,
            check_circular=check_circular,
            allow_nan=allow_nan,
            json_cls=json_cls,
            indent=indent,
            separators=separators,
            default=default,
            sort_keys=sort_keys,
            **kwargs,
        )


__all__ = ("Serializable",)
