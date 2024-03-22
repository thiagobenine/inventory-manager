from datetime import datetime
from unittest.mock import Mock
from uuid import uuid4

import pytest
from freezegun import freeze_time

from src.domain.entities.client import Client
from src.domain.entities.item import Item
from src.domain.entities.order import Order, OrderItem
from src.domain.exceptions import ItemNotFoundByIdError, OrderNotFoundError
from src.domain.use_cases.cancel_order.cancel_order import CancelOrderUseCase
from src.domain.use_cases.cancel_order.dtos import (
    CancelOrderInputDTO,
    CancelOrderOutputDTO,
)


class TestCancelOrderUseCase:
    @pytest.fixture
    def order_repository(self):
        return Mock()

    @pytest.fixture
    def item_repository(self):
        return Mock()

    @pytest.fixture
    def client(self):
        return Client(name="Tirulipa", id=1)

    @pytest.fixture
    def order_item(self):
        return OrderItem(item_id=uuid4(), quantity=10)

    @freeze_time("2023-06-07 10:00:00")
    def test_cancel_order_use_case_with_success(
        self,
        order_repository,
        item_repository,
        client,
        order_item,
    ):
        # Arrange
        order_id = uuid4()
        item_id = order_item.item_id
        order_repository.find_order_by_id.return_value = Order(
            id=order_id,
            external_id=1234,
            created_at=datetime(2023, 6, 7, 10, 0, 0),
            updated_at=datetime(2023, 6, 7, 10, 0, 0),
            is_cancelled=False,
            client=client,
            items=[order_item],
        )

        item_name = "Marmita de Frango"

        item_repository.find_item_by_id.return_value = Item(
            id=item_id,
            name=item_name,
            inventory_quantity=10,
        )

        input_dto = CancelOrderInputDTO(order_id=order_id)

        use_case = CancelOrderUseCase(
            order_repository,
            item_repository,
        )

        # Act
        output_dto = use_case.execute(input_dto)

        # Assert
        assert isinstance(output_dto, CancelOrderOutputDTO)
        assert output_dto.order_id == order_id
        assert output_dto.client_name == "Tirulipa"
        assert output_dto.external_order_id == 1234
        assert output_dto.is_cancelled
        assert output_dto.created_at == "2023-06-07T10:00:00"
        assert output_dto.updated_at == "2023-06-07T10:00:00"
        assert len(output_dto.order_items) == 1
        assert output_dto.order_items[0].item_name == "Marmita de Frango"
        assert output_dto.order_items[0].quantity == 10
        assert output_dto.order_items[0].inventory_quantity == 10

        item_repository.find_item_by_id.assert_called_once_with(item_id)

        order_repository.find_order_by_id.assert_called_once_with(order_id)
        order_repository.save.assert_called_once()
        saved_order = order_repository.save.call_args[0][0]
        assert saved_order.id == order_id
        assert saved_order.external_id == 1234
        assert saved_order.created_at == datetime(2023, 6, 7, 10, 0, 0)
        assert saved_order.updated_at == datetime(2023, 6, 7, 10, 0, 0)
        assert saved_order.is_cancelled
        assert saved_order.client == client
        assert saved_order.items == [order_item]

    def test_cancel_order_use_case_raises_order_not_found(
        self,
        order_repository,
        item_repository,
    ):
        # Arrange
        order_id = uuid4()
        order_repository.find_order_by_id.return_value = None

        input_dto = CancelOrderInputDTO(order_id=order_id)

        use_case = CancelOrderUseCase(
            order_repository,
            item_repository,
        )

        # Act & Assert
        with pytest.raises(OrderNotFoundError) as exc_info:
            use_case.execute(input_dto)
        assert str(exc_info.value) == f"Order not found: {order_id}"

        order_repository.save.assert_not_called()

    def test_cancel_order_use_case_raises_item_not_found(
        self,
        order_repository,
        item_repository,
        client,
        order_item,
    ):
        # Arrange
        order_id = uuid4()
        item_id = order_item.item_id
        order_repository.find_order_by_id.return_value = Order(
            id=order_id,
            external_id=1234,
            created_at=datetime(2023, 6, 7, 10, 0, 0),
            updated_at=datetime(2023, 6, 7, 10, 0, 0),
            is_cancelled=False,
            client=client,
            items=[order_item],
        )
        item_repository.find_item_by_id.return_value = None

        input_dto = CancelOrderInputDTO(order_id=order_id)

        use_case = CancelOrderUseCase(
            order_repository,
            item_repository,
        )

        # Act & Assert
        with pytest.raises(ItemNotFoundByIdError) as exc_info:
            use_case.execute(input_dto)
        assert str(exc_info.value) == f"Item not found: {item_id}"

        order_repository.save.assert_not_called()
