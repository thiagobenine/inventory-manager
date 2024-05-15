from __future__ import annotations

from pymongo import InsertOne, UpdateOne

from src.adapters.outbound.repositories.mongo.connection import MongoConnection
from src.adapters.outbound.repositories.mongo.documents.item import (
    ItemDocument,
)
from src.domain.entities.item import Item


class MongoItemRepository:
    def __init__(self, mongo_connection: MongoConnection):
        mongo_connection.connect()

    def find_item_by_name(self, item_name: str) -> Item | None:
        document = ItemDocument.objects(name=item_name).first()
        if document:
            return Item(
                id=document.id,
                name=document.name,
                inventory_quantity=document.inventory_quantity,
            )
        return None

    def find_items_by_names(self, items_names: list[str]) -> list[Item]:
        documents = ItemDocument.objects(name__in=items_names)
        return [
            Item(
                id=doc.id,
                name=doc.name,
                inventory_quantity=doc.inventory_quantity,
            )
            for doc in documents
        ]

    def get_all(self) -> list[Item]:
        documents = ItemDocument.objects()
        return [
            Item(
                id=doc.id,
                name=doc.name,
                inventory_quantity=doc.inventory_quantity,
            )
            for doc in documents
        ]

    def remove_item_by_name(self, item_name: str) -> None:
        ItemDocument.objects(name=item_name).delete()

    def save(self, item: Item) -> None:
        item_doc = ItemDocument(
            id=item.id,
            name=item.name,
            inventory_quantity=item.inventory_quantity,
        )
        item_doc.save()

    def save_all(self, items: list[Item]) -> None:
        bulk_operations = []
        for item in items:
            existing_item = ItemDocument.objects(name=item.name).first()
            if existing_item:
                update_operation = UpdateOne(
                    {"_id": existing_item.id},
                    {"$set": {"inventory_quantity": item.inventory_quantity}},
                )
                bulk_operations.append(update_operation)
            else:
                new_item = {
                    "_id": item.id,
                    "name": item.name,
                    "inventory_quantity": item.inventory_quantity,
                }
                insert_operation = InsertOne(new_item)
                bulk_operations.append(insert_operation)

        ItemDocument._get_collection().bulk_write(bulk_operations)
