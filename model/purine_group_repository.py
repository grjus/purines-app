""" Purine group repository """

from dataclasses import dataclass

from pydantic import BaseModel

from model.db import DatabaseConfig, open_db
from model.repository import Repository


@dataclass
class PurineGroup:
    uuid: str
    name: str


class PurineGroupEntity(BaseModel):
    uuid: str
    name: str

    def __init__(self, *args):
        fields = ["uuid", "name"]
        super().__init__(**dict(zip(fields, args)))

    def to_dto(self) -> PurineGroup:
        return PurineGroup(self.uuid, self.name)


class PurineGroupRepository(Repository[PurineGroupEntity]):
    def __init__(self, db_config: DatabaseConfig) -> None:
        self.db_config = db_config

    def find_all(self, _=None) -> list[PurineGroupEntity]:
        with open_db(self.db_config) as cursor:
            query = "SELECT * FROM purine_group"
            result = cursor.execute(query).fetchall()
            return [PurineGroupEntity(*each) for each in result]

    def find(self, uuid: str) -> PurineGroupEntity | None:
        with open_db(self.db_config) as cursor:
            query = "SELECT * from purine_group where uuid = (?)"
            result = cursor.execute(query, (uuid,)).fetchone()
            return PurineGroupEntity(*result)

    def add(self, _: PurineGroupEntity):
        raise NotImplementedError("Not implemented")

    def delete(self, _: str) -> bool:
        raise NotImplementedError("Not implemented")
