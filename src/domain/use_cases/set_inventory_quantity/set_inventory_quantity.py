from src.domain.exceptions import ItemNotFoundError
from src.domain.ports.repositories.item import ItemRepositoryInterface
from src.domain.use_cases.set_inventory_quantity.dtos import (
    SetInventoryQuantityInputDTO,
    SetInventoryQuantityOutputDTO,
)


class SetInventoryQuantityUseCase:
    def __init__(self, item_repository: ItemRepositoryInterface):
        self.item_repository = item_repository

    def execute(
        self, input_dto: SetInventoryQuantityInputDTO
    ) -> SetInventoryQuantityOutputDTO:
        item = self.item_repository.find_item_by_name(input_dto.item_name)
        if not item:
            raise ItemNotFoundError(input_dto.item_name)

        item.set_inventory_quantity(input_dto.inventory_quantity)
        self.item_repository.save(item)

        return SetInventoryQuantityOutputDTO(
            item_name=item.name,
            inventory_quantity=item.inventory_quantity,
        )
