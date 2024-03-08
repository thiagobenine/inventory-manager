from datetime import datetime
from uuid import uuid4

from domain.entities.client import Client
from domain.entities.item import Item
from domain.entities.order import Order, OrderItem
from domain.use_cases.create_order.dtos import CreateOrderInputDTO, OrderItemInputDTO


class OrderFactory:
    @staticmethod
    def build(
        input_dto: CreateOrderInputDTO, client: Client, order_items: list[OrderItem]
    ) -> Order:
        return Order(
            id=uuid4(),
            external_id=input_dto.external_order_id,
            created_at=datetime.strptime(input_dto.created_at, "%Y-%m-%dT%H:%M:%S"),
            updated_at=datetime.strptime(input_dto.created_at, "%Y-%m-%dT%H:%M:%S"),
            is_cancelled=False,
            client=client,
            items=order_items,
        )
