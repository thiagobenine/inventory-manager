from typing import Protocol

from src.domain.ports.inbound.items.dtos import (
    AddItemInputDTO,
    AddItemOutputDTO,
    ListItemsOutputDTO,
    RemoveItemInputDTO,
    RemoveItemOutputDTO,
    SetInventoryQuantityInputDTO,
    SetInventoryQuantityOutputDTO,
)


class AddItemPort(Protocol):
    def execute(self, input_dto: AddItemInputDTO) -> AddItemOutputDTO: ...


class ListItemsPort(Protocol):
    def execute(self) -> ListItemsOutputDTO: ...


class RemoveItemPort(Protocol):
    def execute(
        self, input_dto: RemoveItemInputDTO
    ) -> RemoveItemOutputDTO: ...


class SetInventoryQuantityPort(Protocol):
    def execute(
        self, input_dto: SetInventoryQuantityInputDTO
    ) -> SetInventoryQuantityOutputDTO: ...
