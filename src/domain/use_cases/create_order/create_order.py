from domain.entities.order import OrderItem
from domain.factories.order import OrderFactory
from domain.ports.repositories.client import ClientRepositoryInterface
from domain.ports.repositories.item import ItemRepositoryInterface
from domain.ports.repositories.order import OrderRepositoryInterface

from .dtos import CreateOrderInputDTO, CreateOrderOutputDTO, OrderItemOutputDTO


class CreateOrderUseCase:
    def __init__(
            self,
            client_repository: ClientRepositoryInterface,
            item_repository: ItemRepositoryInterface,
            order_repository: OrderRepositoryInterface
        ):
        self.client_repository = client_repository
        self.item_repository = item_repository
        self.order_repository = order_repository

    def execute(self, input_dto: CreateOrderInputDTO) -> CreateOrderOutputDTO:
        client = self.client_repository.find_client_by_name(input_dto.client_name)
        order_items = []
        for item_input in input_dto.items:
            item = self.item_repository.find_item_by_name(item_input.item_name)
            item.decrease_inventory_quantity(item_input.quantity)
            self.item_repository.save(item.name, item.inventory_quantity)
            order_item = OrderItem(item=item, quantity=item_input.quantity)
            order_items.append(order_item)

        order = OrderFactory.build(input_dto, client, order_items)
        self.order_repository.save(order)

        return CreateOrderOutputDTO(
            order_id=order.id,
            client_name=client.name,
            external_order_id=order.external_id,
            order_items=[
                OrderItemOutputDTO(
                    item_name=order_item.item.name,
                    quantity=order_item.quantity,
                    inventory_quantity=order_item.item.inventory_quantity,
                )
                for order_item in order.items
            ],
        )
    