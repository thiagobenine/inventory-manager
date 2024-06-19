from http import HTTPStatus

from bson import ObjectId
from fastapi import HTTPException


class APIException(HTTPException):
    status_code: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR
    detail: str = ""

    def __init__(self, detail: str = "", status_code: int | None = None):
        if detail:
            self.detail = detail
        if status_code:
            self.status_code = HTTPStatus(status_code)

        super().__init__(status_code=self.status_code, detail=self.detail)

    def __str__(self) -> str:
        return self.detail


class ItemNotFoundByNameAPIException(APIException):
    status_code = HTTPStatus.NOT_FOUND

    def __init__(self, item_name: str):
        super().__init__(f"Item not found by name: {item_name}")


class ItemsNotFoundByNameAPIException(APIException):
    status_code = HTTPStatus.NOT_FOUND

    def __init__(self, items_names: list[str]):
        super().__init__(f"Items not found by names: {items_names}")


class ItemAlreadyExistsAPIException(APIException):
    status_code = HTTPStatus.CONFLICT

    def __init__(self, item_name: str):
        super().__init__(f"Item already exists: {item_name}")


class OrderNotFoundAPIException(APIException):
    status_code = HTTPStatus.NOT_FOUND

    def __init__(self, order_id: ObjectId):
        super().__init__(f"Order not found by ID: {order_id}")
