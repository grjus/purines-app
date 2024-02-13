""" Database setup"""

import logging
import sqlite3
from contextlib import contextmanager
from typing import Any, Generator


class DatabaseConfig:
    def __init__(self, db_path: str, db_drop: bool = False):
        self._db_path = db_path
        self._db_drop = db_drop

    @property
    def db_path(self) -> str:
        if not self._db_drop:
            raise ValueError("Database source path not defined")
        return self._db_path

    @property
    def db_drop(self) -> bool:
        return self._db_drop


@contextmanager
def open_db(config: DatabaseConfig) -> Generator[sqlite3.Cursor, Any, Any]:
    connection = sqlite3.connect(config.db_path)
    try:
        cursor = connection.cursor()
        yield cursor
    except sqlite3.DatabaseError as error:
        logging.error(error)
    finally:
        connection.commit()
        connection.close()
