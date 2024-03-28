from datetime import datetime

from src.domain.entities.client import Client
from src.domain.entities.order import Order, OrderItem
from src.domain.ports.inbound.orders.dtos import CreateOrderInputDTO


class OrderFactory:
    @staticmethod
    def build(
        input_dto: CreateOrderInputDTO,
        client: Client,
        order_items: list[OrderItem],
    ) -> Order:
        return Order(
            external_id=input_dto.external_order_id,
            created_at=datetime.strptime(
                input_dto.created_at, "%Y-%m-%dT%H:%M:%S"
            ),
            updated_at=datetime.strptime(
                input_dto.created_at, "%Y-%m-%dT%H:%M:%S"
            ),
            is_cancelled=False,
            client=client,
            items=order_items,
        )
