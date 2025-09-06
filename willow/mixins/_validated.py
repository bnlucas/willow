from __future__ import annotations

from typing import TYPE_CHECKING

from ..errors import ValidationError
from .._utils import willow_metadata
from ._willow import WillowMixin

if TYPE_CHECKING:
    from dataclasses import Field
    from typing import Any


class Validated(WillowMixin):
    """
    Mixin for dataclasses that performs automatic validation of fields.

    Uses validator functions defined in field metadata under the key 'validator'.
    Fields may optionally allow `None` values if 'allow_none' is True.
    Raises `ValidationError` if validation fails.
    """

    def __post_init__(self):
        """
        Validate all fields after dataclass initialization.

        Iterates through all fields and validates their values using the
        associated validator from metadata. Skips validation for fields
        with `None` values if 'allow_none' is True.

        :raises ValidationError: If a field fails validation or the validator raises
                an exception.
        """
        for field in self._fields:
            value = getattr(self, field.name)
            self._validate_field(field, value)

    def _on_field_update(
        self,
        field: Field,
        value: Any,
        old_value: Any,
    ) -> None:
        """
        Validate a field whenever its value is updated.

        :param field: The dataclass field being updated.
        :param value: The new value assigned to the field.
        :param old_value: The previous value of the field.
        """
        self._validate_field(field, value)

    def _on_validation(
        self,
        field: Field,
        value: Any,
        *,
        error: tuple[str, Exception | None] | None = None,
    ) -> None:
        """
        Hook called when a validation error occurs.

        Raises `ValidationError` with the provided message and field info.

        :param field: The dataclass field being validated.
        :param value: The value that failed validation.
        :param error: Tuple containing error message and optional exception.
        """
        if error:
            message, exception = error

            raise ValidationError(
                message=message,
                field=field,
                value=value,
                error=exception,
            )

    def _validate_field(
        self,
        field: Field,
        value: Any,
    ) -> None:
        """
        Perform validation on a single field.

        Skips validation if `_willow_validation` is False.
        Uses the validator from field metadata. If `allow_none` is True
        and the value is None, validation is skipped.

        :param field: The dataclass field to validate.
        :param value: The value to validate.
        """
        if not self._willow_validation:
            return

        error: tuple[str, Exception | None] | None = None
        metadata = willow_metadata(field)
        allow_none = metadata.get("allow_none", False)
        validator = metadata.get("validator")

        try:
            if (value is None and allow_none) or validator is None:
                return

            try:
                is_validated = validator(value)

                if not is_validated:
                    error = (f"Validation failed for field '{field.name}'", None)
            except Exception as e:
                error = (f"Validation failed for field '{field.name}'", e)
        finally:
            self._willow_hook("_on_validation", field, value, error=error)


__all__ = ("Validated",)
