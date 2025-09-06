from __future__ import annotations

from contextlib import contextmanager
from copy import deepcopy
from typing import TYPE_CHECKING

from ._willow import WillowMixin

if TYPE_CHECKING:
    from typing import Any

    from ..protocols import WillowDataclass


class Updatable(WillowMixin):
    """
    Mixin for dataclasses that provides copy and update utilities.

    Enables creating modified copies of an instance without mutating the original.
    """

    def copy(
        self,
    ) -> WillowDataclass:
        """
        Return a copy of the current instance.

        This is equivalent to calling `update()` with no modifications.

        :return: A new instance identical to the original.
        """
        return self.update()

    def update(
        self,
        *,
        use_deepcopy: bool = False,
        **kwargs: Any,
    ) -> WillowDataclass:
        """
        Return a new instance with updated field values.

        :param use_deepcopy: If True, deep copy the field values before creating
               the new instance.
        :param kwargs: Field values to override in the new instance.
        :return: A new instance of the same class with updated fields.
        """
        data = self.asdict()
        data.update(kwargs)

        if use_deepcopy is True:
            data = deepcopy(data)

        return self.__class__(**data)

    @contextmanager
    def batch_update(self):
        """
        Context manager to temporarily disable validation during multiple updates.

        After exiting the context, validation is performed on all dirty fields.

        Usage:
        >>> with instance.batch_update() as inst:
        >>>     inst.field1 = value1
        >>>     inst.field2 = value2
        """
        original = self._willow_validation
        self._willow_validation = False

        yield self

        self._willow_validation = original

        if self._willow_validation and hasattr(self, "_validate_field"):
            for field_name in self._dirty_fields:
                field = next((f for f in self._fields if f.name == field_name), None)

                if field is None:
                    continue

                value = getattr(self, field.name)
                self._validate_field(field, value)


__all__ = ("Updatable",)
