""" Purine group repository """

from dataclasses import dataclass
from uuid import UUID

from model.db import open_db

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
    """Purine group repository"""

    def find_all(self) -> list[PurineGroupEntity]:
        with open_db(self.db_path) as cursor:
            query = "SELECT * FROM purine_group"
            result = cursor.execute(query).fetchall()
            return [PurineGroupEntity(each) for each in result]

    def find(self, uuid: UUID) -> PurineGroupEntity | None:
        with open_db(self.db_path) as cursor:
            query = "SELECT * from purine_group where uuid = (?)"
            result = cursor.execute(query, (str(uuid),)).fetchone()
            return PurineGroupEntity(result)
