from abc import ABC, abstractmethod
from .model import Model
from .struct import StructBase
from public import public


@public
class Storage(ABC):
    _model: Model

    @abstractmethod
    def save(
        self,
        indiv: StructBase,
        *,
        return_saved=False,
        exclusive_creation=False,
        exclusive_update=False,
    ) -> StructBase | None:
        pass

    @abstractmethod
    def read(self, id: str) -> StructBase:
        pass

    @abstractmethod
    def search(self, **params) -> list[StructBase]:
        pass

    @abstractmethod
    def delete(self, id) -> bool:
        pass
