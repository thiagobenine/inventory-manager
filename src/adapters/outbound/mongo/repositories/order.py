from bson import ObjectId

from src.adapters.outbound.mongo.connection import MongoConnection
from src.adapters.outbound.mongo.documents.client import ClientDocument
from src.adapters.outbound.mongo.documents.item import ItemDocument
from src.adapters.outbound.mongo.documents.order import OrderDocument
from src.adapters.outbound.mongo.documents.order_item import OrderItemDocument
from src.domain.entities.client import Client
from src.domain.entities.item import Item
from src.domain.entities.order import Order, OrderItem


class MongoOrderRepository:
    def __init__(self, mongo_connection: MongoConnection):
        mongo_connection.connect()

    def find_order_by_id(self, order_id: ObjectId) -> None | Order:
        document = OrderDocument.objects.with_id(order_id)
        if document:
            client = Client(
                id=document.client.id,
                name=document.client.name,
            )
            order_items = [
                OrderItem(
                    quantity=order_item.quantity,
                    item=Item(
                        id=order_item.item.id,
                        name=order_item.item.name,
                        inventory_quantity=order_item.item.inventory_quantity,
                    ),
                )
                for order_item in document.order_items
            ]
            return Order(
                id=document.id,
                external_id=document.external_id,
                client=client,
                created_at=document.created_at,
                updated_at=document.updated_at,
                is_cancelled=document.is_cancelled,
                order_items=order_items,
            )
        return None

    def save(self, order: Order) -> None:
        client_document = ClientDocument.objects.with_id(order.client.id)

        order_item_documents = []
        for order_item in order.order_items:
            item_document = ItemDocument.objects.with_id(order_item.item.id)

            order_item_document = OrderItemDocument(
                quantity=order_item.quantity, item=item_document
            ).save()

            order_item_documents.append(order_item_document)

        order_document = OrderDocument(
            id=order.id,
            external_id=order.external_id,
            client=client_document,
            created_at=order.created_at,
            updated_at=order.updated_at,
            is_cancelled=order.is_cancelled,
            order_items=order_item_documents,
        )
        order_document.save()
