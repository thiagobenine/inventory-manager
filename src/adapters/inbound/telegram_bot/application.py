import os

from flask import Flask, request
from telegram import (
    Bot,
    Update,
)
from telegram.ext import (
    Application,
)

from src.adapters.inbound.telegram_bot.bot import TelegramBotCommandHandler

app = Flask(__name__)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(TOKEN)
application = Application.builder().token(TOKEN).build()


@app.route("/hook", methods=["POST"])
def webhook_handler():
    update = Update.de_json(request.json, bot)
    application.update_queue.put(update)
    return "ok"


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
        port=5000,
        url_path=TOKEN,
        webhook_url=webhook_url,
    )
