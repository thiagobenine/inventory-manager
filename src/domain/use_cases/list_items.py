from src.domain.ports.inbound.items.dtos import (
    ItemOutputDTO,
    ListItemsOutputDTO,
)
from src.domain.ports.outbound.repositories.item import ItemRepositoryInterface


class ListItemsUseCase:
    def __init__(self, item_repository: ItemRepositoryInterface):
        self.item_repository = item_repository

    def execute(
        self,
    ) -> ListItemsOutputDTO:
        items = self.item_repository.get_all()

        return ListItemsOutputDTO(
            items=[
                ItemOutputDTO(
                    item_name=item.name,
                    inventory_quantity=item.inventory_quantity,
                )
                for item in items
            ]
        )
