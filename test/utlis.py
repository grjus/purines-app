""" Test db initilizer"""

import sqlite3
from uuid import uuid4

from model.db import DatabaseConfig
from model.db_init import SQL_INIT
from model.purine_group_repository import PurineGroupEntity
from model.purine_repository import PurineEntity


def create_purine_group(name: str) -> PurineGroupEntity:
    return PurineGroupEntity(str(uuid4()), name)


def create_purine(name: str, value: int, group_uuid: str):
    return PurineEntity(str(uuid4()), name, value, group_uuid)


class InMemoryDb:
    config = DatabaseConfig(db_path="file::memory:?cache=shared", db_drop=True)
    group_uuid, group_name = (str(uuid4()), "TEST-GROUP")

    def __init__(self) -> None:
        self.connection = sqlite3.connect(self.config.db_path)
        self.cursor = self.connection.cursor()

    def init(self):
        self.cursor.executescript(SQL_INIT)
        self.connection.commit()

    def insert_mock_data(self) -> None:
        group_1 = create_purine_group("TEST-GROUP-1")
        group_2 = create_purine_group("TEST-GROUP-2")
        purine_1 = create_purine("Bacon", 23, group_1.uuid)
        purine_2 = create_purine("Salad", 33, group_1.uuid)
        purine_3 = create_purine("Mellon", 12, group_2.uuid)
        purine_4 = create_purine("Some name", 120, group_2.uuid)
        sql_group = "INSERT INTO purine_group (uuid, name) VALUES (?,?)"
        sql_purine = """INSERT INTO purine
                        (uuid, name, value, purine_group_uuid) VALUES (?,?,?,?)"""

        groups = (
            tuple(group_1.model_dump().values()),
            tuple(group_2.model_dump().values()),
        )
        purines = (
            tuple(purine_1.model_dump().values()),
            tuple(purine_2.model_dump().values()),
            tuple(purine_3.model_dump().values()),
            tuple(purine_4.model_dump().values()),
        )
        self.cursor.executemany(sql_group, groups)
        self.cursor.executemany(
            sql_purine,
            purines,
        )
        self.connection.commit()
        self.cursor.close()
