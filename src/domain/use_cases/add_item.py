from src.domain.entities.item import Item
from src.domain.exceptions import ItemAlreadyExistsError
from src.domain.ports.inbound.items.dtos import (
    AddItemInputDTO,
    AddItemOutputDTO,
)
from src.domain.ports.outbound.repositories.item import ItemRepositoryInterface


class AddItemUseCase:
    def __init__(self, item_repository: ItemRepositoryInterface):
        self.item_repository = item_repository

    def execute(self, input_dto: AddItemInputDTO) -> AddItemOutputDTO:
        existing_item = self.item_repository.find_item_by_name(input_dto.name)
        if existing_item:
            raise ItemAlreadyExistsError(input_dto.name)

        new_item = Item(
            name=input_dto.name,
            inventory_quantity=input_dto.inventory_quantity,
        )
        self.item_repository.save(new_item)

        return AddItemOutputDTO(
            name=new_item.name, inventory_quantity=new_item.inventory_quantity
        )
