# di_config.py
from injector import Binder, Module, singleton
from model.db import DatabaseConfig
from model.purine_group_repository import PurineGroupRepository
from model.purine_repository import PurineRepository
from service.purine_group_service import PurineGroupService
from service.purine_service import PurineService


class AppModule(Module):
    def configure(self, binder: Binder) -> None:
        db_config = DatabaseConfig(db_path="path/to/your/database")

        binder.bind(DatabaseConfig, to=db_config, scope=singleton)
        binder.bind(PurineRepository, to=PurineRepository, scope=singleton)
        binder.bind(PurineService, to=PurineService, scope=singleton)
        binder.bind(PurineGroupRepository, to=PurineGroupRepository, scope=singleton)
        binder.bind(PurineGroupService, to=PurineGroupService, scope=singleton)
