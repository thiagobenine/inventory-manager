from datetime import datetime

import pytest
from freezegun import freeze_time

from src.adapters.outbound.repositories.mongo.documents.client import (
    ClientDocument,
)
from src.adapters.outbound.repositories.mongo.documents.item import (
    ItemDocument,
)
from src.adapters.outbound.repositories.mongo.documents.order import (
    OrderDocument,
)
from src.adapters.outbound.repositories.mongo.documents.order_item import (
    OrderItemDocument,
)
from src.adapters.outbound.repositories.mongo.order import MongoOrderRepository
from src.domain.entities.client import Client
from src.domain.entities.item import Item
from src.domain.entities.order import Order, OrderItem


class TestMongoOrderRepository:
    @pytest.fixture
    def repository(self, mongo_connection):
        return MongoOrderRepository(mongo_connection)

    @freeze_time("2023-06-07 10:00:00")
    def test_save_order(self, repository, mongo_connection):
        # Arrange
        test_client = ClientDocument(name="Carlos").save()
        test_item = ItemDocument(
            name="Marmita de Frango", inventory_quantity=10
        ).save()
        test_order_item = OrderItem(
            quantity=2,
            item=Item(
                id=test_item.id,
                name=test_item.name,
                inventory_quantity=test_item.inventory_quantity,
            ),
        )
        test_order = Order(
            external_id=1,
            client=Client(id=test_client.id, name=test_client.name),
            order_items=[test_order_item],
            external_created_at="17:54",
            created_at=datetime(2023, 6, 7, 10, 0, 0),
            updated_at=datetime(2023, 6, 7, 10, 0, 0),
            is_cancelled=False,
        )

        # Act
        repository.save(test_order)

        # Assert
        saved_order = OrderDocument.objects().first()
        assert saved_order is not None
        assert saved_order.external_id == 1
        assert saved_order.client.id == test_client.id
        assert saved_order.client.name == "Carlos"
        assert saved_order.external_created_at == "17:54"
        assert saved_order.created_at == datetime(2023, 6, 7, 10, 0, 0)
        assert saved_order.updated_at == datetime(2023, 6, 7, 10, 0, 0)
        assert len(saved_order.order_items) == 1
        assert saved_order.order_items[0].quantity == 2
        assert saved_order.order_items[0].item.id == test_item.id
        assert saved_order.order_items[0].item.name == "Marmita de Frango"
        assert saved_order.order_items[0].item.inventory_quantity == 10
        assert OrderDocument.objects.count() == 1

    @freeze_time("2023-06-07 10:00:00")
    def test_find_order_by_id(self, repository, mongo_connection):
        # Arrange
        test_client = ClientDocument(name="Joana").save()
        test_item = ItemDocument(
            name="Marmita de Carne", inventory_quantity=5
        ).save()
        test_order_item = OrderItemDocument(quantity=1, item=test_item).save()
        test_order = OrderDocument(
            external_id=2,
            client=test_client,
            order_items=[test_order_item],
            external_created_at="17:54",
            created_at=datetime(2023, 6, 7, 10, 0, 0),
            updated_at=datetime(2023, 6, 7, 10, 0, 0),
            is_cancelled=False,
        ).save()

        # Act
        found_order = repository.find_order_by_id(test_order.id)

        # Assert
        assert found_order is not None
        assert found_order.id == test_order.id
        assert found_order.external_id == 2
        assert found_order.client.id == test_client.id
        assert found_order.client.name == "Joana"
        assert found_order.external_created_at == "17:54"
        assert found_order.created_at == datetime(2023, 6, 7, 10, 0, 0)
        assert found_order.updated_at == datetime(2023, 6, 7, 10, 0, 0)
        assert len(found_order.order_items) == 1
        assert found_order.order_items[0].quantity == 1
        assert found_order.order_items[0].item.id == test_item.id
        assert found_order.order_items[0].item.name == "Marmita de Carne"
        assert found_order.order_items[0].item.inventory_quantity == 5
        assert OrderDocument.objects.count() == 1
