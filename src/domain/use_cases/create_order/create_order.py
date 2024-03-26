from src.domain.entities.item import Item
from src.domain.entities.order import OrderItem
from src.domain.exceptions import ClientNotFoundError, ItemsNotFoundByNameError
from src.domain.factories.order import OrderFactory
from src.domain.ports.repositories.client import ClientRepositoryInterface
from src.domain.ports.repositories.item import ItemRepositoryInterface
from src.domain.ports.repositories.order import OrderRepositoryInterface
from src.domain.use_cases.create_order.dtos import (
    CreateOrderInputDTO,
    CreateOrderOutputDTO,
    OrderItemOutputDTO,
)


class CreateOrderUseCase:
    def __init__(
        self,
        client_repository: ClientRepositoryInterface,
        item_repository: ItemRepositoryInterface,
        order_repository: OrderRepositoryInterface,
    ):
        self.client_repository = client_repository
        self.item_repository = item_repository
        self.order_repository = order_repository

    @staticmethod
    def _validate_no_missing_items(
        items_names_from_dto: list[str], items_from_repository: list[Item]
    ):
        is_any_item_missing = len(items_from_repository) != len(
            items_names_from_dto
        )
        if is_any_item_missing:
            found_item_names = {item.name for item in items_from_repository}
            missing_item_names = set(items_names_from_dto) - found_item_names
            raise ItemsNotFoundByNameError(list(missing_item_names))

    def execute(self, input_dto: CreateOrderInputDTO) -> CreateOrderOutputDTO:
        client = self.client_repository.find_client_by_name(
            input_dto.client_name
        )
        if not client:
            raise ClientNotFoundError(input_dto.client_name)

        items_names_from_dto = [
            item_input.item_name for item_input in input_dto.items
        ]
        items_from_repository = self.item_repository.find_items_by_names(
            items_names_from_dto
        )

        self._validate_no_missing_items(
            items_names_from_dto, items_from_repository
        )

        item_map_by_name = {item.name: item for item in items_from_repository}
        item_map_by_id = {item.id: item for item in items_from_repository}

        order_items = []
        for item_input in input_dto.items:
            item = item_map_by_name[item_input.item_name]
            item.decrease_inventory_quantity(item_input.quantity)
            order_item = OrderItem(
                item_id=item.id, quantity=item_input.quantity
            )
            order_items.append(order_item)

        order = OrderFactory.build(input_dto, client, order_items)

        self.item_repository.save_all(items_from_repository)
        self.order_repository.save(order)

        return CreateOrderOutputDTO(
            order_id=order.id,
            client_name=client.name,
            external_order_id=order.external_id,
            order_items=[
                OrderItemOutputDTO(
                    item_name=item_map_by_id[order_item.item_id].name,
                    quantity=order_item.quantity,
                    inventory_quantity=item_map_by_id[
                        order_item.item_id
                    ].inventory_quantity,
                )
                for order_item in order.items
            ],
        )
