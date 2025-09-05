from __future__ import annotations

from ._willow import WillowMixin


class Hashable(WillowMixin):
    """
    Mixin for dataclasses that provides a hash implementation based on field values.

    Allows instances to be used in sets and as dictionary keys.
    """

    def __hash__(
        self,
    ) -> int:
        """
        Compute a hash value for the instance.

        The hash is computed from the tuple of the instance's field values.

        :return: Integer hash of the instance.
        """
        return hash(tuple(self._asdict().values()))


__all__ = ("Hashable",)
