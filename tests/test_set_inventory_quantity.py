from unittest.mock import Mock
from uuid import UUID

import pytest

from src.domain.entities.item import Item
from src.domain.exceptions import ItemNotFoundError
from src.domain.use_cases.set_inventory_quantity.dtos import (
    SetInventoryQuantityInputDTO,
    SetInventoryQuantityOutputDTO,
)
from src.domain.use_cases.set_inventory_quantity.set_inventory_quantity import (  # noqa
    SetInventoryQuantityUseCase,
)


class TestSetInventoryQuantityUseCase:
    @pytest.fixture
    def item_repository(self):
        return Mock()

    def test_set_inventory_quantity_use_case_with_success(
        self, item_repository
    ):
        # Arrange
        item_name = "Marmita Fit de Frango"
        inventory_quantity = 100
        item_repository.find_item_by_name.return_value = Item(
            name=item_name, inventory_quantity=inventory_quantity
        )
        input_dto = SetInventoryQuantityInputDTO(
            item_name=item_name, inventory_quantity=inventory_quantity
        )
        use_case = SetInventoryQuantityUseCase(item_repository)

        # Act
        output_dto = use_case.execute(input_dto)

        # Assert
        assert isinstance(output_dto, SetInventoryQuantityOutputDTO)
        assert output_dto.item_name == item_name
        assert output_dto.inventory_quantity == inventory_quantity

        item_repository.find_item_by_name.assert_called_once_with(item_name)
        item_repository.save.assert_called_once()
        saved_item = item_repository.save.call_args[0][0]
        assert saved_item.name == item_name
        assert saved_item.inventory_quantity == inventory_quantity
        assert isinstance(saved_item.id, UUID)

    def test_set_inventory_quantity_use_case_with_negative_quantity(
        self, item_repository
    ):
        # Arrange
        item_name = "Marmita Fit de Carne"
        inventory_quantity = -10
        item_repository.find_item_by_name.return_value = Item(
            name=item_name, inventory_quantity=inventory_quantity
        )
        input_dto = SetInventoryQuantityInputDTO(
            item_name=item_name, inventory_quantity=inventory_quantity
        )
        use_case = SetInventoryQuantityUseCase(item_repository)

        # Act
        output_dto = use_case.execute(input_dto)

        # Assert
        assert isinstance(output_dto, SetInventoryQuantityOutputDTO)
        assert output_dto.item_name == item_name
        assert output_dto.inventory_quantity == inventory_quantity

        item_repository.find_item_by_name.assert_called_once_with(item_name)
        item_repository.save.assert_called_once()
        saved_item = item_repository.save.call_args[0][0]
        assert saved_item.name == item_name
        assert saved_item.inventory_quantity == inventory_quantity
        assert isinstance(saved_item.id, UUID)

    def test_set_inventory_quantity_use_case_unexistent_item_raises_error(
        self, item_repository
    ):
        # Arrange
        item_name = "Marmita Vegana"
        inventory_quantity = 50
        item_repository.find_item_by_name.return_value = None
        input_dto = SetInventoryQuantityInputDTO(
            item_name=item_name, inventory_quantity=inventory_quantity
        )
        use_case = SetInventoryQuantityUseCase(item_repository)

        # Act & Assert
        with pytest.raises(ItemNotFoundError) as exc_info:
            use_case.execute(input_dto)

        assert str(exc_info.value) == f"Item not found: {item_name}"
        item_repository.find_item_by_name.assert_called_once_with(item_name)
        item_repository.save.assert_not_called()
