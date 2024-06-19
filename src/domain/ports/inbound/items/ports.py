from typing import Protocol

from src.domain.ports.inbound.items.dtos import (
    AddItemInputDTO,
    AddItemOutputDTO,
    ListItemsOutputDTO,
    RemoveItemInputDTO,
    RemoveItemOutputDTO,
    SetInventoryQuantitiesInputDTO,
    SetInventoryQuantitiesOutputDTO,
)


class AddItemPort(Protocol):
    def execute(self, input_dto: AddItemInputDTO) -> AddItemOutputDTO: ...


class ListItemsPort(Protocol):
    def execute(self) -> ListItemsOutputDTO: ...


class RemoveItemPort(Protocol):
    def execute(
        self, input_dto: RemoveItemInputDTO
    ) -> RemoveItemOutputDTO: ...


class SetInventoryQuantitiesPort(Protocol):
    def execute(
        self, input_dto: SetInventoryQuantitiesInputDTO
    ) -> SetInventoryQuantitiesOutputDTO: ...
