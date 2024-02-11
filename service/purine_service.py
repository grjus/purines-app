""" Purine service"""

from model.purine_repository import Purine, PurineEntity, PurineFilter
from model.repository import Repository


class PurineService:
    def __init__(self, repository: Repository):
        self.repository = repository

    def get_all_purines(self) -> list[Purine]:
        result = self.repository.find_all(filter_params=None)
        return [each.to_dto() for each in result]

    def get_all_purines_matching_query(
        self, filter_params: PurineFilter
    ) -> list[Purine]:
        result = self.repository.find_all(filter_params)
        return [each.to_dto() for each in result]

    def add_product(self, name: str, value: int, group_uuid: str) -> bool:
        entity = PurineEntity((name, value, group_uuid))
        self.repository.add(entity)
        return True

    def delete_product(self, uuid: str) -> None:
        product = self.repository.find(uuid)
        if product is None:
            raise ValueError(f"Purine with id: {uuid} does not exists")
        self.repository.delete(uuid)
