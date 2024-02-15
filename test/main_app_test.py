# pylint: disable=no-member
""" Main app test """

from test.utlis import PURINE_GROUP_UUID, PURINE_UUID, InMemoryDb
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from di.providers import Providers
from main import app
from model.purine_group_repository import PurineGroupRepository
from model.purine_repository import PurineRepository
from service.purine_group_service import PurineGroupService
from service.purine_service import PurineService

client = TestClient(app)


def override_purine_service() -> PurineService:
    repository = PurineRepository(InMemoryDb.config)
    return PurineService(repository)


def override_group_service() -> PurineGroupService:
    repository = PurineGroupRepository(InMemoryDb.config)
    return PurineGroupService(repository)


app.dependency_overrides[Providers.get_purine_service] = override_purine_service
app.dependency_overrides[Providers.get_group_service] = override_group_service


@pytest.fixture(name="db", autouse=True)
def db_setup():
    test_db = InMemoryDb()
    test_db.init()
    test_db.insert_mock_data()
    yield test_db
    test_db.connection.close()


def test_health_check():
    response = client.get("/health-check")
    assert response.status_code == 200
    assert response.json() == {"msg": "I am alive"}


def test_should_show_all_purines_on_main_page():
    response = client.get(
        "/",
    )
    assert response.template.name == "index.html"
    assert len(response.context.get("purines")) == 4
    assert len(response.context.get("purine_group")) == 2


def test_should_show_filtered_purines_on_request():
    response = client.get(
        "/",
        headers={"hx-request": "hx-request"},
        params={"show-high": "True"},
    )
    assert response.template.name == "purines-rows.html"
    assert len(response.context.get("purines")) == 1
    assert response.context.get("purines")[0].value == 120


def test_should_add_new_product(db):
    product_name, value, group_uuid = ("MyProduct", 100, PURINE_GROUP_UUID)
    form_data = {"name": product_name, "value": value, "product_group": group_uuid}
    response = client.post("/api/add-product", data=form_data)
    cursor = db.cursor
    sql = "SELECT * from purine where name= ?"
    data = cursor.execute(sql, (product_name,)).fetchone()
    assert response.status_code == 200
    assert product_name == data[1]
    assert response.template.name == "modal/add-product-success.html"


def test_should_fail_with_incorrect_new_product_data():
    product_name, value, group_uuid = ("MyProduct", "invalid", PURINE_GROUP_UUID)
    form_data = {"name": product_name, "value": value, "product_group": group_uuid}
    response = client.post("/api/add-product", data=form_data)
    assert response.status_code == 422
    assert response.template.name == "modal/add-product-error.html"


def test_should_return_modal_content_when_creating_product():
    response = client.get("/template/create-purine-modal")
    assert response.status_code == 200
    assert len(response.context.get("purine_group")) == 2
    assert response.template.name == "modal/create-product-modal.html"


def test_should_return_404_when_deleting_not_existing_product():
    purine_uuid = str(uuid4())
    response = client.post(f"/api/delete-product/{purine_uuid}")
    assert response.status_code == 404


def test_should_delete_and_update_table():
    form_data = {"search": "", "product-group": ""}
    response = client.post(f"/api/delete-product/{PURINE_UUID}", data=form_data)
    assert response.status_code == 200
    assert response.template.name == "purines-rows.html"
    assert len(response.context.get("purines")) == 3
