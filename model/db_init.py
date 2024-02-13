from fastapi import Depends
from di.providers import Providers
from model.db import DatabaseConfig, open_db
import json


class DbInitialization:
    def __init__(self, db_config: DatabaseConfig) -> None:
        self.db_config = db_config

    def __initialize_db(self) -> None:
        with open_db(self.db_config) as db:
            sql = """
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
            db.executescript(sql)

    def __populate_mock_data(self):
        with open("./db_mock.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        with open_db(self.db_config) as cursor:
            sql_group = "INSERT INTO purine_group (uuid, name) VALUES (?,?)"
            sql_purine = "INSERT INTO purine (uuid, name, value, purine_group_uuid) VALUES (?,?,?,?)"
            cursor.executemany(sql_group, data.get("purine_group"))
            cursor.executemany(sql_purine, data.get("purine"))

    def init(self):
        self.__initialize_db()
        self.__populate_mock_data()


def drop_and_initilize_database():
    db_config = Providers.get_db_config()
    if db_config.db_drop:
        DbInitialization(db_config).init()
