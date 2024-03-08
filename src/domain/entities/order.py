from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel

from domain.entities.client import Client
from domain.entities.item import Item


class OrderItem(BaseModel):
    quantity: int
    item_id: int

class Order(BaseModel):
    id: UUID
    external_id: int
    created_at: datetime
    updated_at: datetime
    is_cancelled: bool
    client: Client
    items: List[OrderItem]