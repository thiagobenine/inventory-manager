from pydantic import BaseModel


class Item(BaseModel):
    id: int
    name: str
    inventory_quantity: int

    def update_inventory(self, requested_quantity: int):
        self.inventory_quantity -= requested_quantity