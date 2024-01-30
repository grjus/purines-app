from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Generic
from uuid import UUID

from model.db import open_db

T = TypeVar("T")


@dataclass
class Purine:
    uuid: UUID
    name: str
    value: int


class Repository(Generic[T], ABC):
    @abstractmethod
    def find_all(self) -> list[T]:
        pass

    @abstractmethod
    def find(self, uuid: UUID) -> T | None:
        pass

    @abstractmethod
    def find_all_matching_query(self, query: str) -> T:
        pass


class PurineEntity(tuple):
    def to_dto(self) -> Purine:
        if len(self) != 3:
            raise ValueError("Invalid sql result")
        return Purine(UUID(self[0]), self[1], self[2])


class PurinesRepository(Repository[PurineEntity]):
    def find_all_matching_query(self, query: str) -> list[PurineEntity]:
        if not query:
            return self.find_all()
        with open_db() as cursor:
            sql = "SELECT * FROM purines p WHERE p.name LIKE '%' || ? || '%'"
            cursor.execute(sql, (query,))
            results: list[PurineEntity] = cursor.fetchall()
            return results

    def find(self, uuid: UUID) -> PurineEntity | None:
        with open_db() as cursor:
            query = "SELECT * FROM purines WHERE uuid = ?"
            cursor.execute(query, (uuid.__str__(),))
            result: PurineEntity = cursor.fetchone()
            return result

    def find_all(self) -> list[PurineEntity]:
        with open_db("../data.db") as cursor:
            query = "SELECT * FROM purines"
            result = cursor.execute(query).fetchall()
            return result
