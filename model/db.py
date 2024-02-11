import logging
import sqlite3
from contextlib import contextmanager
from typing import Generator, Any


class DatabaseConfig:
    def __init__(self, db_path: str):
        self.__db_path = db_path

    def get_db_path(self) -> str:
        return self.__db_path


@contextmanager
def open_db(config: DatabaseConfig) -> Generator[sqlite3.Cursor, Any, Any]:
    connection = sqlite3.connect(config.get_db_path())
    try:
        cursor = connection.cursor()
        yield cursor
    except sqlite3.DatabaseError as error:
        logging.error(error)
    finally:
        connection.commit()
        connection.close()
