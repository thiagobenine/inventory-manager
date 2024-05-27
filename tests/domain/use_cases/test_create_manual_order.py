from unittest.mock import Mock

import pytest

from src.domain.entities.item import Item
from src.domain.exceptions import ItemsNotFoundByNameError
from src.domain.ports.inbound.orders.dtos import (
    CreateManualOrderInputDTO,
    CreateManualOrderOutputDTO,
    OrderItemInputDTO,
)
from src.domain.use_cases.create_manual_order import CreateManualOrderUseCase


class TestCreateManualOrderUseCase:
    @pytest.fixture
    def item_repository(self):
        return Mock()

    @pytest.fixture
    def order_repository(self):
        return Mock()

    @pytest.fixture
    def item_1(self):
        return Item(name="Item 1", inventory_quantity=10)

    @pytest.fixture
    def item_2(self):
        return Item(name="Item 2", inventory_quantity=5)

    def test_create_manual_order_use_case_with_success(
        self,
        item_repository,
        order_repository,
        item_1,
        item_2,
    ):
        # Arrange
        item_repository.find_items_by_names.return_value = [item_1, item_2]

        input_dto = CreateManualOrderInputDTO(
            items=[
                OrderItemInputDTO(item_name="Item 1", quantity=2),
                OrderItemInputDTO(item_name="Item 2", quantity=3),
            ],
        )

        use_case = CreateManualOrderUseCase(item_repository, order_repository)

        # Act
        output_dto = use_case.execute(input_dto)

        # Assert
        assert isinstance(output_dto, CreateManualOrderOutputDTO)
        assert len(output_dto.order_items) == 2
        assert output_dto.order_items[0].item_name == "Item 1"
        assert output_dto.order_items[0].quantity == 2
        assert output_dto.order_items[0].inventory_quantity == 8
        assert output_dto.order_items[1].item_name == "Item 2"
        assert output_dto.order_items[1].quantity == 3
        assert output_dto.order_items[1].inventory_quantity == 2

        item_repository.find_items_by_names.assert_called_once_with(
            ["Item 1", "Item 2"]
        )
        item_repository.save_all.assert_called_once_with([item_1, item_2])

        order_repository.save.assert_called_once()

    def test_create_manual_order_use_case_negative_inventory(
        self,
        item_repository,
        order_repository,
        item_1,
    ):
        # Arrange
        item_repository.find_items_by_names.return_value = [item_1]

        input_dto = CreateManualOrderInputDTO(
            items=[OrderItemInputDTO(item_name="Item 1", quantity=15)],
        )

        use_case = CreateManualOrderUseCase(item_repository, order_repository)

        # Act
        output_dto = use_case.execute(input_dto)

        # Assert
        assert isinstance(output_dto, CreateManualOrderOutputDTO)
        assert len(output_dto.order_items) == 1
        assert output_dto.order_items[0].item_name == "Item 1"
        assert output_dto.order_items[0].quantity == 15
        assert output_dto.order_items[0].inventory_quantity == -5

        item_repository.save_all.assert_called_once_with([item_1])
        order_repository.save.assert_called_once()

    def test_create_order_use_case_raises_item_not_found(
        self, item_repository, order_repository
    ):
        # Arrange
        item_repository.find_items_by_names.return_value = []

        input_dto = CreateManualOrderInputDTO(
            items=[OrderItemInputDTO(item_name="Item 1", quantity=2)],
        )

        use_case = CreateManualOrderUseCase(item_repository, order_repository)

        # Act & Assert
        with pytest.raises(ItemsNotFoundByNameError) as exc_info:
            use_case.execute(input_dto)
        assert str(exc_info.value) == "Items not found: ['Item 1']"

        item_repository.save.assert_not_called()
        order_repository.save.assert_not_called()
