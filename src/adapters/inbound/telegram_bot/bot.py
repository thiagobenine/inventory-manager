# mypy: ignore-errors
from enum import Enum

from telegram import (
    ForceReply,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    MaybeInaccessibleMessage,
    Update,
)
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from src.adapters.inbound.telegram_bot.controller import TelegramBotController
from src.domain.ports.outbound.repositories.client import (
    ClientRepositoryInterface,
)
from src.domain.ports.outbound.repositories.item import ItemRepositoryInterface
from src.domain.ports.outbound.repositories.order import (
    OrderRepositoryInterface,
)
from src.domain.use_cases.add_item import AddItemUseCase
from src.domain.use_cases.cancel_order import CancelOrderUseCase
from src.domain.use_cases.create_goomer_order import CreateGoomerOrderUseCase
from src.domain.use_cases.create_manual_order import CreateManualOrderUseCase
from src.domain.use_cases.list_items import ListItemsUseCase
from src.domain.use_cases.remove_item import RemoveItemUseCase
from src.domain.use_cases.set_inventory_quantities import (
    SetInventoryQuantitiesUseCase,
)


class ConversationState(int, Enum):
    WAITING_OPTION = 0
    WAITING_ADD_ITEM = 1
    WAITING_REMOVE_ITEM = 2
    WAITING_SET_INVENTORY_QUANTITIES = 3
    WAITING_CREATE_GOOMER_ORDER = 4
    WAITING_CANCEL_ORDER = 5
    WAITING_CREATE_MANUAL_ORDER = 6


class TelegramBotCommandHandler:
    def __init__(
        self,
        item_repository: ItemRepositoryInterface,
        order_repository: OrderRepositoryInterface,
        client_repository: ClientRepositoryInterface,
    ):
        self.item_repository = item_repository
        self.order_repository = order_repository
        self.client_repository = client_repository
        self.telegram_bot_controller = TelegramBotController()

    async def start_command(
        self, update: Update, context: ContextTypes = ContextTypes.DEFAULT_TYPE
    ) -> int:
        keyboard = [
            [
                InlineKeyboardButton(
                    "Registrar Nova Marmita", callback_data="add_item"
                )
            ],
            [
                InlineKeyboardButton(
                    "Listar Marmitas", callback_data="list_items"
                )
            ],
            [
                InlineKeyboardButton(
                    "Remover Marmita", callback_data="remove_item"
                )
            ],
            [
                InlineKeyboardButton(
                    "Registrar Estoque",
                    callback_data="set_inventory_quantities",
                )
            ],
            [
                InlineKeyboardButton(
                    "Registrar Pedido (Goomer)",
                    callback_data="create_goomer_order",
                )
            ],
            [
                InlineKeyboardButton(
                    "Registrar Pedido (Manual)",
                    callback_data="create_manual_order",
                )
            ],
            [
                InlineKeyboardButton(
                    "Cancelar Pedido", callback_data="cancel_order"
                )
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "Escolha uma opção:", reply_markup=reply_markup
        )
        return ConversationState.WAITING_OPTION

    async def handle_option(  # noqa: C901
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        query = update.callback_query
        await query.answer()
        if query.data == "add_item":
            await query.message.reply_text(
                "Você escolheu registrar uma nova marmita. "
                "\nEnvie os dados da marmita no seguinte formato:"
                "\nestoque nome"
                "\n\nExemplo: 10 ARROZ INTEGRAL E STROGONOFF DE CARNE",
                reply_markup=ForceReply(selective=True),
            )
            return ConversationState.WAITING_ADD_ITEM
        elif query.data == "list_items":
            await self.handle_list_items(query.message)
            return ConversationHandler.END
        elif query.data == "remove_item":
            await query.message.reply_text(
                "Você escolheu remover uma marmita. "
                "Envie o nome da marmita que deseja remover."
                "\n\nExemplo: ARROZ INTEGRAL E STROGONOFF DE CARNE",
                reply_markup=ForceReply(selective=True),
            )
            return ConversationState.WAITING_REMOVE_ITEM
        elif query.data == "set_inventory_quantities":
            await query.message.reply_text(
                "Você escolheu registrar o estoque.\n"
                "Envie o nome da(s) marmita(s) e a(s) "
                "quantidade(s) em estoque no seguinte formato:"
                "\nestoque nome"
                "\n\nExemplo: 10 ARROZ INTEGRAL E STROGONOFF DE CARNE",
                reply_markup=ForceReply(selective=True),
            )
            return ConversationState.WAITING_SET_INVENTORY_QUANTITIES
        elif query.data == "create_goomer_order":
            await query.message.reply_text(
                "Você escolheu registrar um pedido feito pelo Goomer. "
                "Envie os dados do pedido.",
                reply_markup=ForceReply(selective=True),
            )
            return ConversationState.WAITING_CREATE_GOOMER_ORDER
        elif query.data == "create_manual_order":
            await query.message.reply_text(
                "Você escolheu registrar um pedido feito manualmente. "
                "Envie os dados do pedido.",
                reply_markup=ForceReply(selective=True),
            )
            return ConversationState.WAITING_CREATE_MANUAL_ORDER
        elif query.data == "cancel_order":
            await query.message.reply_text(
                "Você escolheu cancelar um pedido. Envie o ID do pedido. "
                "\n\nExemplo: 662b23f05e0fe3996cc41e6c",
                reply_markup=ForceReply(selective=True),
            )
            return ConversationState.WAITING_CANCEL_ORDER
        else:
            await query.message.reply_text("Opção desconhecida.")
            return ConversationHandler.END

    async def handle_add_item(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        raw_input = update.message.text
        print(f"Raw input: {raw_input}")

        add_item_use_case = AddItemUseCase(self.item_repository)
        output_message = self.telegram_bot_controller.add_item(
            raw_input, add_item_use_case
        )

        await update.message.reply_text(
            output_message,
            parse_mode="MarkdownV2",
        )

        return ConversationHandler.END

    async def handle_list_items(
        self, message: MaybeInaccessibleMessage
    ) -> int:
        list_items_use_case = ListItemsUseCase(self.item_repository)
        output_message = self.telegram_bot_controller.list_items(
            list_items_use_case
        )

        await message.reply_text(
            output_message,
            parse_mode="MarkdownV2",
        )

        return ConversationHandler.END

    async def handle_remove_item(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        raw_input = update.message.text
        print(f"Raw input: {raw_input}")

        remove_item_use_case = RemoveItemUseCase(self.item_repository)
        output_message = self.telegram_bot_controller.remove_item(
            raw_input, remove_item_use_case
        )

        await update.message.reply_text(
            output_message,
            parse_mode="MarkdownV2",
        )
        return ConversationHandler.END

    async def handle_set_inventory_quantities(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        raw_input = update.message.text
        print(f"Raw input: {raw_input}")

        set_inventory_quantities_use_case = SetInventoryQuantitiesUseCase(
            self.item_repository
        )
        output_message = self.telegram_bot_controller.set_inventory_quantities(
            raw_input, set_inventory_quantities_use_case
        )

        await update.message.reply_text(
            output_message,
            parse_mode="MarkdownV2",
        )
        return ConversationHandler.END

    async def handle_create_goomer_order(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        raw_input = update.message.text
        print(f"Raw input: {raw_input}")

        create_goomer_order_use_case = CreateGoomerOrderUseCase(
            self.client_repository, self.item_repository, self.order_repository
        )
        output_message = self.telegram_bot_controller.create_goomer_order(
            raw_input, create_goomer_order_use_case
        )

        await update.message.reply_text(
            output_message,
            parse_mode="MarkdownV2",
        )
        return ConversationHandler.END

    async def handle_create_manual_order(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        raw_input = update.message.text
        print(f"Raw input: {raw_input}")

        create_manual_order_use_case = CreateManualOrderUseCase(
            self.item_repository, self.order_repository
        )
        output_message = self.telegram_bot_controller.create_manual_order(
            raw_input, create_manual_order_use_case
        )

        await update.message.reply_text(
            output_message,
            parse_mode="MarkdownV2",
        )
        return ConversationHandler.END

    async def handle_cancel_order(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        raw_input = update.message.text
        print(f"Raw input: {raw_input}")

        cancel_order_use_case = CancelOrderUseCase(
            self.order_repository, self.item_repository
        )
        output_message = self.telegram_bot_controller.cancel_order(
            raw_input, cancel_order_use_case
        )

        await update.message.reply_text(
            output_message,
            parse_mode="MarkdownV2",
        )
        return ConversationHandler.END

    def get_conversation_handler(self):
        return ConversationHandler(
            entry_points=[CommandHandler("start", self.start_command)],
            states={
                ConversationState.WAITING_OPTION: [
                    CallbackQueryHandler(self.handle_option)
                ],
                ConversationState.WAITING_ADD_ITEM: [
                    MessageHandler(
                        filters.TEXT & ~filters.COMMAND, self.handle_add_item
                    )
                ],
                ConversationState.WAITING_REMOVE_ITEM: [
                    MessageHandler(
                        filters.TEXT & ~filters.COMMAND,
                        self.handle_remove_item,
                    )
                ],
                ConversationState.WAITING_SET_INVENTORY_QUANTITIES: [
                    MessageHandler(
                        filters.TEXT & ~filters.COMMAND,
                        self.handle_set_inventory_quantities,
                    )
                ],
                ConversationState.WAITING_CREATE_GOOMER_ORDER: [
                    MessageHandler(
                        filters.TEXT & ~filters.COMMAND,
                        self.handle_create_goomer_order,
                    )
                ],
                ConversationState.WAITING_CREATE_MANUAL_ORDER: [
                    MessageHandler(
                        filters.TEXT & ~filters.COMMAND,
                        self.handle_create_manual_order,
                    )
                ],
                ConversationState.WAITING_CANCEL_ORDER: [
                    MessageHandler(
                        filters.TEXT & ~filters.COMMAND,
                        self.handle_cancel_order,
                    )
                ],
            },
            fallbacks=[CommandHandler("start", self.start_command)],
        )

    def get_callback_query_handler(self):
        return CallbackQueryHandler(self.handle_option)
