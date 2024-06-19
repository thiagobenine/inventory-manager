from src.adapters.outbound.repositories.mongo.client import (
    MongoClientRepository,
)
from src.adapters.outbound.repositories.mongo.connection import MongoConnection
from src.adapters.outbound.repositories.mongo.item import MongoItemRepository
from src.adapters.outbound.repositories.mongo.order import MongoOrderRepository
from src.domain.ports.inbound.items.ports import (
    AddItemPort,
    ListItemsPort,
    RemoveItemPort,
    SetInventoryQuantitiesPort,
)
from src.domain.ports.inbound.orders.ports import (
    CreateGoomerOrderPort,
    CreateManualOrderPort,
)
from src.domain.ports.outbound.repositories.client import (
    ClientRepositoryInterface,
)
from src.domain.ports.outbound.repositories.item import ItemRepositoryInterface
from src.domain.ports.outbound.repositories.order import (
    OrderRepositoryInterface,
)
from src.domain.use_cases.add_item import AddItemUseCase
from src.domain.use_cases.create_goomer_order import CreateGoomerOrderUseCase
from src.domain.use_cases.create_manual_order import CreateManualOrderUseCase
from src.domain.use_cases.list_items import ListItemsUseCase
from src.domain.use_cases.remove_item import RemoveItemUseCase
from src.domain.use_cases.set_inventory_quantities import (
    SetInventoryQuantitiesUseCase,
)
from src.settings import settings


def build_add_item_use_case() -> AddItemPort:
    return AddItemUseCase(
        item_repository=build_item_repository(),
    )


def build_list_items_use_case() -> ListItemsPort:
    return ListItemsUseCase(
        item_repository=build_item_repository(),
    )


def build_set_inventory_quantities_use_case() -> SetInventoryQuantitiesPort:
    return SetInventoryQuantitiesUseCase(
        item_repository=build_item_repository(),
    )


def build_remove_item_use_case() -> RemoveItemPort:
    return RemoveItemUseCase(
        item_repository=build_item_repository(),
    )


def build_create_goomer_order_use_case() -> CreateGoomerOrderPort:
    return CreateGoomerOrderUseCase(
        item_repository=build_item_repository(),
        order_repository=build_order_repository(),
        client_repository=build_client_repository(),
    )


def build_create_manual_order_use_case() -> CreateManualOrderPort:
    return CreateManualOrderUseCase(
        item_repository=build_item_repository(),
        order_repository=build_order_repository(),
    )


def build_client_repository() -> ClientRepositoryInterface:
    return MongoClientRepository(
        MongoConnection(
            settings.MONGO_CONNECTION_STRING,
        )
    )


def build_order_repository() -> OrderRepositoryInterface:
    return MongoOrderRepository(
        MongoConnection(
            settings.MONGO_CONNECTION_STRING,
        )
    )


def build_item_repository() -> ItemRepositoryInterface:
    return MongoItemRepository(
        MongoConnection(
            settings.MONGO_CONNECTION_STRING,
        )
    )
