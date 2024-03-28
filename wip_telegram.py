import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)


# Função para exibir o menu principal
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Option 1", callback_data='option1')],
        [InlineKeyboardButton("Option 2", callback_data='option2')],
        [InlineKeyboardButton("Option 3", callback_data='option3')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Select an option:", reply_markup=reply_markup)

# Função para lidar com as opções selecionadas no menu
async def menu_actions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer() # É necessário responder ao CallbackQuery antes de editar a mensagem
    if query.data == 'option1':
        await query.edit_message_text(text="You selected Option 1")
    elif query.data == 'option2':
        await query.edit_message_text(text="You selected Option 2")
    elif query.data == 'option3':
        await query.edit_message_text(text="You selected Option 3")

# Função para lidar com mensagens desconhecidas
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

async def main():
    bot_token = os.environ["BOT_TOKEN"]
    webhook_url = os.environ["WEBHOOK_URL"]

    # Cria o objeto Application e configura o webhook
    application = Application.builder().token(bot_token).build()

    # Registra os handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(menu_actions))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    # Configura e inicia o webhook
    await application.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", "8443")),
        url_path=bot_token,
        webhook_url=webhook_url + bot_token
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
