from src.domain.ports.inbound.items.dtos import (
    AddItemOutputDTO,
    ItemOutputDTO,
    ListItemsOutputDTO,
    RemoveItemOutputDTO,
    SetInventoryQuantityOutputDTO,
)
from src.domain.ports.inbound.orders.dtos import (
    CancelOrderItemOutputDTO,
    CancelOrderOutputDTO,
    CreateGoomerOrderOutputDTO,
    CreateManualOrderOutputDTO,
    CreateOrderItemOutputDTO,
)

CATEGORY_ITEM_NAME_MAP: dict[str, str] = {
    "Carne": "Marmitas de Carne",
    "Frango": "Marmitas de Frango",
    "Vegana": "Marmitas Veganas",
}


class TelegramBotPresenter:
    @staticmethod
    def format_add_item_message(output_dto: AddItemOutputDTO) -> str:
        output_message = "Marmita registrada com sucesso\\!\n\n"
        output_message += f"*Nome:* {output_dto.name.capitalize()}\n"
        output_message += f"*Estoque:* {output_dto.inventory_quantity}\n"
        return output_message

    @staticmethod
    def format_list_items_message(output_dto: ListItemsOutputDTO) -> str:
        meat_items, chicken_items, vegan_items = (
            TelegramBotPresenter._classify_items_by_category(output_dto.items)
        )

        output_message = "Lista de Marmitas:\n"
        output_message += TelegramBotPresenter._format_category_for_list_items(
            meat_items, "Carne"
        )
        output_message += TelegramBotPresenter._format_category_for_list_items(
            chicken_items, "Frango"
        )
        output_message += TelegramBotPresenter._format_category_for_list_items(
            vegan_items, "Vegana"
        )
        return output_message

    @staticmethod
    def _format_category_for_list_items(
        items: list[ItemOutputDTO], category_name: str
    ) -> str:
        if not items:
            return ""

        output_message = f"\n*{CATEGORY_ITEM_NAME_MAP[category_name]}:*\n"
        for item in items:
            item_name = item.item_name.capitalize()
            inventory_quantity = str(item.inventory_quantity).replace(
                "-", "\\-"
            )
            output_message += f"*Nome:* {item_name}\n"
            output_message += f"*Estoque:* {inventory_quantity}\n"
        return output_message

    @staticmethod
    def format_remove_item_message(output_dto: RemoveItemOutputDTO) -> str:
        output_message = "Marmita removida com sucesso\\!\n\n"
        output_message += f"*Nome:* {output_dto.item_name.capitalize()}"
        return output_message

    @staticmethod
    def format_set_inventory_quantity_message(
        output_dto: SetInventoryQuantityOutputDTO,
    ) -> str:
        output_message = "Estoque registrado com sucesso\\!\n\n"
        output_message += f"*Nome:* {output_dto.item_name.capitalize()}\n"
        output_message += f"*Novo Estoque:* {output_dto.inventory_quantity}"
        return output_message

    @staticmethod
    def format_create_manual_order_message(
        output_dto: CreateManualOrderOutputDTO,
    ) -> str:
        meat_items, chicken_items, vegan_items = (
            TelegramBotPresenter._classify_items_by_category(
                output_dto.order_items
            )
        )

        output_message = "Pedido registrado com sucesso\\!\n\n"
        output_message += f"*ID do Pedido:* {output_dto.order_id}\n"
        output_message += "*Marmitas:*\n\n"

        output_message += (
            TelegramBotPresenter._format_category_for_order_items(
                meat_items, "Carne"
            )
        )
        output_message += (
            TelegramBotPresenter._format_category_for_order_items(
                chicken_items, "Frango"
            )
        )
        output_message += (
            TelegramBotPresenter._format_category_for_order_items(
                vegan_items, "Vegana"
            )
        )
        return output_message

    @staticmethod
    def format_create_goomer_order_message(
        output_dto: CreateGoomerOrderOutputDTO,
    ) -> str:
        meat_items, chicken_items, vegan_items = (
            TelegramBotPresenter._classify_items_by_category(
                output_dto.order_items
            )
        )

        output_message = "Pedido registrado com sucesso\\!\n\n"
        output_message += f"*ID do Pedido:* {output_dto.order_id}\n"
        output_message += f"*Cliente:* {output_dto.client_name.capitalize()}\n"
        output_message += "*Marmitas:*\n\n"

        output_message += (
            TelegramBotPresenter._format_category_for_order_items(
                meat_items, "Carne"
            )
        )
        output_message += (
            TelegramBotPresenter._format_category_for_order_items(
                chicken_items, "Frango"
            )
        )
        output_message += (
            TelegramBotPresenter._format_category_for_order_items(
                vegan_items, "Vegana"
            )
        )
        return output_message

    @staticmethod
    def format_cancel_order_message(
        output_dto: CancelOrderOutputDTO,
    ) -> str:
        vegan_items = []
        meat_items = []
        chicken_items = []

        for item in output_dto.order_items:
            if '"carne"' in item.item_name or '"frango"' in item.item_name:
                vegan_items.append(item)
            elif "carne" in item.item_name:
                meat_items.append(item)
            elif "frango" in item.item_name:
                chicken_items.append(item)

        output_message = "Pedido cancelado com sucesso\\!\n\n"
        output_message += f"*ID do Pedido:* {output_dto.order_id}\n"

        if output_dto.client_name:
            output_message += (
                f"*Cliente:* {output_dto.client_name.capitalize()}\n"
            )

        output_message += "*Marmitas:*\n\n"

        output_message += (
            TelegramBotPresenter._format_category_for_order_items(
                meat_items, "Carne"
            )
        )
        output_message += (
            TelegramBotPresenter._format_category_for_order_items(
                chicken_items, "Frango"
            )
        )
        output_message += (
            TelegramBotPresenter._format_category_for_order_items(
                vegan_items, "Vegana"
            )
        )
        return output_message

    @staticmethod
    def _format_category_for_order_items(
        items: list[CreateOrderItemOutputDTO] | list[CancelOrderItemOutputDTO],
        category_name: str,
    ) -> str:
        if not items:
            return ""

        output_message = f"*{CATEGORY_ITEM_NAME_MAP[category_name]}:*\n"
        for item in items:
            item_name = item.item_name.capitalize()
            item_quantity = item.quantity
            inventory_quantity = str(item.inventory_quantity).replace(
                "-", "\\-"
            )
            output_message += f"  \\- *Nome:* {item_name}\n"
            output_message += (
                f"  \\- *Quantidade no Pedido:* {item_quantity}\n"
            )
            output_message += f"  \\- *Novo Estoque:* {inventory_quantity}\n\n"

        return output_message

    @staticmethod
    def _classify_items_by_category(items):
        meat_items = []
        chicken_items = []
        vegan_items = []

        for item in items:
            if '"carne"' in item.item_name or '"frango"' in item.item_name:
                vegan_items.append(item)
            elif "carne" in item.item_name:
                meat_items.append(item)
            elif "frango" in item.item_name:
                chicken_items.append(item)

        return meat_items, chicken_items, vegan_items
