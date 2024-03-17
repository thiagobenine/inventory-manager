from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from src.domain.entities.client import Client


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
    items: list[OrderItem]
