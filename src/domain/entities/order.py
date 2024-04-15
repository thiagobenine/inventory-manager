from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from src.domain.entities.client import Client
from src.domain.entities.entity import Entity
from src.domain.entities.item import Item


class OrderItem(BaseModel):
    quantity: int
    item_id: UUID


class Order(Entity):
    external_id: int
    created_at: datetime
    updated_at: datetime
    is_cancelled: bool
    client: Client
    items: list[OrderItem]

    def cancel(self):
        self.is_cancelled = True
        self.updated_at = datetime.now()
