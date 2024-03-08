from typing import Protocol

from domain.entities.client import Client


class ClientRepositoryInterface(Protocol):
    def find_client_by_name(self, client_name: str) -> Client:
        ...
