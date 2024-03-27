from uuid import UUID

from pydantic import BaseModel


class OrderItemInputDTO(BaseModel):
    item_name: str
    quantity: int


class CreateOrderInputDTO(BaseModel):
    client_name: str
    external_order_id: int
    created_at: str
    items: list[OrderItemInputDTO]


class CreateOrderItemOutputDTO(BaseModel):
    item_name: str
    quantity: int
    inventory_quantity: int


class CreateOrderOutputDTO(BaseModel):
    order_id: int
    client_name: str
    external_order_id: int
    order_items: list[CreateOrderItemOutputDTO]


class CancelOrderInputDTO(BaseModel):
    order_id: UUID


class CancelOrderItemOutputDTO(BaseModel):
    item_name: str
    quantity: int
    inventory_quantity: int


class CancelOrderOutputDTO(BaseModel):
    order_id: UUID
    client_name: str
    external_order_id: int
    order_items: list[CancelOrderItemOutputDTO]
    is_cancelled: bool
    created_at: str
    updated_at: str
