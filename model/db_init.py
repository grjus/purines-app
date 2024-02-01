from model.db import open_db
from uuid import uuid4


class DbInitialization:
    def __init__(self, db_path: str, drop_db: bool) -> None:
        self.db_path = db_path
        self.drop_db = drop_db

    def initialize_db(self) -> None:
        with open_db(self.db_path) as db:
            if self.drop_db:
                sql_drop = "DROP TABLE IF EXISTS purines"
                db.execute(sql_drop)
            sql = """
            CREATE TABLE IF NOT EXISTS purines (
            uuid TEXT,
            name TEXT,
            value INT
            )
            """
            db.execute(sql)
            return self

    def check_if_empty_table(self) -> bool:
        with open_db(self.db_path) as cursor:
            sql = "SELECT COUNT(*) from purines"
            count = cursor.execute(sql).fetchone()
            if count[0] == 0:
                return True
            return False

    def populate_mock_data(self):
        if self.check_if_empty_table():
            data = [
                ["Bacon", 96],
                ["Frankfurters", 89],
                ["Veal, brain", 460],
                ["White sausage", 73],
                ["Fried sausage", 91],
                ["Horse meat", 200],
                ["Luncheon meat", 70],
                ["Salami", 103],
                ["Pork, ears", 136],
                ["Pork, ham", 160],
                ["Beef, sirloin", 120],
                ["Beef, brisket", 90],
                ["Mackerel", 145],
            ]
            db_content = []
            for each in data:
                each.insert(0, uuid4().__str__())
                db_content.append(each)
            with open_db(self.db_path) as cursor:
                sql = "INSERT INTO purines (uuid, name, value) VALUES (?,?,?)"
                cursor.executemany(sql, db_content)
