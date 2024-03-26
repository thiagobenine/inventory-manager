from typing import Protocol
from uuid import UUID

from src.domain.entities.item import Item


class ItemRepositoryInterface(Protocol):
    def find_item_by_name(self, item_name: str) -> Item | None: ...

    def find_items_by_ids(self, items_ids: list[UUID]) -> list[Item]: ...

    def remove_item_by_name(self, item_name: str) -> None: ...

    def save(self, item: Item) -> None: ...
