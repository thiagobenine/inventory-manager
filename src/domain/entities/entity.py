from bson import ObjectId
from pydantic import BaseModel, Field
from pydantic_mongo import ObjectIdField


class Entity(BaseModel):
    id: ObjectIdField = Field(default_factory=ObjectId)
