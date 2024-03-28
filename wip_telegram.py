import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

bot_token = os.environ["BOT_TOKEN"]
webhook_url = os.environ["WEBHOOK_URL"]


# Function to display the main menu
def start(update, context):
    keyboard = [
        [InlineKeyboardButton("Option 1", callback_data="option1")],
        [InlineKeyboardButton("Option 2", callback_data="option2")],
        [InlineKeyboardButton("Option 3", callback_data="option3")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Select an option:", reply_markup=reply_markup)


# Function to handle the selected options in the menu
def menu_actions(update, context):
    query = update.callback_query
    if query.data == "option1":
        query.edit_message_text(text="You selected Option 1")
    elif query.data == "option2":
        query.edit_message_text(text="You selected Option 2")
    elif query.data == "option3":
        query.edit_message_text(text="You selected Option 3")


# Function to handle unknown messages
def unknown(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Sorry, I didn't understand that command.",
    )


if __name__ == "__main__":
    # Create the Application object and configure the webhook
    application = Application.builder().token(bot_token).build()
    webhook_url = f"{webhook_url}/bot"
    application.bot.set_webhook(url=webhook_url)

    # Get the dispatcher object to register handlers
    dispatcher = application.dispatcher

    # Register the handlers
    start_handler = CommandHandler("start", start)
    menu_handler = CallbackQueryHandler(menu_actions)
    unknown_handler = MessageHandler(filters.command, unknown)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(menu_handler)
    dispatcher.add_handler(unknown_handler)

    # Start the webhook
    application.run_webhook(
        listen='0.0.0.0',
        port=int(os.environ.get('PORT', '8443')),
        url_path="bot",
        webhook_url=webhook_url
    )

    # Keep the program running
    application.idle()