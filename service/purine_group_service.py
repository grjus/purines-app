""" Purine service"""

from model.purine_group_repository import PurineGroup
from model.repository import Repository


class PurineGroupService:
    def __init__(self, repository: Repository):
        self.repository = repository

    def get_all_purine_groups(self) -> list[PurineGroup]:
        result = self.repository.find_all(None)
        return [each.to_dto() for each in result]

    def find(self, uuid) -> PurineGroup | None:
        result = self.repository.find(uuid)
        if result:
            return result.to_dto()
        return None
