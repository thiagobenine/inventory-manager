from datetime import datetime
from uuid import UUID

from src.domain.entities.item import Item
from src.domain.exceptions import ItemsNotFoundByIdError, OrderNotFoundError
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

    @staticmethod
    def _validate_no_missing_items(
        items_ids_from_order: list[UUID], items_from_repository: list[Item]
    ):
        is_any_item_missing = len(items_from_repository) != len(
            items_ids_from_order
        )
        if is_any_item_missing:
            found_item_ids = {item.id for item in items_from_repository}
            missing_items_ids = set(items_ids_from_order) - found_item_ids
            missing_items_ids_string = [
                str(item_id) for item_id in missing_items_ids
            ]
            raise ItemsNotFoundByIdError(missing_items_ids_string)

    def execute(self, input_dto: CancelOrderInputDTO) -> CancelOrderOutputDTO:
        order = self.order_repository.find_order_by_id(input_dto.order_id)
        if not order:
            raise OrderNotFoundError(input_dto.order_id)

        items_ids_from_order = [
            order_item.item_id for order_item in order.items
        ]
        items_from_repository = self.item_repository.find_items_by_ids(
            items_ids_from_order
        )

        self._validate_no_missing_items(
            items_ids_from_order, items_from_repository
        )

        item_map_by_id = {item.id: item for item in items_from_repository}

        order_items = []
        for order_item in order.items:
            item = item_map_by_id[order_item.item_id]
            order_items.append(
                CancelOrderItemOutputDTO(
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
