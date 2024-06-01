from datetime import datetime
from unittest.mock import Mock

import pytest
from bson import ObjectId
from freezegun import freeze_time

from src.domain.entities.client import Client
from src.domain.entities.item import Item
from src.domain.entities.order import Order, OrderItem
from src.domain.exceptions import OrderNotFoundError
from src.domain.ports.inbound.orders.dtos import (
    CancelOrderInputDTO,
    CancelOrderOutputDTO,
)
from src.domain.use_cases.cancel_order import CancelOrderUseCase


class TestCancelOrderUseCase:
    @pytest.fixture
    def order_repository(self):
        return Mock()

    @pytest.fixture
    def item_repository(self):
        return Mock()

    @pytest.fixture
    def client(self):
        return Client(name="Tirulipa")

    @pytest.fixture
    def order_item(self):
        item = Item(name="Marmita de Frango", inventory_quantity=10)
        return OrderItem(item=item, quantity=10)

    @freeze_time("2023-06-07 10:00:00")
    def test_cancel_order_use_case_with_success(
        self,
        order_repository,
        item_repository,
        client,
        order_item,
    ):
        # Arrange
        order_id = ObjectId()
        item_id = order_item.item.id
        order_repository.find_order_by_id.return_value = Order(
            id=order_id,
            external_id=1234,
            external_created_at="17:54",
            created_at=datetime(2023, 6, 7, 10, 0, 0),
            updated_at=datetime(2023, 6, 7, 10, 0, 0),
            is_cancelled=False,
            client=client,
            order_items=[order_item],
        )

        item_name = "Marmita de Frango"

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
        assert output_dto.order_items[0].inventory_quantity == 20

        order_repository.find_order_by_id.assert_called_once_with(order_id)
        order_repository.save.assert_called_once()
        saved_order = order_repository.save.call_args[0][0]
        assert saved_order.id == order_id
        assert saved_order.external_id == 1234
        assert saved_order.created_at == datetime(2023, 6, 7, 10, 0, 0)
        assert saved_order.updated_at == datetime(2023, 6, 7, 10, 0, 0)
        assert saved_order.is_cancelled
        assert saved_order.client == client
        assert saved_order.order_items == [order_item]

        item_repository.save_all.assert_called_once()
        saved_items = item_repository.save_all.call_args[0][0]
        assert len(saved_items) == 1
        saved_item = saved_items[0]
        assert saved_item.id == item_id
        assert saved_item.name == item_name
        assert (
            saved_item.inventory_quantity == 20
        )  # initial inventory_quantity was 10

    def test_cancel_order_use_case_raises_order_not_found(
        self,
        order_repository,
        item_repository,
    ):
        # Arrange
        order_id = ObjectId()
        order_repository.find_order_by_id.return_value = None

        input_dto = CancelOrderInputDTO(order_id=order_id)

        use_case = CancelOrderUseCase(
            order_repository,
            item_repository,
        )

        # Act & Assert
        with pytest.raises(OrderNotFoundError) as exc_info:
            use_case.execute(input_dto)
        assert exc_info.value.order_id == order_id

        order_repository.save.assert_not_called()
