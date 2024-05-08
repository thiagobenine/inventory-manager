from pydantic import BaseModel


class AddItemInputDTO(BaseModel):
    name: str
    inventory_quantity: int


class AddItemOutputDTO(BaseModel):
    name: str
    inventory_quantity: int


class RemoveItemInputDTO(BaseModel):
    item_name: str


class RemoveItemOutputDTO(BaseModel):
    item_name: str


class SetInventoryQuantityInputDTO(BaseModel):
    item_name: str
    inventory_quantity: int


class SetInventoryQuantityOutputDTO(BaseModel):
    item_name: str
    inventory_quantity: int
