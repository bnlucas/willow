from __future__ import annotations

from typing import TYPE_CHECKING

from ..protocols import HooksProtocol

if TYPE_CHECKING:
    from dataclasses import Field
    from typing import Any


class HooksMixin(HooksProtocol):
    """
    Mixin providing automatic hook invocation for dataclass-like objects.

    Triggers `_on_field_update` when attributes are updated after initialization.
    """

    def __setattr__(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Override `__setattr__` to trigger hooks on field updates.

        :param key: Name of the attribute being set.
        :param value: New value to assign to the attribute.
        """
        old_value = getattr(self, key, None)

        super().__setattr__(key, value)

        if getattr(self, "__willow_initialized", False):
            field = None

            if hasattr(self, "_fields"):
                field = next((f for f in self._fields if f.name == key), None)

            if field is not None:
                self._willow_hook("_on_field_update", field, value, old_value)

    def _on_validation(
        self,
        field: Field,
        value: Any,
        *,
        error: tuple[str, Exception | None] | None = None,
    ) -> None:
        """
        Hook called after a field has been validated.

        Override this method in subclasses to handle validation events.

        :param field: The dataclass field being validated.
        :param value: The value that was validated.
        :param error: Optional tuple containing a validation error message
                      and the exception that was raised, if any.
        """
        pass

    def _on_field_update(
        self,
        field: Field,
        value: Any,
        old_value: Any,
    ) -> None:
        """
        Hook called after a field has been updated.

        Override this method in subclasses to handle field update events.

        :param field: The dataclass field being updated.
        :param value: The new value assigned to the field.
        :param old_value: The previous value of the field.
        """
        pass

    def _willow_hook(
        self,
        hook_name: str,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Internal helper to invoke a hook if it exists and is callable.

        :param hook_name: Name of the hook method to invoke.
        :param args: Positional arguments to pass to the hook.
        :param kwargs: Keyword arguments to pass to the hook.
        """
        hook = getattr(self, hook_name, None)

        if callable(hook):
            hook(*args, **kwargs)


__all__ = ("HooksMixin",)
