from datetime import datetime

from pydantic import BaseModel

from src.domain.entities.client import Client
from src.domain.entities.entity import Entity
from src.domain.entities.item import Item


class OrderItem(BaseModel):
    quantity: int
    item: Item


class Order(Entity):
    external_id: int | None
    external_created_at: str | None
    created_at: datetime
    updated_at: datetime
    is_cancelled: bool
    client: Client | None
    order_items: list[OrderItem]

    def cancel(self):
        self.is_cancelled = True
        self.updated_at = datetime.now()
