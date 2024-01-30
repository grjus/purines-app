from model.repository import Repository, Purine, PurinesRepository


class PurineService:
    def __init__(self, repository: Repository):
        self.repository = repository

    def get_all_purines(self) -> list[Purine]:
        result = self.repository.find_all()
        return [each.to_dto() for each in result]


if __name__ == "__main__":
    data = PurineService(PurinesRepository()).get_all_purines()
    print(data)
