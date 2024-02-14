""" Dependency Injection for FastApi"""

import yaml
from fastapi import Depends

from model.db import DatabaseConfig
from model.purine_group_repository import PurineGroupRepository
from model.purine_repository import PurineRepository
from model.repository import Repository
from service.purine_group_service import PurineGroupService
from service.purine_service import PurineService


class Providers:
    @staticmethod
    def get_db_config() -> DatabaseConfig:
        with open("./settings.yml", "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
            db_path = config.get("sql").get("db_path")
            db_drop = config.get("sql").get("drop_db")
            return DatabaseConfig(db_path=db_path, db_drop=db_drop)

    @staticmethod
    def get_purine_repository(
        db_conf: DatabaseConfig = Depends(get_db_config),
    ) -> Repository:
        return PurineRepository(db_conf)

    @staticmethod
    def get_purine_service(
        repository: PurineRepository = Depends(get_purine_repository),
    ) -> PurineService:
        return PurineService(repository)

    @staticmethod
    def get_group_repository(
        db_conf: DatabaseConfig = Depends(get_db_config),
    ) -> Repository:
        return PurineGroupRepository(db_conf)

    @staticmethod
    def get_group_service(
        repository: PurineGroupRepository = Depends(get_group_repository),
    ) -> PurineGroupService:
        return PurineGroupService(repository)
