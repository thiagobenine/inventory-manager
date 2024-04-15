from src.adapters.outbound.mongo.connection import MongoConnection
from src.adapters.outbound.mongo.documents.client import ClientDocument
from src.domain.entities.client import Client


class MongoClientRepository:
    def __init__(self, mongo_connection: MongoConnection):
        mongo_connection.connect()

    def find_client_by_name(self, client_name: str) -> Client:
        document = ClientDocument.objects(name=client_name).first()
        if document:
            return Client(name=document.name, id=document.id)
        return None

    def save(self, client: Client) -> None:
        client_doc = ClientDocument(id=client.id, name=client.name)
        client_doc.save()
