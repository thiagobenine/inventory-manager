from bson import ObjectId


class DomainException(Exception):
    pass


class ItemNotFoundByNameError(DomainException):
    item_name: str

    def __init__(self, item_name: str):
        self.item_name = item_name


class ItemsNotFoundByNameError(DomainException):
    items_names: list[str]

    def __init__(self, items_names: list[str]):
        self.items_names = items_names


class ItemAlreadyExistsError(DomainException):
    item_name: str

    def __init__(self, item_name: str):
        self.item_name = item_name


class OrderNotFoundError(DomainException):
    order_id: ObjectId

    def __init__(self, order_id: ObjectId):
        self.order_id = order_id
