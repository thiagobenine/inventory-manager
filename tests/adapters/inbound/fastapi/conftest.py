import pytest
from httpx import AsyncClient

from src.adapters.inbound.fastapi.dependencies import (
    build_add_item_use_case,
    build_create_goomer_order_use_case,
    build_create_manual_order_use_case,
    build_list_items_use_case,
    build_remove_item_use_case,
    build_set_inventory_quantities_use_case,
)
from src.adapters.outbound.repositories.mongo.client import (
    MongoClientRepository,
)
from src.adapters.outbound.repositories.mongo.item import MongoItemRepository
from src.adapters.outbound.repositories.mongo.order import MongoOrderRepository
from src.domain.use_cases.add_item import AddItemUseCase
from src.domain.use_cases.create_goomer_order import CreateGoomerOrderUseCase
from src.domain.use_cases.create_manual_order import CreateManualOrderUseCase
from src.domain.use_cases.list_items import ListItemsUseCase
from src.domain.use_cases.remove_item import RemoveItemUseCase
from src.domain.use_cases.set_inventory_quantities import (
    SetInventoryQuantitiesUseCase,
)
from src.main import build_api


@pytest.fixture()
async def fastapi_client(mongo_connection):
    fastapi_app = build_api()

    client_repository = MongoClientRepository(mongo_connection)
    order_repository = MongoOrderRepository(mongo_connection)
    item_repository = MongoItemRepository(mongo_connection)

    add_item_use_case = AddItemUseCase(item_repository=item_repository)
    list_items_use_case = ListItemsUseCase(item_repository=item_repository)
    set_inventory_quantities_use_case = SetInventoryQuantitiesUseCase(
        item_repository=item_repository
    )
    remove_item_use_case = RemoveItemUseCase(item_repository=item_repository)
    create_goomer_order_use_case = CreateGoomerOrderUseCase(
        item_repository=item_repository,
        order_repository=order_repository,
        client_repository=client_repository,
    )
    create_manual_order_use_case = CreateManualOrderUseCase(
        item_repository=item_repository,
        order_repository=order_repository,
    )

    fastapi_app.dependency_overrides[build_add_item_use_case] = (
        lambda: add_item_use_case
    )
    fastapi_app.dependency_overrides[build_list_items_use_case] = (
        lambda: list_items_use_case
    )
    fastapi_app.dependency_overrides[
        build_set_inventory_quantities_use_case
    ] = lambda: set_inventory_quantities_use_case
    fastapi_app.dependency_overrides[build_remove_item_use_case] = (
        lambda: remove_item_use_case
    )
    fastapi_app.dependency_overrides[build_create_goomer_order_use_case] = (
        lambda: create_goomer_order_use_case
    )
    fastapi_app.dependency_overrides[build_create_manual_order_use_case] = (
        lambda: create_manual_order_use_case
    )

    async with AsyncClient(
        app=fastapi_app, base_url="http://localhost", follow_redirects=True
    ) as ac:
        yield ac
