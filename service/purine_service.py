from model.repository import Repository, Purine


class PurineService:
    def __init__(self, repository: Repository):
        self.repository = repository

    def get_all_purines(self) -> list[Purine]:
        result = self.repository.find_all()
        return [each.to_dto() for each in result]

    def get_all_purines_matching_query(self, query) -> list[Purine]:
        result = self.repository.find_all_matching_query(query)
        return [each.to_dto() for each in result]
