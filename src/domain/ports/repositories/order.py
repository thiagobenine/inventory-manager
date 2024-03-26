from typing import Protocol

from src.domain.entities.order import Order


class OrderRepositoryInterface(Protocol):
    def save(self, order: Order) -> None: ...
