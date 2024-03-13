from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from domain.entities.client import Client
from domain.entities.item import Item


class OrderItem(BaseModel):
    quantity: int
    item_id: UUID

class Order(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    external_id: int
    created_at: datetime
    updated_at: datetime
    is_cancelled: bool
    client: Client
    items: List[OrderItem]