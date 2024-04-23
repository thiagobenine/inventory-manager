from unittest.mock import Mock

import pytest
from bson import ObjectId

from src.domain.entities.item import Item
from src.domain.exceptions import ItemAlreadyExistsError
from src.domain.ports.inbound.items.dtos import (
    AddItemInputDTO,
    AddItemOutputDTO,
)
from src.domain.use_cases.add_item import AddItemUseCase


class TestAddItemUseCase:
    @pytest.fixture
    def item_repository(self):
        return Mock()

    def test_add_item_use_case_with_success(self, item_repository):
        # Arrange
        item_name = "Marmita Fit de Frango"
        inventory_quantity = 100
        item_repository.find_item_by_name.return_value = None
        input_dto = AddItemInputDTO(
            name=item_name, inventory_quantity=inventory_quantity
        )
        use_case = AddItemUseCase(item_repository)

        # Act
        output_dto = use_case.execute(input_dto)

        # Assert
        assert isinstance(output_dto, AddItemOutputDTO)
        assert output_dto.name == item_name
        assert output_dto.inventory_quantity == inventory_quantity

        item_repository.find_item_by_name.assert_called_once_with(item_name)
        item_repository.save.assert_called_once()
        saved_item = item_repository.save.call_args[0][0]
        assert saved_item.name == item_name
        assert saved_item.inventory_quantity == inventory_quantity
        assert isinstance(saved_item.id, ObjectId)

    def test_add_item_use_case_with_negative_quantity(self, item_repository):
        # Arrange
        item_name = "Marmita Fit de Carne"
        inventory_quantity = -10
        item_repository.find_item_by_name.return_value = None
        input_dto = AddItemInputDTO(
            name=item_name, inventory_quantity=inventory_quantity
        )
        use_case = AddItemUseCase(item_repository)

        # Act
        output_dto = use_case.execute(input_dto)

        # Assert
        assert isinstance(output_dto, AddItemOutputDTO)
        assert output_dto.name == item_name
        assert output_dto.inventory_quantity == inventory_quantity

        item_repository.find_item_by_name.assert_called_once_with(item_name)
        item_repository.save.assert_called_once()
        saved_item = item_repository.save.call_args[0][0]
        assert saved_item.name == item_name
        assert saved_item.inventory_quantity == inventory_quantity
        assert isinstance(saved_item.id, ObjectId)

    def test_add_item_use_case_existing_item_raises_error(
        self, item_repository
    ):
        # Arrange
        item_name = "Marmita Vegana"
        inventory_quantity = 50
        item_repository.find_item_by_name.return_value = Item(
            name=item_name, inventory_quantity=inventory_quantity
        )
        input_dto = AddItemInputDTO(
            name=item_name, inventory_quantity=inventory_quantity
        )
        use_case = AddItemUseCase(item_repository)

        # Act & Assert
        with pytest.raises(ItemAlreadyExistsError) as exc_info:
            use_case.execute(input_dto)

        assert str(exc_info.value) == f"Item already exists: {item_name}"
        item_repository.find_item_by_name.assert_called_once_with(item_name)
        item_repository.save.assert_not_called()
