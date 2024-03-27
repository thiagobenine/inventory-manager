from typing import Protocol
from uuid import UUID

from src.domain.entities.order import Order


class OrderRepositoryInterface(Protocol):
    def find_order_by_id(self, order_id: UUID) -> Order: ...

    def save(self, order: Order) -> None: ...
