import os

from telegram.ext import (
    Application,
)

from src.adapters.inbound.telegram_bot.bot import TelegramBotCommandHandler

PORT = int(os.environ.get("PORT", 5000))
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "fake")
application = Application.builder().token(TOKEN).build()


def run_application(telegram_bot_command_handler: TelegramBotCommandHandler):
    application.add_handler(
        telegram_bot_command_handler.get_conversation_handler()
    )
    application.add_handler(
        telegram_bot_command_handler.get_callback_query_handler()
    )
    webhook_url = f"{os.getenv('TELEGRAM_WEBHOOK_URL')}/{TOKEN}"
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=webhook_url,
    )
