from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING

from ._willow import WillowMixin

if TYPE_CHECKING:
    from typing import Any

    from ..protocols import DataclassInstance


class Updatable(WillowMixin):
    """
    Mixin for dataclasses that provides copy and update utilities.

    Supports creating modified copies of an instance without mutating the original.
    """

    def copy(
        self,
    ) -> DataclassInstance:
        """
        Return a copy of the current instance.

        This is an alias to `update()` with no field modifications.

        :return: A new instance of the same class identical to the original.
        """
        return self.update()

    def update(
        self,
        **kwargs: Any,
    ) -> DataclassInstance:
        """
        Return a new instance with updated fields.

        :param kwargs: Field values to override in the new instance.
        :return: A new instance of the same class with updated field values.
        """
        data = self._asdict()
        data.update(kwargs)

        return self.__class__(**deepcopy(data))


__all__ = ("Updatable",)
