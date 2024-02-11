""" Create test db"""

import pytest

from model.db import open_db


@pytest.fixture(scope="session")
def initilize_db():
    db_path = "./test_db.db"
    with open_db("./test_db.db") as db:
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
        return db_path
