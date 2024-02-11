""" Repository abtract class"""

from abc import ABC, abstractmethod

from typing import Any, TypeVar, Generic
from uuid import UUID

import yaml


T = TypeVar("T")
G = TypeVar("G")


class Repository(Generic[T], ABC):

    # def __init__(self):
    #     with open("./settings.yml", "r", encoding="utf-8") as file:
    #         config = yaml.safe_load(file)
    #         db_path = config.get("sql").get("db_path")
    #         if not db_path:
    #             raise ValueError("Error finding database")
    #         self.db_path: str = db_path

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
