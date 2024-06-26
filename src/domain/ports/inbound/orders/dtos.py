from pydantic import BaseModel
from pydantic_mongo import ObjectIdField


class OrderItemInputDTO(BaseModel):
    item_name: str
    quantity: int


class CreateGoomerOrderInputDTO(BaseModel):
    client_name: str
    external_order_id: int
    external_created_at: str
    items: list[OrderItemInputDTO]


class CreateOrderItemOutputDTO(BaseModel):
    item_name: str
    quantity: int
    inventory_quantity: int


class CreateGoomerOrderOutputDTO(BaseModel):
    order_id: ObjectIdField
    client_name: str
    external_order_id: int
    order_items: list[CreateOrderItemOutputDTO]


class CreateManualOrderInputDTO(BaseModel):
    items: list[OrderItemInputDTO]


class CreateManualOrderOutputDTO(BaseModel):
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
    client_name: str | None
    external_order_id: int | None
    order_items: list[CancelOrderItemOutputDTO]
    is_cancelled: bool
    created_at: str
    updated_at: str
