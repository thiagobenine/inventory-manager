from typing import List, Optional

from pydantic import BaseModel


class OrderItemInputDTO(BaseModel):
    item_name: str
    quantity: int

class CreateOrderInputDTO(BaseModel):
    client_name: str
    external_order_id: int
    created_at: str
    items: List[OrderItemInputDTO]

class OrderItemOutputDTO(BaseModel):
    item_name: str
    quantity: int
    inventory_quantity: int

class CreateOrderOutputDTO(BaseModel):
    order_id: int
    client_name: str
    external_order_id: int
    order_items: List[OrderItemOutputDTO]
