""" Initialize dev db"""

import json

from di.providers import Providers
from model.db import DatabaseConfig, open_db

SQL_INIT = """
            DROP TABLE IF EXISTS purine_group;
                        DROP TABLE IF EXISTS purine;
                        CREATE TABLE purine_group (
                            uuid TEXT PRIMARY KEY,
                            name TEXT NOT NULL
                        );
                        CREATE TABLE purine (
                                    uuid TEXT PRIMARY KEY,
                                    name TEXT NOT NULL,
                                    value INTEGER NOT NULL,
                                    purine_group_uuid TEXT NOT NULL,
                                    FOREIGN KEY (purine_group_uuid) REFERENCES "purine_group" (uuid)
                                );
"""


class DbInitialization:
    def __init__(self, db_config: DatabaseConfig) -> None:
        self.db_config = db_config

    def initialize_db(self) -> None:
        with open_db(self.db_config) as db:
            db.executescript(SQL_INIT)

    def populate_mock_data(self):
        with open("./db_mock.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        with open_db(self.db_config) as cursor:
            sql_group = "INSERT INTO purine_group (uuid, name) VALUES (?,?)"
            sql_purine = """INSERT INTO purine
                        (uuid, name, value, purine_group_uuid) VALUES (?,?,?,?)"""
            cursor.executemany(sql_group, data.get("purine_group"))
            cursor.executemany(sql_purine, data.get("purine"))

    def initilize_and_populate_data(self):
        self.initialize_db()
        self.populate_mock_data()


def drop_and_initilize_database():
    db_config = Providers.get_db_config()
    if db_config.db_drop:
        DbInitialization(db_config).initilize_and_populate_data()
