from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, MutableMapping
from itertools import chain
from typing import Any

from public import public

NOT_FOUND = object()


@public
class DotPath(tuple):
    """
    A path into a structure.
    """

    def startsWith(self, otherPath):
        """
        Does :code:`self` start with :code:`otherPath`?
        Similar to :type:`str.startswith`.
        """
        if len(self) < len(otherPath):
            return False

        for seg, otherSeg in zip(self, otherPath):
            if seg != otherSeg:
                return False

        return True

    def set(self, target, value):
        """
        Set the mapping at :code:`self` in :code:`target` to :code:`value`.

        .. note::
            This will create intermeditate mappings under :code:`target`
            if they are missing.

        .. note::
            :code:`target` must be :type:`collections.abc.MutableMapping`
            that can be constructed by being called with no arguments.
        """
        return self.merge(target, lambda current_value: value)

    def merge(self, target, merge_func):
        """
        Merge a value into :code:`target`.

        :code:`merge_func` will be called with the current value of
        :code:`self` under :code:`target` and will be replaced
        with the return value of :code:`merge_func`.

        .. note::
            This will create intermeditate mappings under :code:`target`
            if they are missing.

        .. note::
            :code:`target` must be :type:`collections.abc.MutableMapping`
            that can be constructed by being called with no arguments.
        """
        mapping_type = type(target)
        current = target
        for seg in self[:-1]:
            current.setdefault(seg, mapping_type())
            current = current[seg]

        last = self[-1]
        current_value = current.get(last, None)
        current[last] = merge_func(current_value)
        return target

    @classmethod
    def from_string(cls, pathStr):
        """Create a dotpath from :code:`pathStr`."""
        return cls(pathStr.split('.'))

    def __str__(self):
        return '.'.join(map(lambda seg: str(seg), self))

    def __repr__(self):
        repr_segments = (repr(seg) for seg in self)
        cls_name = self.__class__.__name__
        return f'{cls_name}({", ".join(repr_segments)})'

    def get(self, target: Mapping, default: Any = None):
        current = target
        for seg in self:
            if not isinstance(current, Mapping):
                return default
            else:
                current = current.get(seg, NOT_FOUND)
                if current is NOT_FOUND:
                    return default

        return current

    def __or__(self, other):
        """
        Merge `self` and `other` into a new :type:`DotPath`.
        """
        is_str = isinstance(other, str)
        if isinstance(other, Iterable) and not is_str:
            return self.__class__(chain(self,  other))
        else:
            return self.__class__(chain(self, (other, )))


if __name__ == '__main__':
    import code
    code.interact(local=globals())
