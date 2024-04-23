from typing import ClassVar

from mongoengine import (  # type: ignore
    CASCADE,
    Document,
    IntField,
    ReferenceField,
)

from src.adapters.outbound.repositories.mongo.documents.item import (
    ItemDocument,
)


class OrderItemDocument(Document):
    meta: ClassVar[dict] = {"collection": "order_items"}
    quantity = IntField(required=True)
    item = ReferenceField(
        ItemDocument, required=True, reverse_delete_rule=CASCADE
    )
