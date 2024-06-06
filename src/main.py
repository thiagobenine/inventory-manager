from contextvars import ContextVar
import os
from myloglib.factories.logger_factory import LoggerFactory
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

import uuid
from contextvars import ContextVar

NO_CORRELATION = "NO_CORRELATION"

class CorrelationEntity:
    id: str

    __slots__ = ("id",)

    def __init__(self, value: str | None = "") -> None:
        self.id = value or str(uuid.uuid4())


_context: ContextVar[CorrelationEntity] = ContextVar(
    "correlation_other", default=CorrelationEntity(NO_CORRELATION)
)


class Correlation:
    HEADER_KEY = "X-Correlation-ID"

    @classmethod
    def get_id(cls) -> str:
        return _context.get().id

    @staticmethod
    def set_id(value: str | None) -> None:
        _context.set(CorrelationEntity(value))

    @classmethod
    def build_header(cls) -> dict[str, str]:
        return {cls.HEADER_KEY: cls.get_id()}


if __name__ == "__main__":
    logger = LoggerFactory.build_default_logger("test_logger", Correlation)
    Correlation.set_id("9999")

    logger.info("Starting application 10")
    connection = MongoConnection(
        os.getenv("MONGO_CONNECTION_STRING"),
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
