import pytest

from src.adapters.outbound.repositories.mongo.client import (
    MongoClientRepository,
)
from src.adapters.outbound.repositories.mongo.item import MongoItemRepository
from src.domain.entities.client import Client
from src.domain.entities.item import Item

pytestmark = pytest.mark.asyncio


class TestFastAPIController:
    async def test_add_item_with_success(
        self,
        fastapi_client,
    ):
        # Act
        response = await fastapi_client.post(
            "/items",
            json={
                "item_name": "item_name",
                "inventory_quantity": 1,
            },
        )

        # Assert
        assert response.status_code == 201
        assert response.json() == {
            "item_name": "item_name",
            "inventory_quantity": 1,
        }

    async def test_add_item_raises_409_when_item_already_exists(
        self,
        fastapi_client,
        mongo_connection,
    ):
        # Arrange
        item_repository = MongoItemRepository(mongo_connection)
        test_item = Item(name="item_name", inventory_quantity=100)
        item_repository.save(test_item)

        # Act
        response = await fastapi_client.post(
            "/items",
            json={
                "item_name": "item_name",
                "inventory_quantity": 10,
            },
        )

        # Assert
        assert response.status_code == 409
        assert response.json() == {"detail": "Item already exists: item_name"}

    async def test_list_items_with_success(
        self,
        fastapi_client,
        mongo_connection,
    ):
        # Arrange
        item_repository = MongoItemRepository(mongo_connection)
        test_item = Item(name="item_name", inventory_quantity=100)
        item_repository.save(test_item)

        # Act
        response = await fastapi_client.get("/items")

        # Assert
        assert response.status_code == 200
        assert response.json() == {
            "items": [
                {
                    "item_name": "item_name",
                    "inventory_quantity": 100,
                }
            ]
        }

    async def test_set_inventory_quantities_with_success(
        self,
        fastapi_client,
        mongo_connection,
    ):
        # Arrange
        item_repository = MongoItemRepository(mongo_connection)
        test_item = Item(name="item_name", inventory_quantity=100)
        item_repository.save(test_item)

        # Act
        response = await fastapi_client.patch(
            "/items",
            json={
                "items": [
                    {
                        "item_name": "item_name",
                        "inventory_quantity": 10,
                    }
                ]
            },
        )

        # Assert
        assert response.status_code == 200
        assert response.json() == {
            "items": [
                {
                    "item_name": "item_name",
                    "inventory_quantity": 10,
                }
            ]
        }

    async def test_set_inventory_quantities_raises_404_when_item_does_not_exist(  # noqa
        self,
        fastapi_client,
    ):
        # Act
        response = await fastapi_client.patch(
            "/items",
            json={
                "items": [
                    {
                        "item_name": "item_name",
                        "inventory_quantity": 10,
                    }
                ]
            },
        )

        # Assert
        assert response.status_code == 404
        assert response.json() == {
            "detail": "Items not found by names: ['item_name']"
        }

    async def test_remove_item_with_success(
        self,
        fastapi_client,
        mongo_connection,
    ):
        # Arrange
        item_repository = MongoItemRepository(mongo_connection)
        test_item = Item(name="item_name", inventory_quantity=100)
        item_repository.save(test_item)

        # Act
        response = await fastapi_client.request(
            method="DELETE",
            url="http://localhost/items",
            json={
                "item_name": "item_name",
            },
        )

        # Assert
        assert response.status_code == 200
        assert response.json() == {
            "item_name": "item_name",
        }

    async def test_remove_item_raises_404_when_item_does_not_exist(
        self,
        fastapi_client,
    ):
        # Act
        response = await fastapi_client.request(
            method="DELETE",
            url="http://localhost/items",
            json={
                "item_name": "item_name",
            },
        )

        # Assert
        assert response.status_code == 404
        assert response.json() == {
            "detail": "Item not found by name: item_name"
        }

    async def test_create_goomer_order_with_success(
        self,
        fastapi_client,
        mongo_connection,
    ):
        # Arrange
        item_repository = MongoItemRepository(mongo_connection)
        test_item = Item(
            name="item_name",
            inventory_quantity=100,
        )
        item_repository.save(test_item)

        client_repository = MongoClientRepository(mongo_connection)
        test_client = Client(name="client_name")
        client_repository.save(test_client)

        # Act
        response = await fastapi_client.post(
            "/orders/goomer",
            json={
                "client_name": "client_name",
                "external_order_id": 10,
                "external_created_at": "12:00",
                "items": [
                    {
                        "item_name": "item_name",
                        "quantity": 10,
                    }
                ],
            },
        )

        # Assert
        assert response.status_code == 201
        response_json = response.json()
        assert response_json["client_name"] == "client_name"
        assert response_json["external_order_id"] == 10
        assert response_json["order_items"] == [
            {
                "item_name": "item_name",
                "quantity": 10,
                "inventory_quantity": 90,
            }
        ]

    async def test_create_goomer_order_raises_404_when_item_does_not_exist(
        self,
        fastapi_client,
    ):
        # Act
        response = await fastapi_client.post(
            "/orders/goomer",
            json={
                "client_name": "client_name",
                "external_order_id": 10,
                "external_created_at": "12:00",
                "items": [
                    {
                        "item_name": "item_name",
                        "quantity": 10,
                    }
                ],
            },
        )

        # Assert
        assert response.status_code == 404
        assert response.json() == {
            "detail": "Items not found by names: ['item_name']"
        }

    async def test_create_manual_order_with_success(
        self,
        fastapi_client,
        mongo_connection,
    ):
        # Arrange
        item_repository = MongoItemRepository(mongo_connection)
        test_item = Item(
            name="item_name",
            inventory_quantity=100,
        )
        item_repository.save(test_item)

        # Act
        response = await fastapi_client.post(
            "/orders/manual",
            json={
                "items": [
                    {
                        "item_name": "item_name",
                        "quantity": 10,
                    }
                ],
            },
        )

        # Assert
        assert response.status_code == 201
        response_json = response.json()
        assert response_json["order_items"] == [
            {
                "item_name": "item_name",
                "quantity": 10,
                "inventory_quantity": 90,
            }
        ]

    async def test_create_manual_order_raises_404_when_item_does_not_exist(
        self,
        fastapi_client,
    ):
        # Act
        response = await fastapi_client.post(
            "/orders/manual",
            json={
                "items": [
                    {
                        "item_name": "item_name",
                        "quantity": 10,
                    }
                ],
            },
        )

        # Assert
        assert response.status_code == 404
        assert response.json() == {
            "detail": "Items not found by names: ['item_name']"
        }
