from __future__ import annotations

from dataclasses import fields
from typing import TYPE_CHECKING

from ._hooks import HooksMixin
from .._utils import asdict
from ..protocols import WillowDataclass

if TYPE_CHECKING:
    from dataclasses import Field
    from typing import Any

    from ..types import DictFactory, Member, MutableDict


class WillowMixin(WillowDataclass, HooksMixin):
    """
    Base mixin for dataclasses providing utility methods and caching.

    Features:
      - Cached `asdict` results for efficient dictionary conversions.
      - Cached dataclass `fields` and field names for introspection.
      - Cached properties and property names for repeated access.
      - Automatic cache invalidation when a tracked field is updated.
      - Supports introspection of fields and properties for validation and updates.
    """

    __willow_initialized: bool = False
    __willow_validation: bool = True
    __willow_asdict: MutableDict | None = None
    __willow_fields: tuple[Field, ...] | None = None
    __willow_field_names: set[str] | None = None
    __willow_dirty_fields = set[str]()
    __willow_properties: dict[str, property] | None = None
    __willow_property_names: set[str] | None = None

    def __post_init__(self) -> None:
        """
        Marks the instance as initialized after dataclass __init__.
        """
        self.__willow_initialized = True

    def _on_validation(
        self,
        field: Field,
        value: Any,
        *,
        error: tuple[str, Exception | None] | None = None,
    ) -> None:
        """
        Hook called during field validation.

        Removes the field from the dirty set regardless of validation outcome.

        :param field: The dataclass field being validated.
        :param value: The value that was validated.
        :param error: Optional tuple containing a validation error message
                      and the exception that was raised, if any.
        """
        self.__willow_dirty_fields.discard(field.name)

    def _on_field_update(
        self,
        field: Field,
        value: Any,
        old_value: Any,
    ) -> None:
        """
        Hook called when a field is updated.

        Clears relevant caches and marks the field as dirty.

        :param field: The dataclass field being updated.
        :param value: The new value assigned to the field.
        :param old_value: The previous value of the field.
        """
        self.__willow_asdict = None
        self.__willow_properties = None
        self.__willow_dirty_fields.add(field.name)

    def asdict(
        self,
        *,
        dict_factory: DictFactory = dict,
        refresh: bool = False,
    ) -> MutableDict:
        """
        Return a dictionary representation of the instance.

        Caches the result for efficiency. Supports forced refresh to recompute
        the dictionary.

        :param dict_factory: Callable used to construct the resulting dictionary.
        :param refresh: If True, recompute the dictionary ignoring the cache.
        :return: Dictionary mapping field names to current values.
        """
        if refresh or self.__willow_asdict is None:
            self.__willow_asdict = asdict(self, dict_factory=dict_factory)

        return self.__willow_asdict

    @property
    def _initialized(
        self,
    ) -> bool:
        """
        Indicates whether the dataclass instance has been fully initialized.

        :return: True if __post_init__ has run.
        """
        return self.__willow_initialized

    @property
    def _fields(
        self,
    ) -> tuple[Field, ...]:
        """
        Return a tuple of dataclass fields for this instance.

        Cached for repeated introspection to avoid recomputation.

        :return: Tuple of dataclasses.Field objects.
        """
        if self.__willow_fields is None:
            self.__willow_fields = fields(self)

        return self.__willow_fields

    @property
    def _dirty_fields(
        self,
    ) -> set[str]:
        """
        Return the set of fields that have been modified since initialization.

        :return: Set of dirty field names.
        """
        return self.__willow_dirty_fields

    @property
    def _field_names(
        self,
    ) -> set[str]:
        """
        Return the set of dataclass field names for this instance.

        Cached for repeated access. Useful for validation and updates.

        :return: Set of field name strings.
        """
        if self.__willow_field_names is None:
            self.__willow_field_names = {f.name for f in self._fields}

        return self.__willow_field_names

    @property
    def _properties(
        self,
    ) -> dict[str, property]:
        """
        Return a dictionary mapping property names to property objects.

        Cached for repeated introspection. Excludes private and dunder attributes.
        """
        if self.__willow_properties is None:
            self.__willow_properties = dict[str, property]()
            for attr in dir(self):
                prop = getattr(type(self), attr, None)

                if isinstance(prop, property):
                    self.__willow_properties[attr] = prop

        return self.__willow_properties

    @property
    def _property_names(
        self,
    ) -> set[str]:
        """
        Return the set of property names for this instance.

        Cached for efficiency.

        :return: Set of property name strings.
        """
        if self.__willow_property_names is None:
            self.__willow_property_names = set(self._properties.keys())

        return self.__willow_property_names

    def _members(
        self,
        include_properties: bool = True,
        include_private: bool = False,
    ) -> dict[str, Member]:
        """
        Return a mapping of member names to Field or property objects.

        Includes fields by default and optionally properties. Can filter private
        members.

        :param include_properties: Include properties if True.
        :param include_private: Include private members if True.
        :return: Dictionary of member names to Field or property objects.
        """
        members: dict[str, Member] = {f.name: f for f in self._fields}

        if include_properties:
            properties = self._properties.copy()

            if not include_private:
                members |= {
                    n: p for n, p in properties.items() if not n.startswith("_")
                }
            else:
                members |= properties

        return members

    def _member_names(
        self,
        include_properties: bool = True,
        include_private: bool = False,
    ) -> set[str]:
        """
        Return a set of member names (fields and optionally properties).

        Can exclude private members.

        :param include_properties: Include properties if True.
        :param include_private: Include private members if True.
        :return: Set of member names.
        """
        member_names: set[str] = self._field_names.copy()

        if include_properties:
            member_names |= self._property_names.copy()

        if not include_private:
            return set(filter(lambda n: n.startswith("_"), member_names))

        return member_names

    @property
    def _willow_validation(
        self,
    ) -> bool:
        """
        Indicates whether field validation is enabled for this instance.

        :return: True if validation is enabled.
        """
        return self.__willow_validation

    @_willow_validation.setter
    def _willow_validation(
        self,
        value: bool,
    ) -> None:
        """
        Enable or disable field validation for this instance.

        :param value: True to enable validation, False to disable.
        """
        self.__willow_validation = value


__all__ = ("WillowMixin",)
