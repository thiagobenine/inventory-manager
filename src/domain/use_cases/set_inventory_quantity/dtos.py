from pydantic import BaseModel


class SetInventoryQuantityInputDTO(BaseModel):
    item_name: str
    inventory_quantity: int


class SetInventoryQuantityOutputDTO(BaseModel):
    item_name: str
    inventory_quantity: int
