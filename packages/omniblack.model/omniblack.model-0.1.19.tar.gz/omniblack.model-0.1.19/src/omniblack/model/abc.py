from abc import ABC, abstractmethod
from collections.abc import Mapping

from public import public


@public
class Localizable(ABC):
    @abstractmethod
    def localize(lang: str) -> str:
        pass


# Strings are considered localizeable so that double localization does not
# cause errors
Localizable.register(str)


@public
class Registry(Mapping):
    def __init__(self, model):
        self.model = model
        cls_name = self.__class__.__name__
        setattr(self, f'_{cls_name}__model', model)
        self._data = {}

    def _add(self, name, item):
        self._data[name] = item
        return item

    def __getitem__(self, key):
        return self._data[key]

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as err:
            raise AttributeError(*err.args) from None

    def __repr__(self):
        cls_name = self.__class__.__name__
        data_repr = ', '.join(self.keys())
        return f'{cls_name}({data_repr})'

    def __rich_repr__(self):
        for key in self.keys():
            yield key

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __contains__(self, key):
        return key in self._data

    def __reversed__(self):
        return reversed(self._data)

    def __bool__(self):
        return bool(self._data)

    def keys(self):
        return self._data.keys()

    def items(self):
        return self._data.items()

    def values(self):
        return self._data.values()

    def get(self, key, default=None):
        return self._data.get(key, default)
