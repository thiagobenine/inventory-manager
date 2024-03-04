from domain.factories.order import OrderFactory, OrderItemFactory
from domain.repositories.client import ClientRepositoryInterface
from domain.repositories.item import ItemRepositoryInterface
from domain.repositories.order import OrderRepositoryInterface

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
        client = self.client_repository.find_client_by_name(input_dto.client_name) # exception caso não encontre?
        order_items = []
        for item_input in input_dto.items:
            item = self.item_repository.find_item_by_name(item_input.item_name) # exception caso não encontre?
            item.update_inventory(item_input.quantity)
            self.item_repository.update_inventory(item.name, item.inventory_quantity)
            order_item = OrderItemFactory.build(item, item_input.quantity) # tá bom o nome "build"?
            order_items.append(order_item)

        order = OrderFactory.build(input_dto, client, order_items)  # tá bom o nome "build"?
        self.order_repository.save(order)

        return CreateOrderOutputDTO( # precisa de factory?
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
    