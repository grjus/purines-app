""" Purine service"""

from model.purine_repository import Purine, PurineFilter, PurineRepository


class PurineService:
    def __init__(
        self,
    ):
        self.repository = PurineRepository()

    def get_all_purines(self) -> list[Purine]:
        result = self.repository.find_all()
        return [each.to_dto() for each in result]

    def get_all_purines_matching_query(self, filt: PurineFilter) -> list[Purine]:
        result = self.repository.find_all_matching_filter(filt)
        return [each.to_dto() for each in result]
