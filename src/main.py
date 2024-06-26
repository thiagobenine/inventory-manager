import os

from src.adapters.inbound.telegram_bot.application import run_application
from src.adapters.inbound.telegram_bot.bot import TelegramBotCommandHandler
from src.adapters.outbound.repositories.mongo.client import (
    MongoClientRepository,
)
from src.adapters.outbound.repositories.mongo.connection import (
    MongoConnection,
)
from src.adapters.outbound.repositories.mongo.item import MongoItemRepository
from src.adapters.outbound.repositories.mongo.order import MongoOrderRepository

if __name__ == "__main__":
    connection = MongoConnection(
        os.getenv("MONGO_CONNECTION_STRING", "mongodb://localhost:27017")
    )
    connection.connect()

    item_repository = MongoItemRepository(connection)
    order_repository = MongoOrderRepository(connection)
    client_repository = MongoClientRepository(connection)

    telegram_bot = TelegramBotCommandHandler(
        item_repository=item_repository,
        order_repository=order_repository,
        client_repository=client_repository,
    )
    run_application(telegram_bot_command_handler=telegram_bot)
