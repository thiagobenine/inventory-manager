import pytest

from src.adapters.outbound.repositories.mongo.connection import (
    MongoMockConnection,
)


@pytest.fixture(scope="function")
def mongo_connection():
    connection = MongoMockConnection(
        "mongodb://localhost",
        "testdb",
    )
    connection.connect()
    yield connection
    connection.close()