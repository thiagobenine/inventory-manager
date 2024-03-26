from domain.entities.item import Item
from domain.exceptions import ItemNotFoundError
from domain.ports.repositories.item import ItemRepositoryInterface
from domain.use_cases.remove_item.dtos import RemoveItemInputDTO, RemoveItemOutputDTO


class RemoveItemUseCase:
    def __init__(self, item_repository: ItemRepositoryInterface):
        self.item_repository = item_repository

    def execute(self, input_dto: RemoveItemInputDTO) -> Item:
        existing_item = self.item_repository.find_item_by_name(input_dto.name)
        if not existing_item:
            raise ItemNotFoundError(input_dto.name)
        
        self.item_repository.remove_item_by_name(existing_item.name)
        return RemoveItemOutputDTO(
            name=existing_item.name, 
        )