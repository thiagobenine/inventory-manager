class DomainException(Exception):
    pass


class ClientNotFoundError(DomainException):
    def __init__(self, client_name: str):
        super().__init__(f"Client not found: {client_name}")


class ItemNotFoundError(DomainException):
    def __init__(self, item_name: str):
        super().__init__(f"Item not found: {item_name}")