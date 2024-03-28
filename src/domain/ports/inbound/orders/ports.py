from typing import Protocol

from src.domain.ports.inbound.orders.dtos import (
    CancelOrderInputDTO,
    CancelOrderOutputDTO,
    CreateOrderInputDTO,
    CreateOrderOutputDTO,
)


class CreateOrderPort(Protocol):
    def execute(
        self, input_dto: CreateOrderInputDTO
    ) -> CreateOrderOutputDTO: ...


class CancelOrderPort(Protocol):
    def execute(
        self, input_dto: CancelOrderInputDTO
    ) -> CancelOrderOutputDTO: ...
