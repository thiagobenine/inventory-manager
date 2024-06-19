from pydantic import BaseModel


class AddItemInputDTO(BaseModel):
    item_name: str
    inventory_quantity: int


class AddItemOutputDTO(BaseModel):
    item_name: str
    inventory_quantity: int


class RemoveItemInputDTO(BaseModel):
    item_name: str


class RemoveItemOutputDTO(BaseModel):
    item_name: str


class SetInventoryQuantityItemInputDTO(BaseModel):
    item_name: str
    inventory_quantity: int


class SetInventoryQuantitiesInputDTO(BaseModel):
    items: list[SetInventoryQuantityItemInputDTO]


class SetInventoryQuantityItemOutputDTO(BaseModel):
    item_name: str
    inventory_quantity: int


class SetInventoryQuantitiesOutputDTO(BaseModel):
    items: list[SetInventoryQuantityItemOutputDTO]


class ItemOutputDTO(BaseModel):
    item_name: str
    inventory_quantity: int


class ListItemsOutputDTO(BaseModel):
    items: list[ItemOutputDTO]
