from src.domain.entities.entity import Entity


class Item(Entity):
    name: str
    inventory_quantity: int

    def decrease_inventory_quantity(self, quantity: int):
        self.inventory_quantity -= quantity

    def increase_inventory_quantity(self, quantity: int):
        self.inventory_quantity += quantity

    def set_inventory_quantity(self, quantity: int):
        self.inventory_quantity = quantity
