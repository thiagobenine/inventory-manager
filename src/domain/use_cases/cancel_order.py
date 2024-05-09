from datetime import datetime

from src.domain.exceptions import OrderNotFoundError
from src.domain.ports.inbound.orders.dtos import (
    CancelOrderInputDTO,
    CancelOrderItemOutputDTO,
    CancelOrderOutputDTO,
)
from src.domain.ports.outbound.repositories.item import ItemRepositoryInterface
from src.domain.ports.outbound.repositories.order import (
    OrderRepositoryInterface,
)


class CancelOrderUseCase:
    def __init__(
        self,
        order_repository: OrderRepositoryInterface,
        item_repository: ItemRepositoryInterface,
    ):
        self.order_repository = order_repository
        self.item_repository = item_repository

    def execute(self, input_dto: CancelOrderInputDTO) -> CancelOrderOutputDTO:
        order = self.order_repository.find_order_by_id(input_dto.order_id)
        if not order:
            raise OrderNotFoundError(input_dto.order_id)

        items_to_save = []
        for order_item in order.order_items:
            item = order_item.item
            item.increase_inventory_quantity(order_item.quantity)
            items_to_save.append(item)
        self.item_repository.save_all(items_to_save)

        order.cancel()
        self.order_repository.save(order)

        order_items_output_dtos = []
        for order_item in order.order_items:
            order_items_output_dtos.append(
                CancelOrderItemOutputDTO(
                    item_name=order_item.item.name,
                    quantity=order_item.quantity,
                    inventory_quantity=order_item.item.inventory_quantity,
                )
            )

        return CancelOrderOutputDTO(
            order_id=order.id,
            client_name=order.client.name,
            external_order_id=order.external_id,
            is_cancelled=order.is_cancelled,
            created_at=datetime.strftime(
                order.created_at, "%Y-%m-%dT%H:%M:%S"
            ),
            updated_at=datetime.strftime(
                order.updated_at, "%Y-%m-%dT%H:%M:%S"
            ),
            order_items=order_items_output_dtos,
        )
