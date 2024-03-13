from unittest.mock import Mock, call

import pytest

from domain.entities.item import Item
from domain.exceptions import ClientNotFoundError, ItemNotFoundError
from domain.use_cases.create_order.create_order import CreateOrderUseCase
from domain.use_cases.create_order.dtos import (
    CreateOrderInputDTO,
    CreateOrderOutputDTO,
    OrderItemInputDTO,
)
from src.domain.entities.client import Client


class TestCreateOrderUseCase:
    @pytest.fixture
    def client_repository(self):
        return Mock()

    @pytest.fixture
    def item_repository(self):
        return Mock()

    @pytest.fixture
    def order_repository(self):
        return Mock()

    @pytest.fixture
    def client(self):
        return Client(name="Tirulipa", id=1)

    @pytest.fixture
    def item_1(self):
        return Item(name="Item 1", inventory_quantity=10)

    @pytest.fixture
    def item_2(self):
        return Item(name="Item 2", inventory_quantity=5)

    def test_create_order_use_case_with_success(
        self, client_repository, item_repository, order_repository, client, item_1, item_2
    ):
        # Arrange
        client_repository.find_client_by_name.return_value = client
        item_repository.find_item_by_name.side_effect = [item_1, item_2]

        input_dto = CreateOrderInputDTO(
            client_name="Tirulipa",
            external_order_id=1234,
            created_at="2023-06-07T10:00:00",
            items=[
                OrderItemInputDTO(item_name="Item 1", quantity=2),
                OrderItemInputDTO(item_name="Item 2", quantity=3),
            ],
        )

        use_case = CreateOrderUseCase(client_repository, item_repository, order_repository)

        # Act
        output_dto = use_case.execute(input_dto)

        # Assert
        assert isinstance(output_dto, CreateOrderOutputDTO)
        assert output_dto.client_name == "Tirulipa"
        assert output_dto.external_order_id == 1234
        assert len(output_dto.order_items) == 2
        assert output_dto.order_items[0].item_name == "Item 1"
        assert output_dto.order_items[0].quantity == 2
        assert output_dto.order_items[0].inventory_quantity == 8
        assert output_dto.order_items[1].item_name == "Item 2"
        assert output_dto.order_items[1].quantity == 3
        assert output_dto.order_items[1].inventory_quantity == 2

        client_repository.find_client_by_name.assert_called_once_with("Tirulipa")
        assert item_repository.find_item_by_name.call_count == 2
        item_repository.find_item_by_name.assert_has_calls(
            [call("Item 1"), call("Item 2")]
        )
        item_repository.save.assert_has_calls([call(item_1), call(item_2)])
        order_repository.save.assert_called_once()

    def test_create_order_use_case_negative_inventory(
        self, client_repository, item_repository, order_repository, client, item_1
    ):
        # Arrange
        client_repository.find_client_by_name.return_value = client
        item_repository.find_item_by_name.return_value = item_1

        input_dto = CreateOrderInputDTO(
            client_name="Tirulipa",
            external_order_id=1234,
            created_at="2023-06-07T10:00:00",
            items=[OrderItemInputDTO(item_name="Item 1", quantity=15)],
        )

        use_case = CreateOrderUseCase(client_repository, item_repository, order_repository)

        # Act
        output_dto = use_case.execute(input_dto)

        # Assert
        assert isinstance(output_dto, CreateOrderOutputDTO)
        assert output_dto.client_name == "Tirulipa"
        assert output_dto.external_order_id == 1234
        assert len(output_dto.order_items) == 1
        assert output_dto.order_items[0].item_name == "Item 1"
        assert output_dto.order_items[0].quantity == 15
        assert output_dto.order_items[0].inventory_quantity == -5

        client_repository.find_client_by_name.assert_called_once_with("Tirulipa")
        item_repository.find_item_by_name.assert_called_once_with("Item 1")
        item_repository.save.assert_called_once_with(item_1)
        order_repository.save.assert_called_once()

    def test_create_order_use_case_raises_client_not_found(
        self, client_repository, item_repository, order_repository
    ):
        # Arrange
        client_repository.find_client_by_name.return_value = None

        input_dto = CreateOrderInputDTO(
            client_name="Tirulipa",
            external_order_id=1234,
            created_at="2023-06-07T10:00:00",
            items=[],
        )

        use_case = CreateOrderUseCase(client_repository, item_repository, order_repository)

        # Act & Assert
        with pytest.raises(ClientNotFoundError) as exc_info:
            use_case.execute(input_dto)
        assert str(exc_info.value) == "Client not found: Tirulipa"

    def test_create_order_use_case_raises_item_not_found(
        self, client_repository, item_repository, order_repository, client
    ):
        # Arrange
        client_repository.find_client_by_name.return_value = client
        item_repository.find_item_by_name.return_value = None

        input_dto = CreateOrderInputDTO(
            client_name="Tirulipa",
            external_order_id=1234,
            created_at="2023-06-07T10:00:00",
            items=[OrderItemInputDTO(item_name="Item 1", quantity=2)],
        )

        use_case = CreateOrderUseCase(client_repository, item_repository, order_repository)

        # Act & Assert
        with pytest.raises(ItemNotFoundError) as exc_info:
            use_case.execute(input_dto)
        assert str(exc_info.value) == "Item not found: Item 1"