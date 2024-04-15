from src.adapters.outbound.mongo.connection import MongoConnection
from src.adapters.outbound.mongo.documents.item import ItemDocument
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
        ItemDocument.objects.insert(
            [
                ItemDocument(
                    id=item.id,
                    name=item.name,
                    inventory_quantity=item.inventory_quantity,
                )
                for item in items
            ],
            load_bulk=False,
        )
