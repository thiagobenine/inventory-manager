from typing import Protocol

from bson import ObjectId

from src.domain.entities.order import Order


class OrderRepositoryInterface(Protocol):
    def find_order_by_id(self, order_id: ObjectId) -> None | Order: ...

    def save(self, order: Order) -> None: ...
