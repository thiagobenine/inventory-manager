from typing import Protocol

from src.domain.entities.client import Client


class ClientRepositoryInterface(Protocol):
    def find_client_by_name(self, client_name: str) -> Client: ...

    def save(self, client: Client) -> None: ...
