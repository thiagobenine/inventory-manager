from uuid import UUID

from pydantic import BaseModel


class CancelOrderInputDTO(BaseModel):
    order_id: UUID


class OrderItemOutputDTO(BaseModel):
    item_name: str
    quantity: int
    inventory_quantity: int


class CancelOrderOutputDTO(BaseModel):
    order_id: UUID
    client_name: str
    external_order_id: int
    order_items: list[OrderItemOutputDTO]
    is_cancelled: bool
    created_at: str
    updated_at: str
