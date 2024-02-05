""" Repository abtract class"""

from abc import ABC, abstractmethod

from typing import TypeVar, Generic
from uuid import UUID

import yaml


T = TypeVar("T")


class Repository(Generic[T], ABC):

    def __init__(self):
        with open("./settings.yml", "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
            db_path = config.get("sql").get("db_path")
            if not db_path:
                raise ValueError("Error finding database")
            self.db_path: str = db_path

    @abstractmethod
    def find_all(self) -> list[T]:
        pass

    @abstractmethod
    def find(self, uuid: UUID) -> T | None:
        pass
