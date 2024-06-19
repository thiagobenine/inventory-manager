from http import HTTPStatus

from fastapi import APIRouter, Depends, Response

from src.adapters.inbound.fastapi.dependencies import (
    build_add_item_use_case,
    build_create_goomer_order_use_case,
    build_create_manual_order_use_case,
    build_list_items_use_case,
    build_remove_item_use_case,
    build_set_inventory_quantities_use_case,
)
from src.adapters.inbound.fastapi.dtos import (
    RequestAddItemInputDTO,
    RequestCreateGoomerOrderInputDTO,
    RequestCreateManualOrderInputDTO,
    RequestRemoveItemInputDTO,
    RequestSetInventoryQuantitiesInputDTO,
    ResponseAddItemOutputDTO,
    ResponseCreateGoomerOrderOutputDTO,
    ResponseCreateManualOrderOutputDTO,
    ResponseListItemsOutputDTO,
    ResponseRemoveItemOutputDTO,
    ResponseSetInventoryQuantitiesOutputDTO,
)
from src.adapters.inbound.fastapi.presenter import FastAPIPresenter
from src.domain.ports.inbound.items.dtos import (
    AddItemInputDTO,
    RemoveItemInputDTO,
    SetInventoryQuantitiesInputDTO,
    SetInventoryQuantityItemInputDTO,
)
from src.domain.ports.inbound.items.ports import (
    AddItemPort,
    ListItemsPort,
    RemoveItemPort,
    SetInventoryQuantitiesPort,
)
from src.domain.ports.inbound.orders.dtos import (
    CreateGoomerOrderInputDTO,
    CreateManualOrderInputDTO,
    OrderItemInputDTO,
)
from src.domain.ports.inbound.orders.ports import (
    CreateGoomerOrderPort,
    CreateManualOrderPort,
)

router = APIRouter()


@router.post("/items")
async def add_item(
    body: RequestAddItemInputDTO,
    response: Response,
    use_case: AddItemPort = Depends(build_add_item_use_case),
) -> ResponseAddItemOutputDTO:
    input_dto = AddItemInputDTO(
        item_name=body.item_name,
        inventory_quantity=body.inventory_quantity,
    )
    result = use_case.execute(input_dto)
    response.status_code = HTTPStatus.CREATED
    return FastAPIPresenter.build_add_item_response(result)


@router.get("/items")
async def list_items(
    use_case: ListItemsPort = Depends(build_list_items_use_case),
) -> ResponseListItemsOutputDTO:
    result = use_case.execute()
    return FastAPIPresenter.build_list_items_response(result)


@router.patch("/items")
async def set_inventory_quantities(
    body: RequestSetInventoryQuantitiesInputDTO,
    use_case: SetInventoryQuantitiesPort = Depends(
        build_set_inventory_quantities_use_case
    ),
) -> ResponseSetInventoryQuantitiesOutputDTO:
    input_dto = SetInventoryQuantitiesInputDTO(
        items=[
            SetInventoryQuantityItemInputDTO(
                item_name=item.item_name,
                inventory_quantity=item.inventory_quantity,
            )
            for item in body.items
        ]
    )
    result = use_case.execute(input_dto)
    return FastAPIPresenter.build_set_inventory_quantities_response(result)


@router.delete("/items")
async def remove_item(
    body: RequestRemoveItemInputDTO,
    use_case: RemoveItemPort = Depends(build_remove_item_use_case),
) -> ResponseRemoveItemOutputDTO:
    input_dto = RemoveItemInputDTO(
        item_name=body.item_name,
    )
    result = use_case.execute(input_dto)
    return FastAPIPresenter.build_remove_item_response(result)


@router.post("/orders/goomer")
async def create_goomer_order(
    body: RequestCreateGoomerOrderInputDTO,
    response: Response,
    use_case: CreateGoomerOrderPort = Depends(
        build_create_goomer_order_use_case
    ),
) -> ResponseCreateGoomerOrderOutputDTO:
    input_dto = CreateGoomerOrderInputDTO(
        client_name=body.client_name,
        external_order_id=body.external_order_id,
        external_created_at=body.external_created_at,
        items=[
            OrderItemInputDTO(item_name=item.item_name, quantity=item.quantity)
            for item in body.items
        ],
    )
    result = use_case.execute(input_dto)
    response.status_code = HTTPStatus.CREATED
    return FastAPIPresenter.build_create_goomer_order_response(result)


@router.post("/orders/manual")
async def create_manual_order(
    body: RequestCreateManualOrderInputDTO,
    response: Response,
    use_case: CreateManualOrderPort = Depends(
        build_create_manual_order_use_case
    ),
) -> ResponseCreateManualOrderOutputDTO:
    input_dto = CreateManualOrderInputDTO(
        items=[
            OrderItemInputDTO(item_name=item.item_name, quantity=item.quantity)
            for item in body.items
        ],
    )
    result = use_case.execute(input_dto)
    response.status_code = HTTPStatus.CREATED
    return FastAPIPresenter.build_create_manual_order_response(result)
