from starlette.requests import Request

from src.adapters.inbound.fastapi.dtos import (
    CreateOrderItemOutputDTO,
    ItemOutputDTO,
    ResponseAddItemOutputDTO,
    ResponseCreateGoomerOrderOutputDTO,
    ResponseCreateManualOrderOutputDTO,
    ResponseListItemsOutputDTO,
    ResponseRemoveItemOutputDTO,
    ResponseSetInventoryQuantitiesOutputDTO,
    SetInventoryQuantityItemOutputDTO,
)
from src.adapters.inbound.fastapi.exceptions import (
    APIException,
    ItemAlreadyExistsAPIException,
    ItemNotFoundByNameAPIException,
    ItemsNotFoundByNameAPIException,
    OrderNotFoundAPIException,
)
from src.domain.exceptions import (
    DomainException,
    ItemAlreadyExistsError,
    ItemNotFoundByNameError,
    ItemsNotFoundByNameError,
    OrderNotFoundError,
)
from src.domain.ports.inbound.items.dtos import (
    AddItemOutputDTO,
    ListItemsOutputDTO,
    RemoveItemOutputDTO,
    SetInventoryQuantitiesOutputDTO,
)
from src.domain.ports.inbound.orders.dtos import (
    CreateGoomerOrderOutputDTO,
    CreateManualOrderOutputDTO,
)


class FastAPIPresenter:
    @staticmethod
    def map_domain_exception(_: Request, exception: DomainException):
        match exception:
            case ItemNotFoundByNameError() as e:
                raise ItemNotFoundByNameAPIException(item_name=e.item_name)
            case ItemsNotFoundByNameError() as e:
                raise ItemsNotFoundByNameAPIException(
                    items_names=e.items_names
                )
            case ItemAlreadyExistsError() as e:
                raise ItemAlreadyExistsAPIException(item_name=e.item_name)
            case OrderNotFoundError() as e:
                raise OrderNotFoundAPIException(order_id=e.order_id)
            case _:
                raise APIException()

    @staticmethod
    def build_add_item_response(
        use_case_output_dto: AddItemOutputDTO,
    ) -> ResponseAddItemOutputDTO:
        return ResponseAddItemOutputDTO(
            item_name=use_case_output_dto.item_name,
            inventory_quantity=use_case_output_dto.inventory_quantity,
        )

    @staticmethod
    def build_list_items_response(
        use_case_output_dto: ListItemsOutputDTO,
    ) -> ResponseListItemsOutputDTO:
        items = [
            ItemOutputDTO(
                item_name=item.item_name,
                inventory_quantity=item.inventory_quantity,
            )
            for item in use_case_output_dto.items
        ]
        return ResponseListItemsOutputDTO(items=items)

    @staticmethod
    def build_set_inventory_quantities_response(
        use_case_output_dto: SetInventoryQuantitiesOutputDTO,
    ) -> ResponseSetInventoryQuantitiesOutputDTO:
        items = [
            SetInventoryQuantityItemOutputDTO(
                item_name=item.item_name,
                inventory_quantity=item.inventory_quantity,
            )
            for item in use_case_output_dto.items
        ]
        return ResponseSetInventoryQuantitiesOutputDTO(items=items)

    @staticmethod
    def build_remove_item_response(
        use_case_output_dto: RemoveItemOutputDTO,
    ) -> ResponseRemoveItemOutputDTO:
        return ResponseRemoveItemOutputDTO(
            item_name=use_case_output_dto.item_name
        )

    @staticmethod
    def build_create_goomer_order_response(
        use_case_output_dto: CreateGoomerOrderOutputDTO,
    ) -> ResponseCreateGoomerOrderOutputDTO:
        return ResponseCreateGoomerOrderOutputDTO(
            order_id=use_case_output_dto.order_id,
            client_name=use_case_output_dto.client_name,
            external_order_id=use_case_output_dto.external_order_id,
            order_items=[
                CreateOrderItemOutputDTO(
                    item_name=item.item_name,
                    quantity=item.quantity,
                    inventory_quantity=item.inventory_quantity,
                )
                for item in use_case_output_dto.order_items
            ],
        )

    @staticmethod
    def build_create_manual_order_response(
        use_case_output_dto: CreateManualOrderOutputDTO,
    ) -> ResponseCreateManualOrderOutputDTO:
        return ResponseCreateManualOrderOutputDTO(
            order_id=use_case_output_dto.order_id,
            order_items=[
                CreateOrderItemOutputDTO(
                    item_name=item.item_name,
                    quantity=item.quantity,
                    inventory_quantity=item.inventory_quantity,
                )
                for item in use_case_output_dto.order_items
            ],
        )
