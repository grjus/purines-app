""" Repository abtract class"""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class Repository(Generic[T], ABC):

    @abstractmethod
    def find_all(self, filter_params: Any) -> list[T]:
        pass

    @abstractmethod
    def find(self, uuid: str) -> T | None:
        pass

    @abstractmethod
    def add(self, entity: T) -> T:
        pass

    @abstractmethod
    def delete(self, uuid: str) -> bool:
        pass
