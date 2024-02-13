"""Purine repository"""

import sqlite3
from dataclasses import dataclass
from uuid import UUID, uuid4

from loguru import logger

from model.db import DatabaseConfig, open_db
from model.repository import Repository


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
    def __init__(self, db_config: DatabaseConfig):
        self.db_config = db_config

    def find_all(self, filter_params: PurineFilter | None) -> list[PurineEntity]:
        with open_db(self.db_config) as cursor:
            sql = "SELECT * FROM purine p "
            params = []
            conditions = []
            if filter_params and filter_params.query:
                conditions.append("p.name LIKE '%' || ? || '%'")
                params.append(filter_params.query)
            if filter_params and filter_params.group_uuid:
                conditions.append("p.purine_group_uuid = ?")
                params.append(filter_params.group_uuid)
            if filter_params and filter_params.show_high:
                conditions.append("p.value > 100")

            if conditions:
                sql += "WHERE " + " AND ".join(conditions)

            cursor.execute(sql, tuple(params))
            results = cursor.fetchall()

            return [PurineEntity(each) for each in results]

    def find(self, uuid: str) -> PurineEntity | None:
        with open_db(self.db_config) as cursor:
            query = "SELECT * FROM purine WHERE uuid = ?"
            cursor.execute(query, (str(uuid),))
            result = cursor.fetchone()
            return PurineEntity(result)

    def add(self, entity: PurineEntity):
        with open_db(self.db_config) as cursor:
            try:
                query = "INSERT into purine(uuid, name, value, purine_group_uuid) VALUES (?,?,?,?)"
                cursor.execute(
                    query,
                    (
                        str(uuid4()),
                        *entity,
                    ),
                )
            except sqlite3.DatabaseError as e:
                logger.error(f"Failed to created an entity: {e}")

    def delete(self, uuid: str) -> bool:
        with open_db(self.db_config) as cursor:
            try:
                sql = "DELETE FROM purine WHERE uuid = ?"
                cursor.execute(sql, (uuid,))
                return True
            except sqlite3.DatabaseError as e:
                logger.error(f"Failed to delete product: {uuid}", e)
                return False
