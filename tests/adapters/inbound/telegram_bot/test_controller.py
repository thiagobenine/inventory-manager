from datetime import datetime

import pytest

from src.adapters.inbound.telegram_bot.controller import TelegramBotController
from src.adapters.outbound.repositories.mongo.client import (
    MongoClientRepository,
)
from src.adapters.outbound.repositories.mongo.item import MongoItemRepository
from src.adapters.outbound.repositories.mongo.order import MongoOrderRepository
from src.domain.entities.client import Client
from src.domain.entities.item import Item
from src.domain.entities.order import Order, OrderItem
from src.domain.use_cases.add_item import AddItemUseCase
from src.domain.use_cases.cancel_order import CancelOrderUseCase
from src.domain.use_cases.create_order import CreateOrderUseCase
from src.domain.use_cases.list_items import ListItemsUseCase
from src.domain.use_cases.remove_item import RemoveItemUseCase
from src.domain.use_cases.set_inventory_quantity import (
    SetInventoryQuantityUseCase,
)
from tests.adapters.inbound.telegram_bot.test_data import (
    CREATE_ORDER_TYPE_1_INPUT,
    CREATE_ORDER_TYPE_2_INPUT,
)


class TestTelegramBotController:
    @pytest.fixture
    def controller(self):
        return TelegramBotController()

    def test_add_item_controller_with_success(
        self, controller, mongo_connection
    ):
        # Arrange
        item_repository = MongoItemRepository(mongo_connection)
        raw_input = "ARROZ INTEGRAL E STROGONOFF DE CARNE,10"

        # Act
        output_message = controller.add_item(
            raw_input, AddItemUseCase(item_repository)
        )

        # Assert
        assert (
            output_message == "\nMarmita registrada com sucesso\\!"
            "\n\n*Nome:* Arroz integral e strogonoff de carne\n*Estoque:* 10\n"
        )

    def test_add_item_controller_with_error(
        self, controller, mongo_connection
    ):
        # Arrange
        item_repository = MongoItemRepository(mongo_connection)
        raw_input = "ARROZ INTEGRAL E STROGONOFF DE CARNE_10"

        # Act
        output_message = controller.add_item(
            raw_input, AddItemUseCase(item_repository)
        )

        # Assert
        assert output_message == "Ocorreu um erro inesperado\\."

    def test_list_items_controller_with_success(
        self, controller, mongo_connection
    ):
        # Arrange
        item_repository = MongoItemRepository(mongo_connection)
        test_item = Item(
            name="arroz integral e strogonoff de carne", inventory_quantity=100
        )
        item_repository.save(test_item)

        # Act
        output_message = controller.list_items(
            ListItemsUseCase(item_repository)
        )

        # Assert
        assert "Lista de Marmitas:\n\n" in output_message
        assert (
            "*Nome:* Arroz integral e strogonoff de carne\n" in output_message
        )
        assert "*Estoque:* 100\n" in output_message

    def test_remove_item_controller_with_success(
        self, controller, mongo_connection
    ):
        # Arrange
        item_repository = MongoItemRepository(mongo_connection)
        test_item = Item(
            name="arroz integral e strogonoff de carne", inventory_quantity=100
        )
        item_repository.save(test_item)
        raw_input = "arroz integral e strogonoff de carne"

        # Act
        output_message = controller.remove_item(
            raw_input, RemoveItemUseCase(item_repository)
        )

        # Assert
        assert (
            output_message == "\nMarmita removida com sucesso\\!"
            "\n\n*Nome:* Arroz integral e strogonoff de carne\n"
        )

    def test_remove_item_controller_with_error(
        self, controller, mongo_connection
    ):
        # Arrange
        item_repository = MongoItemRepository(mongo_connection)
        raw_input = "ARROZ INTEGRAL E STROGONOFF DE CARNE"
        # doesn't save the item

        # Act
        output_message = controller.remove_item(
            raw_input, RemoveItemUseCase(item_repository)
        )

        # Assert
        assert output_message == "Ocorreu um erro inesperado\\."

    def test_set_inventory_quantity_controller_with_success(
        self, controller, mongo_connection
    ):
        # Arrange
        item_repository = MongoItemRepository(mongo_connection)
        test_item = Item(
            name="arroz integral e strogonoff de carne", inventory_quantity=100
        )
        item_repository.save(test_item)
        raw_input = "arroz integral e strogonoff de carne,10"

        # Act
        output_message = controller.set_inventory_quantity(
            raw_input, SetInventoryQuantityUseCase(item_repository)
        )

        # Assert
        assert (
            output_message == "\nEstoque registrado com sucesso\\!"
            "\n\n*Nome:* Arroz integral e strogonoff de carne"
            "\n*Novo Estoque:* 10\n"
        )

    def test_set_inventory_quantity_controller_with_error(
        self, controller, mongo_connection
    ):
        # Arrange
        item_repository = MongoItemRepository(mongo_connection)
        raw_input = "ARROZ INTEGRAL E STROGONOFF DE CARNE,10"
        # doesn't save the item

        # Act
        output_message = controller.set_inventory_quantity(
            raw_input, SetInventoryQuantityUseCase(item_repository)
        )

        # Assert
        assert output_message == "Ocorreu um erro inesperado\\."

    @pytest.mark.parametrize(
        "raw_input",
        [CREATE_ORDER_TYPE_1_INPUT, CREATE_ORDER_TYPE_2_INPUT],
    )
    def test_create_order_controller_with_success(
        self, controller, mongo_connection, raw_input
    ):
        # Arrange
        order_repository = MongoOrderRepository(mongo_connection)

        item_repository = MongoItemRepository(mongo_connection)
        test_item = Item(
            name="pure de batata doce,hamburguer de frango e mix de legumes",
            inventory_quantity=100,
        )
        item_repository.save(test_item)

        client_repository = MongoClientRepository(mongo_connection)
        test_client = Client(name="Rafaela de Paula")
        client_repository.save(test_client)

        # Act
        output_message = controller.create_order(
            raw_input,
            CreateOrderUseCase(
                client_repository, item_repository, order_repository
            ),
        )

        # Assert
        assert "\nPedido registrado com sucesso\\!\n\n" in output_message
        assert "*ID do Pedido:*" in output_message
        assert "*Cliente:* Rafaela de paula" in output_message
        assert "*Marmitas:*" in output_message
        assert (
            "\\- *Nome:* Pure de batata doce,hamburguer de frango"
            " e mix de legumes" in output_message
        )
        assert "\\- *Quantidade no Pedido:* 2" in output_message
        assert "\\- *Novo Estoque:* 98" in output_message

    @pytest.mark.parametrize(
        "raw_input",
        [CREATE_ORDER_TYPE_1_INPUT, CREATE_ORDER_TYPE_2_INPUT],
    )
    def test_create_order_controller_with_error(
        self, controller, mongo_connection, raw_input
    ):
        # Arrange
        order_repository = MongoOrderRepository(mongo_connection)

        item_repository = MongoItemRepository(mongo_connection)
        # doesn't save the item

        client_repository = MongoClientRepository(mongo_connection)
        test_client = Client(name="Rafaela de Paula")
        client_repository.save(test_client)

        # Act
        output_message = controller.create_order(
            raw_input,
            CreateOrderUseCase(
                client_repository, item_repository, order_repository
            ),
        )

        # Assert
        assert output_message == "Ocorreu um erro inesperado\\."

    def test_cancel_order_controller_with_success(
        self, controller, mongo_connection
    ):
        # Arrange
        item_repository = MongoItemRepository(mongo_connection)
        test_item = Item(name="Marmita de Carne", inventory_quantity=5)
        item_repository.save(test_item)

        client_repository = MongoClientRepository(mongo_connection)
        test_client = Client(name="Joana")
        client_repository.save(test_client)

        order_repository = MongoOrderRepository(mongo_connection)
        test_order = Order(
            external_id=2,
            client=test_client,
            order_items=[OrderItem(quantity=1, item=test_item)],
            external_created_at="17:54",
            created_at=datetime(2023, 6, 7, 10, 0, 0),
            updated_at=datetime(2023, 6, 7, 10, 0, 0),
            is_cancelled=False,
        )
        order_repository.save(test_order)

        raw_input = test_order.id

        # Act
        output_message = controller.cancel_order(
            raw_input, CancelOrderUseCase(order_repository, item_repository)
        )

        # Assert
        assert "\nPedido cancelado com sucesso\\!\n\n" in output_message
        assert "*ID do Pedido:*" in output_message
        assert "*Cliente:* Joana" in output_message
        assert "*Marmitas:*" in output_message
        assert "\\- *Nome:* Marmita de carne" in output_message
        assert "\\- *Quantidade no Pedido:* 1" in output_message
        assert "\\- *Novo Estoque:* 6" in output_message

    def test_cancel_order_controller_with_error(
        self, controller, mongo_connection
    ):
        # Arrange
        item_repository = MongoItemRepository(mongo_connection)
        order_repository = MongoOrderRepository(mongo_connection)
        raw_input = "invalid_id"

        # Act
        output_message = controller.cancel_order(
            raw_input, CancelOrderUseCase(order_repository, item_repository)
        )

        # Assert
        assert output_message == "Ocorreu um erro inesperado\\."
