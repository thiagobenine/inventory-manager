from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Item(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    inventory_quantity: int

    def decrease_inventory_quantity(self, quantity: int):
        self.inventory_quantity -= quantity

    def set_inventory_quantity(self, quantity: int):
        self.inventory_quantity = quantity
