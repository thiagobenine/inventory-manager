from typing import Protocol

from domain.entities.item import Item


class ItemRepositoryInterface(Protocol):
    def find_item_by_name(self, item_name: str) -> Item:
        ...

    def save(self, item: Item) -> None:
        ...

