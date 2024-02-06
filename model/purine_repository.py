"""Purine repository"""

from dataclasses import dataclass

from uuid import UUID, uuid4
from model.db import open_db

from model.repository import Repository
from loguru import logger


@dataclass
class Purine:
    uuid: UUID
    name: str
    value: int


@dataclass
class PurineFilter:
    query: str | None
    group_uuid: str | None
    show_high: bool | None


class PurineEntity(tuple):

    def to_dto(self) -> Purine:
        if len(self) != 4:
            raise ValueError("Invalid sql result")
        return Purine(UUID(self[0]), self[1], self[2])


class PurineRepository(Repository[PurineEntity]):

    def find_all_matching_filter(self, filt: PurineFilter) -> list[PurineEntity]:
        with open_db(self.db_path) as cursor:
            sql = "SELECT * FROM purine p "
            params = []
            conditions = []
            if filt.query:
                conditions.append("p.name LIKE '%' || ? || '%'")
                params.append(filt.query)
            if filt.group_uuid:
                conditions.append("p.purine_group_uuid = ?")
                params.append(filt.group_uuid)
            if filt.show_high:
                conditions.append("p.value > 100")

            if conditions:
                sql += "WHERE " + " AND ".join(conditions)

            cursor.execute(sql, tuple(params))
            results = cursor.fetchall()

            return [PurineEntity(each) for each in results]

    def find(self, uuid: UUID) -> PurineEntity | None:
        with open_db(self.db_path) as cursor:
            query = "SELECT * FROM purines WHERE uuid = ?"
            cursor.execute(query, (str(uuid),))
            result = cursor.fetchone()
            return PurineEntity(result)

    def find_all(self) -> list[PurineEntity]:
        with open_db(self.db_path) as cursor:
            query = "SELECT * FROM purine"
            results = cursor.execute(query).fetchall()
            return [PurineEntity(each) for each in results]

    def add_product(self, name: str, value: int, group_uuid: str):
        with open_db(self.db_path) as cursor:
            try:
                query = "INSERT into purine(uuid, name, value, purine_group_uuid) VALUES (?,?,?,?)"
                cursor.execute(
                    query,
                    (
                        str(uuid4()),
                        name,
                        value,
                        group_uuid,
                    ),
                )
            except Exception as e:
                logger.error(f"Failed to created an entity: {e}")