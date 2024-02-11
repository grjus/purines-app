""" Purine group repository """

from dataclasses import dataclass
from uuid import UUID

from model.db import DatabaseConfig, open_db

from model.repository import Repository


@dataclass
class PurineGroup:
    uuid: UUID
    name: str


class PurineGroupEntity(tuple):
    uuid: str
    name: str

    def to_dto(self) -> PurineGroup:
        if len(self) != 2:
            raise ValueError("Invalid sql result")
        return PurineGroup(UUID(self[0]), self[1])


class PurineGroupRepository(Repository[PurineGroupEntity]):

    def __init__(self, db_config: DatabaseConfig) -> None:
        self.db_config = db_config

    def find_all(self, _: None) -> list[PurineGroupEntity]:
        with open_db(self.db_config) as cursor:
            query = "SELECT * FROM purine_group"
            result = cursor.execute(query).fetchall()
            return [PurineGroupEntity(each) for each in result]

    def find(self, uuid: str) -> PurineGroupEntity | None:
        with open_db(self.db_config) as cursor:
            query = "SELECT * from purine_group where uuid = (?)"
            result = cursor.execute(query, (uuid,)).fetchone()
            return PurineGroupEntity(result)

    def add(self, _: PurineGroupEntity):
        raise ValueError("Not implemented yet")

    def delete(self, _: str) -> bool:
        raise ValueError("Not implemented")
