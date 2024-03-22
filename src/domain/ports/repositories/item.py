from typing import Protocol
from uuid import UUID

from src.domain.entities.item import Item


class ItemRepositoryInterface(Protocol):
    def find_item_by_name(self, item_name: str) -> Item | None: ...

    def find_item_by_id(self, item_id: UUID) -> Item | None: ...

    def remove_item_by_name(self, item_name: str) -> None: ...

    def save(self, item: Item) -> None: ...
