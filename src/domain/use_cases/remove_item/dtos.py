from pydantic import BaseModel


class RemoveItemInputDTO(BaseModel):
    name: str

class RemoveItemOutputDTO(BaseModel):
    name: str