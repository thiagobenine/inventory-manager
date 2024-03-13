from uuid import UUID

from pydantic import BaseModel


class Item(BaseModel):
    id: UUID
    name: str
    inventory_quantity: int

    def decrease_inventory_quantity(self, quantity: int):
        self.inventory_quantity -= quantity