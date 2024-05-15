from unittest.mock import Mock

import pytest

from src.domain.entities.item import Item
from src.domain.ports.inbound.items.dtos import ListItemsOutputDTO
from src.domain.use_cases.list_items import ListItemsUseCase


class TestSetInventoryQuantityUseCase:
    @pytest.fixture
    def item_repository(self):
        return Mock()

    @pytest.fixture
    def use_case(self, item_repository):
        return ListItemsUseCase(item_repository)

    def test_list_items_use_case_with_success(self, item_repository, use_case):
        # Arrange
        item_name = "Marmita Fit de Frango"
        inventory_quantity = 100
        item_repository.get_all.return_value = [
            Item(name=item_name, inventory_quantity=inventory_quantity)
        ]

        # Act
        output_dto = use_case.execute()

        # Assert
        assert isinstance(output_dto, ListItemsOutputDTO)
        assert len(output_dto.items) == 1
        assert output_dto.items[0].item_name == item_name
        assert output_dto.items[0].inventory_quantity == inventory_quantity
