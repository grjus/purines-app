# test_capitalize.py


import pytest
from uuid import uuid4
from model import db_init
from model.db import open_db
from model.purine_repository import PurineRepository
from service.purine_service import PurineService
from test.db_init import initilize_db


@pytest.fixture(scope="module")
def create_group():
    uuid = str(uuid4())
    db_path = initilize_db()
    with open_db(db_path) as cursor:
        sql = f"INSERT INTO purine_group(uuid, name) VALUES ({uuid},'TEST')"
        cursor.execute(sql)
    return uuid


def test_add_product():
    service = PurineService()
    service.repository = PurineRepository()
    service.repository.db_path = initilize_db()
    service.add_product(name="some name", value=43, group_uuid=create_group())
    assert len(service.get_all_purines()) == 1
