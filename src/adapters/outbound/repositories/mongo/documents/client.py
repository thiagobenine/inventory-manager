from typing import ClassVar

from bson import ObjectId
from mongoengine import (  # type: ignore
    Document,
    ObjectIdField,
    StringField,
)


class ClientDocument(Document):
    meta: ClassVar[dict] = {"collection": "clients"}
    id = ObjectIdField(primary_key=True, default=lambda: ObjectId())
    name = StringField(required=True)
