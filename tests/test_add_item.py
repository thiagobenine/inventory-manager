from unittest.mock import Mock
from uuid import UUID, uuid4

import pytest

from domain.entities.item import Item
from domain.exceptions import ItemAlreadyExistsError
from domain.use_cases.add_item.add_item import AddItemUseCase
from domain.use_cases.add_item.dtos import AddItemInputDTO


class TestAddItemUseCase:
    @pytest.fixture
    def item_repository(self):
        return Mock()

    def test_add_item_use_case_with_success(self, item_repository):
        # Arrange
        item_name = "Marmita Fit de Frango"
        inventory_quantity = 100
        item_repository.find_item_by_name.return_value = None
        input_dto = AddItemInputDTO(name=item_name, inventory_quantity=inventory_quantity)
        use_case = AddItemUseCase(item_repository)

        # Act
        use_case.execute(input_dto)

        # Assert
        item_repository.find_item_by_name.assert_called_once_with(item_name)
        item_repository.save.assert_called_once()
        saved_item = item_repository.save.call_args[0][0]
        assert saved_item.name == item_name
        assert saved_item.inventory_quantity == inventory_quantity
        assert isinstance(saved_item.id, UUID)

    def test_add_item_use_case_with_negative_quantity(self, item_repository):
        # Arrange
        item_name = "Marmita Fit de Carne"
        inventory_quantity = -10
        item_repository.find_item_by_name.return_value = None
        input_dto = AddItemInputDTO(name=item_name, inventory_quantity=inventory_quantity)
        use_case = AddItemUseCase(item_repository)

        # Act
        use_case.execute(input_dto)

        # Assert
        item_repository.find_item_by_name.assert_called_once_with(item_name)
        item_repository.save.assert_called_once()
        saved_item = item_repository.save.call_args[0][0]
        assert saved_item.name == item_name
        assert saved_item.inventory_quantity == inventory_quantity
        assert isinstance(saved_item.id, UUID)

    def test_add_item_use_case_existing_item_raises_error(self, item_repository):
        # Arrange
        item_name = "Marmita Vegana"
        inventory_quantity = 50
        item_repository.find_item_by_name.return_value = Item(
            name=item_name,
            inventory_quantity=inventory_quantity
        )
        input_dto = AddItemInputDTO(name=item_name, inventory_quantity=inventory_quantity)
        use_case = AddItemUseCase(item_repository)

        # Act & Assert
        with pytest.raises(ItemAlreadyExistsError):
            use_case.execute(input_dto)

        item_repository.find_item_by_name.assert_called_once_with(item_name)
        item_repository.save.assert_not_called()
