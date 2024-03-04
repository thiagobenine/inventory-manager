from typing import Protocol

from domain.entities.item import Item


class ItemRepositoryInterface(Protocol):
    def find_item_by_name(self, item_name: str) -> Item:
        ...

    def update_inventory(self, item_name: str, new_quantity: int) -> None:
        ...

