import functools
import re
import unicodedata

from pydantic_mongo import ObjectIdField

from src.adapters.inbound.telegram_bot.presenter import TelegramBotPresenter
from src.domain.ports.inbound.items.dtos import (
    AddItemInputDTO,
    RemoveItemInputDTO,
    SetInventoryQuantitiesInputDTO,
    SetInventoryQuantityItemInputDTO,
)
from src.domain.ports.inbound.items.ports import (
    AddItemPort,
    ListItemsPort,
    RemoveItemPort,
    SetInventoryQuantitiesPort,
)
from src.domain.ports.inbound.orders.dtos import (
    CancelOrderInputDTO,
    CreateGoomerOrderInputDTO,
    CreateManualOrderInputDTO,
    OrderItemInputDTO,
)
from src.domain.ports.inbound.orders.ports import (
    CancelOrderPort,
    CreateGoomerOrderPort,
    CreateManualOrderPort,
)

ORDER_SECTIONS_DELIMITER = "---------------------------------------"


class TelegramBotController:
    def __init__(self):
        self._decorate_public_methods_with_error_catch()

    def _decorate_public_methods_with_error_catch(self):
        for attr_name in dir(self):
            if not attr_name.startswith("_"):
                attr = getattr(self, attr_name)
                if callable(attr):
                    setattr(self, attr_name, self._catch_errors(attr))

    def _catch_errors(self, func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                error_message = TelegramBotPresenter.map_error_to_message(e)
                print(f"Error in {func.__name__}: {error_message}")
                return error_message

        return wrapper

    @staticmethod
    def add_item(raw_input: str, add_item_use_case: AddItemPort) -> str:
        input_dto = TelegramBotController._extract_item(raw_input)
        output_dto = add_item_use_case.execute(input_dto)
        output_message = TelegramBotPresenter.format_add_item_message(
            output_dto
        )
        return output_message

    @staticmethod
    def list_items(list_items_use_case: ListItemsPort) -> str:
        output_dto = list_items_use_case.execute()
        output_message = TelegramBotPresenter.format_list_items_message(
            output_dto
        )
        return output_message

    @staticmethod
    def remove_item(
        raw_input: str, remove_item_use_case: RemoveItemPort
    ) -> str:
        raw_item_name = raw_input
        item_name = TelegramBotController._clean_text(raw_item_name)

        input_dto = RemoveItemInputDTO(item_name=item_name)
        output_dto = remove_item_use_case.execute(input_dto)
        output_message = TelegramBotPresenter.format_remove_item_message(
            output_dto
        )
        return output_message

    @staticmethod
    def set_inventory_quantities(
        raw_input: str,
        set_inventory_quantities_use_case: SetInventoryQuantitiesPort,
    ) -> str:
        items_input_dto = TelegramBotController._extract_items(raw_input)
        input_dto = SetInventoryQuantitiesInputDTO(items=items_input_dto)
        output_dto = set_inventory_quantities_use_case.execute(input_dto)
        output_message = (
            TelegramBotPresenter.format_set_inventory_quantities_message(
                output_dto
            )
        )
        return output_message

    @staticmethod
    def _extract_items(
        raw_input: str,
    ) -> list[SetInventoryQuantityItemInputDTO]:
        items_input_dto = []
        raw_items_names_and_inventory_quantities = raw_input.split("\n")
        for (
            raw_item_name_and_inventory_quantity
        ) in raw_items_names_and_inventory_quantities:
            inventory_quantity, raw_item_name = (
                raw_item_name_and_inventory_quantity.split(" ", 1)
            )
            item_name = TelegramBotController._clean_text(raw_item_name)
            items_input_dto.append(
                SetInventoryQuantityItemInputDTO(
                    item_name=item_name,
                    inventory_quantity=int(inventory_quantity),
                )
            )

        return items_input_dto

    @staticmethod
    def _extract_item(
        raw_input: str,
    ) -> AddItemInputDTO:
        inventory_quantity, raw_item_name = raw_input.split(" ", 1)
        item_name = TelegramBotController._clean_text(raw_item_name)
        return AddItemInputDTO(
            item_name=item_name,
            inventory_quantity=int(inventory_quantity),
        )

    @staticmethod
    def create_manual_order(
        raw_input: str, create_order_use_case: CreateManualOrderPort
    ) -> str:
        order_items = TelegramBotController._extract_manual_order_items(
            raw_input
        )

        input_dto = CreateManualOrderInputDTO(items=order_items)

        output_dto = create_order_use_case.execute(input_dto)
        output_message = (
            TelegramBotPresenter.format_create_manual_order_message(output_dto)
        )
        return output_message

    @staticmethod
    def _extract_manual_order_items(raw_input: str) -> list[OrderItemInputDTO]:
        raw_quantity_and_order_items = raw_input.split("\n")

        order_items = []
        for raw_quantity_and_order_item in raw_quantity_and_order_items:
            quantity, order_item = raw_quantity_and_order_item.split(" ", 1)
            order_items.append(
                OrderItemInputDTO(
                    item_name=TelegramBotController._clean_text(order_item),
                    quantity=int(quantity.strip()),
                )
            )

        if not order_items:
            raise ValueError("Order Items not found")

        return order_items

    @staticmethod
    def create_goomer_order(
        raw_input: str, create_order_use_case: CreateGoomerOrderPort
    ) -> str:
        raw_input_list = raw_input.split(ORDER_SECTIONS_DELIMITER)

        external_order_id = TelegramBotController._extract_external_order_id(
            raw_input_list[1]
        )
        order_items = TelegramBotController._extract_goomer_order_items(
            raw_input_list[2]
        )
        client_name = TelegramBotController._extract_client_name(
            raw_input_list[3]
        )
        created_at = TelegramBotController._extract_created_at(raw_input)

        input_dto = CreateGoomerOrderInputDTO(
            client_name=client_name,
            external_order_id=external_order_id,
            external_created_at=created_at,
            items=order_items,
        )

        output_dto = create_order_use_case.execute(input_dto)
        output_message = (
            TelegramBotPresenter.format_create_goomer_order_message(output_dto)
        )
        return output_message

    @staticmethod
    def _extract_external_order_id(order_metadata: str) -> int:
        external_order_id_match = re.search(
            r"Pedido Goomer Delivery #(\d+)", order_metadata
        )
        if not external_order_id_match:
            raise ValueError("External Order ID not found")
        return int(external_order_id_match.group(1))

    @staticmethod
    def _extract_goomer_order_items(raw_order_items_section: str) -> list:
        raw_order_items = raw_order_items_section.split("\n")
        filtered_raw_order_items = [
            item
            for item in raw_order_items
            if re.match(r"^\s*(?:\*\s*|\-\s*)\d+\s*x\b(?![^%]*%)", item)
        ]
        if not filtered_raw_order_items:
            raise ValueError("Order Items not found")

        order_items_to_quantity_map: dict[str, int] = {}
        for raw_order_item in filtered_raw_order_items:
            quantity = int(re.search(r"(\d+)x", raw_order_item).group(1))  # type: ignore
            item_name = raw_order_item.split("x", 1)[1].strip()
            if item_name in order_items_to_quantity_map:
                order_items_to_quantity_map[item_name] += quantity
            else:
                order_items_to_quantity_map[item_name] = quantity

        order_items = [
            OrderItemInputDTO(
                item_name=TelegramBotController._clean_text(item_name),
                quantity=quantity,
            )
            for item_name, quantity in order_items_to_quantity_map.items()
        ]
        return order_items

    @staticmethod
    def _extract_client_name(raw_client_info: str) -> str:
        client_name_match = re.search(r"\*(.*?)\*", raw_client_info)
        if not client_name_match:
            raise ValueError("Client Name not found")
        client_name = client_name_match.group(1).strip()
        return TelegramBotController._clean_text(client_name)

    @staticmethod
    def _extract_created_at(raw_input: str) -> str:
        created_at_match = re.search(r"às (\d{1,2}:\d{2})_", raw_input)
        if not created_at_match:
            raise ValueError("Created At not found")
        return created_at_match.group(1)

    @staticmethod
    def cancel_order(
        raw_input: str, cancel_order_use_case: CancelOrderPort
    ) -> str:
        order_id = raw_input
        input_dto = CancelOrderInputDTO(order_id=ObjectIdField(order_id))
        output_dto = cancel_order_use_case.execute(input_dto)
        output_message = TelegramBotPresenter.format_cancel_order_message(
            output_dto
        )
        return output_message

    @staticmethod
    def _remove_accents(input_str: str) -> str:
        # Normaliza a string para 'NFKD' que separará letras de seus acentos
        # Filtra para manter apenas caracteres que não são acentos
        nfkd_form = unicodedata.normalize("NFKD", input_str)
        return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

    @staticmethod
    def _adjust_commas(input_str: str) -> str:
        # Substitui vírgula seguida de espaço por vírgula sem espaço
        return re.sub(r",\s+", ",", input_str)

    @staticmethod
    def _remove_asterisks(input_str: str) -> str:
        # Remove asteriscos
        return input_str.replace("*", "")

    @staticmethod
    def _remove_multiple_spaces(input_str: str) -> str:
        # Substitui qualquer sequência de espaços em branco por um único espaço
        return re.sub(r"\s+", " ", input_str).strip()

    @staticmethod
    def _clean_text(input_str: str) -> str:
        return TelegramBotController._adjust_commas(
            TelegramBotController._remove_accents(
                TelegramBotController._remove_asterisks(
                    TelegramBotController._remove_multiple_spaces(
                        input_str.strip()
                    )
                )
            )
        ).lower()
