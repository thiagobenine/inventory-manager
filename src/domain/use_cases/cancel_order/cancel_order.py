from datetime import datetime

from src.domain.exceptions import ItemNotFoundByIdError, OrderNotFoundError
from src.domain.ports.repositories.item import ItemRepositoryInterface
from src.domain.ports.repositories.order import OrderRepositoryInterface
from src.domain.use_cases.cancel_order.dtos import (
    CancelOrderInputDTO,
    CancelOrderOutputDTO,
    OrderItemOutputDTO,
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

        order_items = []
        for order_item in order.items:
            item = self.item_repository.find_item_by_id(order_item.item_id)
            if not item:
                raise ItemNotFoundByIdError(order_item.item_id)

            order_items.append(
                OrderItemOutputDTO(
                    item_name=item.name,
                    quantity=order_item.quantity,
                    inventory_quantity=item.inventory_quantity,
                )
            )

        order.cancel()
        self.order_repository.save(order)

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
            order_items=order_items,
        )
