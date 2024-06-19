from src.domain.entities.item import Item
from src.domain.exceptions import ItemsNotFoundByNameError
from src.domain.ports.inbound.items.dtos import (
    SetInventoryQuantitiesInputDTO,
    SetInventoryQuantitiesOutputDTO,
    SetInventoryQuantityItemOutputDTO,
)
from src.domain.ports.outbound.repositories.item import ItemRepositoryInterface


class SetInventoryQuantitiesUseCase:
    def __init__(self, item_repository: ItemRepositoryInterface):
        self.item_repository = item_repository

    def execute(
        self, input_dto: SetInventoryQuantitiesInputDTO
    ) -> SetInventoryQuantitiesOutputDTO:
        items_names_from_dto = [
            item_input.item_name for item_input in input_dto.items
        ]
        items_from_repository = self.item_repository.find_items_by_names(
            items_names_from_dto
        )

        self._validate_no_missing_items(
            items_names_from_dto, items_from_repository
        )

        item_map_by_name = {item.name: item for item in items_from_repository}

        for item_input in input_dto.items:
            item = item_map_by_name[item_input.item_name]
            item.set_inventory_quantity(item_input.inventory_quantity)

        self.item_repository.save_all(items_from_repository)

        return SetInventoryQuantitiesOutputDTO(
            items=[
                SetInventoryQuantityItemOutputDTO(
                    item_name=item.name,
                    inventory_quantity=item.inventory_quantity,
                )
                for item in items_from_repository
            ]
        )

    @staticmethod
    def _validate_no_missing_items(
        items_names_from_dto: list[str], items_from_repository: list[Item]
    ):
        is_any_item_missing = len(items_from_repository) != len(
            items_names_from_dto
        )
        if is_any_item_missing:
            found_item_names = {item.name for item in items_from_repository}
            missing_item_names = set(items_names_from_dto) - found_item_names
            raise ItemsNotFoundByNameError(list(missing_item_names))
