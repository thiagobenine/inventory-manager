from mongoengine import connect, disconnect
import mongomock


class MongoConnection:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self, connection_string: str, db_name: str,
    ):
        if not hasattr(self, "_is_initialized"):
            self.connection_string = connection_string
            self.db_name = db_name
            self._is_initialized = True
            self._is_connected = False

    def connect(self):
        if not self._is_connected:
            connect(db=self.db_name, host=self.connection_string)
            self._is_connected = True

    def close(self):
        if self._is_connected:
            disconnect()
            self._is_connected = False

class MongoMockConnection:
    def __init__(self, connection_string: str, db_name: str):
        self.connection_string = connection_string
        self.db_name = db_name
        self._is_connected = False

    def connect(self):
        if not self._is_connected:
            connect(
                db=self.db_name,
                host=self.connection_string,
                mongo_client_class=mongomock.MongoClient,
            )
            self._is_connected = True

    def close(self):
        if self._is_connected:
            disconnect()
            self._is_connected = False