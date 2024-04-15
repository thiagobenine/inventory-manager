from datetime import datetime
from typing import ClassVar

import mongoengine
from bson import ObjectId
from mongoengine import (
    BooleanField,
    DateTimeField,
    Document,
    IntField,
    ListField,
    ObjectIdField,
    ReferenceField,
)

from src.adapters.outbound.mongo.documents.client import ClientDocument
from src.adapters.outbound.mongo.documents.order_item import OrderItemDocument


class OrderDocument(Document):
    meta: ClassVar[dict] = {"collection": "orders"}
    id = ObjectIdField(primary_key=True, default=lambda: ObjectId())
    external_id = IntField(required=True)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    is_cancelled = BooleanField(default=False)
    client = ReferenceField(ClientDocument, required=True)
    order_items = ListField(
        ReferenceField(OrderItemDocument, reverse_delete_rule=mongoengine.PULL)
    )
