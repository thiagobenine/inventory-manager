from uuid import UUID


class DomainException(Exception):
    pass


class ClientNotFoundError(DomainException):
    def __init__(self, client_name: str):
        super().__init__(f"Client not found: {client_name}")


class ItemNotFoundByNameError(DomainException):
    def __init__(self, item_name: str):
        super().__init__(f"Item not found: {item_name}")


class ItemsNotFoundByIdError(DomainException):
    def __init__(self, items_ids: list[UUID]):
        super().__init__(f"Items not found: {items_ids}")


class ItemAlreadyExistsError(DomainException):
    def __init__(self, item_name: str):
        super().__init__(f"Item already exists: {item_name}")


class OrderNotFoundError(DomainException):
    def __init__(self, order_id: UUID):
        super().__init__(f"Order not found: {order_id}")
