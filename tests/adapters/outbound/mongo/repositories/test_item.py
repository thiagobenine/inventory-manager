import pytest

from src.adapters.outbound.mongo.documents.item import ItemDocument
from src.adapters.outbound.mongo.repositories.item import MongoItemRepository
from src.domain.entities.item import Item


class TestMongoItemRepository:
    @pytest.fixture
    def repository(self, mongo_connection):
        return MongoItemRepository(mongo_connection)

    def test_save_item(self, repository):
        # Arrange
        test_item = Item(name="Marmita de Frango", inventory_quantity=10)

        # Act
        repository.save(test_item)

        # Assert
        saved_item = ItemDocument.objects().first()
        assert saved_item is not None
        assert saved_item.name == "Marmita de Frango"
        assert saved_item.inventory_quantity == 10
        assert ItemDocument.objects.count() == 1

    def test_find_item_by_name(self, repository):
        # Arrange
        ItemDocument(name="Marmita de Carne", inventory_quantity=5).save()

        # Act
        found_item = repository.find_item_by_name("Marmita de Carne")

        # Assert
        assert found_item is not None
        assert found_item.name == "Marmita de Carne"
        assert found_item.inventory_quantity == 5
        assert ItemDocument.objects.count() == 1

    def test_find_items_by_names(self, repository):
        # Arrange
        ItemDocument(name="Marmita de Peixe", inventory_quantity=3).save()
        ItemDocument(name="Marmita Vegana", inventory_quantity=4).save()

        # Act
        found_items = repository.find_items_by_names(
            ["Marmita de Peixe", "Marmita Vegana"]
        )

        # Assert
        assert len(found_items) == 2
        assert found_items[0].name == "Marmita de Peixe"
        assert found_items[0].inventory_quantity == 3
        assert found_items[1].name == "Marmita Vegana"
        assert found_items[1].inventory_quantity == 4
        assert ItemDocument.objects.count() == 2

    def test_remove_item_by_name(self, repository):
        # Arrange
        ItemDocument(name="Marmita de Carne", inventory_quantity=8).save()

        # Act
        repository.remove_item_by_name("Marmita de Carne")

        # Assert
        assert ItemDocument.objects.count() == 0

    def test_save_all_items(self, repository):
        # Arrange
        test_items = [
            Item(name="Marmita de Frango", inventory_quantity=2),
            Item(name="Marmita Vegana", inventory_quantity=6),
        ]

        # Act
        repository.save_all(test_items)

        # Assert
        saved_items = ItemDocument.objects()
        assert saved_items.count() == 2
        assert saved_items[0].name == "Marmita de Frango"
        assert saved_items[0].inventory_quantity == 2
        assert saved_items[1].name == "Marmita Vegana"
        assert saved_items[1].inventory_quantity == 6
