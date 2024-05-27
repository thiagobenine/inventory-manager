from typing import Protocol

from src.domain.ports.inbound.orders.dtos import (
    CancelOrderInputDTO,
    CancelOrderOutputDTO,
    CreateGoomerOrderInputDTO,
    CreateGoomerOrderOutputDTO,
    CreateManualOrderInputDTO,
    CreateManualOrderOutputDTO,
)


class CreateGoomerOrderPort(Protocol):
    def execute(
        self, input_dto: CreateGoomerOrderInputDTO
    ) -> CreateGoomerOrderOutputDTO: ...


class CreateManualOrderPort(Protocol):
    def execute(
        self, input_dto: CreateManualOrderInputDTO
    ) -> CreateManualOrderOutputDTO: ...


class CancelOrderPort(Protocol):
    def execute(
        self, input_dto: CancelOrderInputDTO
    ) -> CancelOrderOutputDTO: ...
