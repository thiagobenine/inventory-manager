from pydantic import BaseModel
from pydantic_mongo import ObjectIdField


class RequestAddItemInputDTO(BaseModel):
    item_name: str
    inventory_quantity: int


class ResponseAddItemOutputDTO(BaseModel):
    item_name: str
    inventory_quantity: int


class RequestRemoveItemInputDTO(BaseModel):
    item_name: str


class ResponseRemoveItemOutputDTO(BaseModel):
    item_name: str


class SetInventoryQuantityItemInputDTO(BaseModel):
    item_name: str
    inventory_quantity: int


class RequestSetInventoryQuantitiesInputDTO(BaseModel):
    items: list[SetInventoryQuantityItemInputDTO]


class SetInventoryQuantityItemOutputDTO(BaseModel):
    item_name: str
    inventory_quantity: int


class ResponseSetInventoryQuantitiesOutputDTO(BaseModel):
    items: list[SetInventoryQuantityItemOutputDTO]


class ItemOutputDTO(BaseModel):
    item_name: str
    inventory_quantity: int


class ResponseListItemsOutputDTO(BaseModel):
    items: list[ItemOutputDTO]


class OrderItemInputDTO(BaseModel):
    item_name: str
    quantity: int


class RequestCreateGoomerOrderInputDTO(BaseModel):
    client_name: str
    external_order_id: int
    external_created_at: str
    items: list[OrderItemInputDTO]


class CreateOrderItemOutputDTO(BaseModel):
    item_name: str
    quantity: int
    inventory_quantity: int


class ResponseCreateGoomerOrderOutputDTO(BaseModel):
    order_id: ObjectIdField
    client_name: str
    external_order_id: int
    order_items: list[CreateOrderItemOutputDTO]


class RequestCreateManualOrderInputDTO(BaseModel):
    items: list[OrderItemInputDTO]


class ResponseCreateManualOrderOutputDTO(BaseModel):
    order_id: ObjectIdField
    order_items: list[CreateOrderItemOutputDTO]


class CancelOrderInputDTO(BaseModel):
    order_id: ObjectIdField


class CancelOrderItemOutputDTO(BaseModel):
    item_name: str
    quantity: int
    inventory_quantity: int


class CancelOrderOutputDTO(BaseModel):
    order_id: ObjectIdField
    client_name: str | None = None
    external_order_id: int | None = None
    order_items: list[CancelOrderItemOutputDTO]
    is_cancelled: bool
    created_at: str
    updated_at: str
