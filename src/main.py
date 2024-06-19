from multiprocessing import Process

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from telegram.ext import (
    Application,
)

from src.adapters.inbound.fastapi.controller import router as fastapi_router
from src.adapters.inbound.fastapi.presenter import FastAPIPresenter
from src.adapters.inbound.telegram_bot.bot import TelegramBotCommandHandler
from src.adapters.outbound.repositories.mongo.client import (
    MongoClientRepository,
)
from src.adapters.outbound.repositories.mongo.connection import (
    MongoConnection,
)
from src.adapters.outbound.repositories.mongo.item import MongoItemRepository
from src.adapters.outbound.repositories.mongo.order import MongoOrderRepository
from src.domain.exceptions import DomainException
from src.settings import settings

PORT = settings.PORT
TELEGRAM_BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
API_PORT = settings.API_PORT


def run_telegram_bot():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    connection = MongoConnection(
        settings.MONGO_CONNECTION_STRING,
    )
    connection.connect()

    item_repository = MongoItemRepository(connection)
    order_repository = MongoOrderRepository(connection)
    client_repository = MongoClientRepository(connection)
    telegram_bot_command_handler = TelegramBotCommandHandler(
        item_repository=item_repository,
        order_repository=order_repository,
        client_repository=client_repository,
    )

    application.add_handler(
        telegram_bot_command_handler.get_conversation_handler()
    )
    application.add_handler(
        telegram_bot_command_handler.get_callback_query_handler()
    )
    webhook_url = f"{settings.TELEGRAM_WEBHOOK_URL}/{TELEGRAM_BOT_TOKEN}"
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TELEGRAM_BOT_TOKEN,
        webhook_url=webhook_url,
    )


def build_api():
    fastapi_application = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
    )

    fastapi_application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    fastapi_application.add_exception_handler(
        DomainException,
        FastAPIPresenter.map_domain_exception,  # type: ignore
    )

    fastapi_application.include_router(fastapi_router)

    return fastapi_application


def run_api():
    fastapi_application = build_api()
    print(f"Will run fastapi_application: {fastapi_application}")
    uvicorn.run(fastapi_application, host="0.0.0.0", port=API_PORT)
    print(f"Ran fastapi_application: {fastapi_application}")


if __name__ == "__main__":
    telegram_process = Process(target=run_telegram_bot)
    telegram_process.start()

    api_process = Process(target=run_api)
    api_process.start()

    telegram_process.join()
    api_process.join()
