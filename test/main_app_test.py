# pylint: disable=no-member
""" Main app test """

from test.utlis import InMemoryDb

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


@pytest.fixture(autouse=True)
def db_setup():
    test_db = InMemoryDb()
    test_db.init()
    test_db.insert_mock_data()
    yield
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


# pylint: disable=no-member
def test_should_show_filtered_purines_on_request():
    response = client.get(
        "/",
        headers={"hx-request": "hx-request"},
        params={"show-high": "True"},
    )
    assert response.template.name == "purines-rows.html"
    assert len(response.context.get("purines")) == 1
    assert response.context.get("purines")[0].value == 120
