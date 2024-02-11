# di_config.py
from injector import Binder, Module, singleton
import yaml
from model.db import DatabaseConfig
from model.purine_group_repository import PurineGroupRepository
from model.purine_repository import PurineRepository
from service.purine_group_service import PurineGroupService
from service.purine_service import PurineService


class AppModule(Module):

    def get_db_path(
        self,
    ):
        with open("./settings.yml", "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
            db_path = config.get("sql").get("db_path", "./data.db")
            if not db_path:
                raise ValueError("Error finding database")
        return db_path

    def configure(self, binder: Binder) -> None:
        db_config = DatabaseConfig(db_path=self.get_db_path())

        binder.bind(DatabaseConfig, to=db_config, scope=singleton)
        binder.bind(PurineRepository, to=PurineRepository, scope=singleton)
        binder.bind(PurineService, to=PurineService, scope=singleton)
        binder.bind(PurineGroupRepository, to=PurineGroupRepository, scope=singleton)
        binder.bind(PurineGroupService, to=PurineGroupService, scope=singleton)
