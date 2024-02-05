""" Purine service"""

from model.purine_group_repository import PurineGroup, PurineGroupRepository


class PurineGroupService:
    def __init__(
        self,
    ):
        self.repository = PurineGroupRepository()

    def get_all_purine_groups(self) -> list[PurineGroup]:
        result = self.repository.find_all()
        return [each.to_dto() for each in result]
