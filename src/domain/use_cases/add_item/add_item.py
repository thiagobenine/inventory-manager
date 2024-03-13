from uuid import uuid4

from domain.entities.item import Item
from domain.exceptions import ItemAlreadyExistsError
from domain.ports.repositories.item import ItemRepositoryInterface
from domain.use_cases.add_item.dtos import AddItemInputDTO


class AddItemUseCase:
    def __init__(self, item_repository: ItemRepositoryInterface):
        self.item_repository = item_repository

    def execute(self, input_dto: AddItemInputDTO) -> Item:
        existing_item = self.item_repository.find_item_by_name(input_dto.name)
        if existing_item:
            raise ItemAlreadyExistsError(input_dto.name)

        new_item = Item(
            id=uuid4(),
            name=input_dto.name, 
            inventory_quantity=input_dto.inventory_quantity
        )
        self.item_repository.save(new_item)
        return new_item