from __future__ import annotations

from typing import Protocol
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dataclasses import Field
    from typing import Any


class HooksProtocol(Protocol):
    """
    Protocol defining hooks that dataclass-like objects can implement
    to react to validation and field updates.
    """

    def _on_validation(
        self,
        field: Field,
        value: Any,
        *,
        error: tuple[str, Exception | None] | None = None,
    ) -> None:
        """
        Hook called after a field has been validated.

        :param field: The dataclass field being validated.
        :param value: The value that was validated.
        :param error: Optional tuple containing a validation error message
                      and the exception that was raised, if any.
        """

    def _on_field_update(
        self,
        field: Field,
        value: Any,
        old_value: Any,
    ) -> None:
        """
        Hook called whenever a field's value is updated.

        :param field: The dataclass field being updated.
        :param value: The new value assigned to the field.
        :param old_value: The previous value of the field.
        """


__all__ = ("HooksProtocol",)
