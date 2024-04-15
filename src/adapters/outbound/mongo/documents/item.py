from typing import ClassVar

from bson import ObjectId
from mongoengine import Document, IntField, ObjectIdField, StringField


class ItemDocument(Document):
    meta: ClassVar[dict] = {"collection": "items"}
    id = ObjectIdField(primary_key=True, default=lambda: ObjectId())
    name = StringField(required=True)
    inventory_quantity = IntField(required=True)
