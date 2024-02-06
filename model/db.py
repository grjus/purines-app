import logging
import sqlite3
from contextlib import contextmanager
from typing import Generator, Any


@contextmanager
def open_db(db_path: str) -> Generator[sqlite3.Cursor, Any, Any]:
    connection = sqlite3.connect(db_path)
    try:
        cursor = connection.cursor()
        yield cursor
    except sqlite3.DatabaseError as error:
        logging.error(error)
    finally:
        connection.commit()
        connection.close()
