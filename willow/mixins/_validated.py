from __future__ import annotations

from ..errors import ValidationError
from ._willow import WillowMixin


class Validated(WillowMixin):
    """
    Mixin for dataclasses that validates fields after initialization.

    Uses validators defined in field metadata to ensure values are valid.
    Raises `ValidationError` if any field fails validation.
    """

    def __post_init__(self):
        """
        Perform validation on all fields of the dataclass after initialization.

        Checks each field's value against a validator function defined in
        the field's metadata under the key 'validator'. Fields with `None`
        values are allowed if 'allow_none' is set to True in metadata.

        :raises ValidationError: If any field fails validation or the validator
                raises an exception.
        """
        for field in self._fields:
            value = getattr(self, field.name)
            allow_none = field.metadata.get("allow_none", False)

            if value is None and allow_none:
                continue

            validator = field.metadata.get("validator")

            if callable(validator):
                try:
                    is_validated = validator(value)

                    if not is_validated:
                        raise ValidationError(
                            f"Validation failed for field '{field.name}'",
                            field=field,
                            value=value,
                        )
                except Exception as e:
                    raise ValidationError(
                        f"Validation failed for field '{field.name}'",
                        field=field,
                        value=value,
                        error=e,
                    ) from e


__all__ = ("Validated",)
