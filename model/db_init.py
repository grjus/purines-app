from model.db import open_db
from uuid import uuid4
import json


class DbInitialization:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    def __initialize_db(self) -> None:
        with open_db(self.db_path) as db:
            sql = """
            DROP TABLE IF EXISTS purine_group;
            DROP TABLE IF EXISTS purine;
            CREATE TABLE purine_group (
                uuid TEXT PRIMARY KEY,
                name TEXT
            );
            CREATE TABLE purine (
                        uuid TEXT PRIMARY KEY,
                        name TEXT,
                        value INTEGER,
                        purine_group_uuid TEXT,
                        FOREIGN KEY (purine_group_uuid) REFERENCES "purine_group" (uuid)
                    );
            """
            db.executescript(sql)

    def __populate_mock_data(self):
        with open("./db_mock.json", "r") as file:
            data = json.load(file)

        with open_db(self.db_path) as cursor:
            sql_group = "INSERT INTO purine_group (uuid, name) VALUES (?,?)"
            sql_purine = "INSERT INTO purine (uuid, name, value, purine_group_uuid) VALUES (?,?,?,?)"
            cursor.executemany(sql_group, data.get("purine_group"))
            cursor.executemany(sql_purine, data.get("purine"))

    def init(self):
        self.__initialize_db()
        self.__populate_mock_data()
