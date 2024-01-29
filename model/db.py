import logging
import sqlite3
from contextlib import contextmanager


@contextmanager
def open_db(db_path: str) -> sqlite3.Cursor:
    connection = sqlite3.connect(db_path)
    try:
        cursor = connection.cursor()
        yield cursor
    except sqlite3.DatabaseError as error:
        logging.error(error)
    finally:
        connection.commit()
        connection.close()


def initialize_db(db_path: str) -> None:
    with open_db(db_path) as db:
        sql = """
        CREATE TABLE IF NOT EXISTS purines (
        uuid TEXT,
        name TEXT,
        value INT
        )
        """
        db.execute(sql)
