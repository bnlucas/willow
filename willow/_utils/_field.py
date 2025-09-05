from __future__ import annotations

import dataclasses

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Callable


def field(
    *,
    default: Any = dataclasses.MISSING,
    default_factory: Any = dataclasses.MISSING,
    init: bool = True,
    repr: bool = True,
    hash: bool | None = None,
    compare: bool = True,
    metadata: dict[str, Any] | None = None,
    json: dict[str, Any] | None = None,
    validator: Callable[[Any], bool] | None = None,
    allow_none: bool = False,
    willow: dict[str, Any] | None = None,
    **kwargs: Any,
):
    """
    Custom dataclass field wrapper that extends `dataclasses.field`.

    Adds support for:
        - JSON serialization metadata (`json`)
        - Field validation (`validator`)
        - Allowing None values (`allow_none`)
        - Arbitrary Willow-specific metadata (`willow`)

    :param default: Default value for the field.
    :param default_factory: Factory function to generate default values.
    :param init: Include in the generated __init__ method.
    :param repr: Include in the generated __repr__ method.
    :param hash: Include in the generated __hash__ method.
    :param compare: Include in the generated comparison methods.
    :param metadata: Additional metadata dictionary.
    :param json: Optional JSON-related metadata to store in `metadata['json']`.
    :param validator: Optional callable to validate field values.
    :param allow_none: If True, allow the field to be None.
    :param willow: Optional dictionary for Willow-specific metadata.
    :param kwargs: Additional keyword arguments passed to `dataclasses.field`.
    :return: A `dataclasses.Field` object with extended metadata.
    """
    metadata = metadata or {}
    metadata["allow_none"] = allow_none

    if json:
        metadata["json"] = json

    if validator:
        metadata["validator"] = validator

    if willow:
        metadata["willow"] = willow

    args: dict[str, Any] = dict(
        init=init,
        repr=repr,
        hash=hash,
        compare=compare,
        metadata=metadata,
        **kwargs,
    )

    if default is not dataclasses.MISSING:
        args["default"] = default
    if default_factory is not dataclasses.MISSING:
        args["default_factory"] = default_factory

    return dataclasses.field(**args)
