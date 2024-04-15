import pytest

from src.adapters.outbound.mongo.documents.client import ClientDocument
from src.adapters.outbound.mongo.repositories.client import (
    MongoClientRepository,
)
from src.domain.entities.client import Client


class TestMongoClientRepository:
    @pytest.fixture
    def repository(self, mongo_connection):
        return MongoClientRepository(mongo_connection)

    def test_save_client(self, repository, mongo_connection):
        # Arrange
        test_client = Client(name="Maria Joaquina")

        # Act
        repository.save(test_client)

        # Assert
        saved_client = ClientDocument.objects().first()
        assert saved_client is not None
        assert saved_client.name == "Maria Joaquina"
        assert ClientDocument.objects.count() == 1

    def test_find_client_by_name(self, repository, mongo_connection):
        # Arrange
        ClientDocument(name="Carlos Magno").save()

        # Act
        found_client = repository.find_client_by_name("Carlos Magno")

        # Assert
        assert found_client.name == "Carlos Magno"
        assert ClientDocument.objects.count() == 1
