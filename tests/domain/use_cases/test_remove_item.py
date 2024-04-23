from unittest.mock import Mock

import pytest

from src.domain.entities.item import Item
from src.domain.exceptions import ItemNotFoundByNameError
from src.domain.ports.inbound.items.dtos import (
    RemoveItemInputDTO,
    RemoveItemOutputDTO,
)
from src.domain.use_cases.remove_item import RemoveItemUseCase


class TestRemoveItemUseCase:
    @pytest.fixture
    def item_repository(self):
        return Mock()

    def test_remove_item_use_case_with_success(self, item_repository):
        # Arrange
        item_name = "Marmita Vegana"
        inventory_quantity = 50
        item_repository.find_item_by_name.return_value = Item(
            name=item_name, inventory_quantity=inventory_quantity
        )
        input_dto = RemoveItemInputDTO(name=item_name)
        use_case = RemoveItemUseCase(item_repository)

        # Act
        output_dto = use_case.execute(input_dto)

        # Assert
        assert isinstance(output_dto, RemoveItemOutputDTO)
        assert output_dto.name == item_name

        item_repository.find_item_by_name.assert_called_once_with(item_name)
        item_repository.remove_item_by_name.assert_called_once_with(item_name)

    def test_remove_item_use_case_unexistent_item_raises_error(
        self, item_repository
    ):
        # Arrange
        item_name = "Marmita Fit de Frango"
        item_repository.find_item_by_name.return_value = None
        input_dto = RemoveItemInputDTO(name=item_name)
        use_case = RemoveItemUseCase(item_repository)

        # Act & Assert
        with pytest.raises(ItemNotFoundByNameError) as exc_info:
            use_case.execute(input_dto)

        assert str(exc_info.value) == f"Item not found: {item_name}"
        item_repository.find_item_by_name.assert_called_once_with(item_name)
        item_repository.remove_item_by_name.assert_not_called()
