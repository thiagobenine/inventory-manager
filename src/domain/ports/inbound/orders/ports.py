from typing import Protocol

from src.domain.ports.inbound.orders.dtos import (
    CancelOrderInputDTO,
    CancelOrderOutputDTO,
    CreateGoomerOrderInputDTO,
    CreateGoomerOrderOutputDTO,
)


class CreateGoomerOrderPort(Protocol):
    def execute(
        self, input_dto: CreateGoomerOrderInputDTO
    ) -> CreateGoomerOrderOutputDTO: ...


class CancelOrderPort(Protocol):
    def execute(
        self, input_dto: CancelOrderInputDTO
    ) -> CancelOrderOutputDTO: ...
