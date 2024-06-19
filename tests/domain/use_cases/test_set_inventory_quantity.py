from unittest.mock import Mock

import pytest
from bson import ObjectId

from src.domain.entities.item import Item
from src.domain.exceptions import ItemsNotFoundByNameError
from src.domain.ports.inbound.items.dtos import (
    SetInventoryQuantitiesInputDTO,
    SetInventoryQuantitiesOutputDTO,
    SetInventoryQuantityItemInputDTO,
)
from src.domain.use_cases.set_inventory_quantities import (
    SetInventoryQuantitiesUseCase,
)


class TestSetInventoryQuantitiesUseCase:
    @pytest.fixture
    def item_repository(self):
        return Mock()

    def test_set_inventory_quantities_use_case_with_success(
        self, item_repository
    ):
        # Arrange
        item_name = "Marmita Fit de Frango"
        inventory_quantity = 100
        item_repository.find_items_by_names.return_value = [
            Item(name=item_name, inventory_quantity=inventory_quantity)
        ]
        item_input_dto = SetInventoryQuantityItemInputDTO(
            item_name=item_name, inventory_quantity=inventory_quantity
        )
        input_dto = SetInventoryQuantitiesInputDTO(items=[item_input_dto])
        use_case = SetInventoryQuantitiesUseCase(item_repository)

        # Act
        output_dto = use_case.execute(input_dto)

        # Assert
        assert isinstance(output_dto, SetInventoryQuantitiesOutputDTO)
        assert output_dto.items[0].item_name == item_name
        assert output_dto.items[0].inventory_quantity == inventory_quantity

        item_repository.find_items_by_names.assert_called_once_with(
            [item_name]
        )
        item_repository.save_all.assert_called_once()
        saved_item = item_repository.save_all.call_args[0][0][0]
        assert saved_item.name == item_name
        assert saved_item.inventory_quantity == inventory_quantity
        assert isinstance(saved_item.id, ObjectId)

    def test_set_inventory_quantities_use_case_with_negative_quantity(
        self, item_repository
    ):
        # Arrange
        item_name = "Marmita Fit de Carne"
        inventory_quantity = -10
        item_repository.find_items_by_names.return_value = [
            Item(name=item_name, inventory_quantity=inventory_quantity)
        ]
        item_input_dto = SetInventoryQuantityItemInputDTO(
            item_name=item_name, inventory_quantity=inventory_quantity
        )
        input_dto = SetInventoryQuantitiesInputDTO(items=[item_input_dto])
        use_case = SetInventoryQuantitiesUseCase(item_repository)

        # Act
        output_dto = use_case.execute(input_dto)

        # Assert
        assert isinstance(output_dto, SetInventoryQuantitiesOutputDTO)
        assert output_dto.items[0].item_name == item_name
        assert output_dto.items[0].inventory_quantity == inventory_quantity

        item_repository.find_items_by_names.assert_called_once_with(
            [item_name]
        )
        item_repository.save_all.assert_called_once()
        saved_item = item_repository.save_all.call_args[0][0][0]
        assert saved_item.name == item_name
        assert saved_item.inventory_quantity == inventory_quantity
        assert isinstance(saved_item.id, ObjectId)

    def test_set_inventory_quantities_use_case_unexistent_item_raises_error(
        self, item_repository
    ):
        # Arrange
        item_name = "Marmita Vegana"
        inventory_quantity = 50
        item_repository.find_items_by_names.return_value = []
        item_input_dto = SetInventoryQuantityItemInputDTO(
            item_name=item_name, inventory_quantity=inventory_quantity
        )
        input_dto = SetInventoryQuantitiesInputDTO(items=[item_input_dto])

        use_case = SetInventoryQuantitiesUseCase(item_repository)

        # Act & Assert
        with pytest.raises(ItemsNotFoundByNameError) as exc_info:
            use_case.execute(input_dto)

        assert exc_info.value.items_names == [item_name]
        item_repository.find_items_by_names.assert_called_once_with(
            [item_name]
        )
        item_repository.save_all.assert_not_called()
