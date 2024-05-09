from datetime import datetime
from zoneinfo import ZoneInfo

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
        now = datetime.now(ZoneInfo("America/Sao_Paulo"))
        return Order(
            external_id=input_dto.external_order_id,
            external_created_at=input_dto.external_created_at,
            created_at=now,
            updated_at=now,
            is_cancelled=False,
            client=client,
            order_items=order_items,
        )
