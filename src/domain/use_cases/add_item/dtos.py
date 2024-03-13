from pydantic import BaseModel


class AddItemInputDTO(BaseModel):
    name: str
    inventory_quantity: int