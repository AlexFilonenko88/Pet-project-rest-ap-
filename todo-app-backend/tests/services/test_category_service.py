from unittest.mock import Mock

import pytest

from app.models.category import CategoryORM
from app.schemas.category import (
    CategoryCreateSchema,
    CategorySchema,
    CategoryUpdateSchema,
)
from app.services.category import CategoryNotFound, CategoryService


def test_list_category_return_pydantic_models(
    category_service: CategoryService,
    category_repository_mock: Mock,
    db_mock,
) -> None:
    category_repository_mock.get_all.return_value = [
        CategoryORM(id="cat-1", name="Категория 1"),
        CategoryORM(id="cat-2", name="Категория 2"),
    ]

    result = category_service.list_categories()

    assert result == [
        CategorySchema(id="cat-1", name="Категория 1"),
        CategorySchema(id="cat-2", name="Категория 2"),
    ]


def test_create_category_commits_created_category(
    category_service: CategoryService,
    category_repository_mock: Mock,
    db_mock,
) -> None:
    created_category = CategoryORM(id="cat-1", name="Категория 1")
    category_repository_mock.create.return_value = created_category

    result = category_service.create_category(CategoryCreateSchema(name="Категория 1"))
    db_mock.commit.assert_called_once_with()
    assert result.model_dump() == {
        "id": "cat-1",
        "name": "Категория 1",
    }


@pytest.mark.parametrize(
    ("payload", "expected_name"),
    [
        pytest.param(
            CategoryUpdateSchema(name="Обновить имя"),
            "Обновить имя",
        ),
        pytest.param(
            CategoryUpdateSchema(name="Готово"),
            "Готово",
        ),
    ],
)
def test_update_category_updates_only_passed_fields(
    category_service: CategoryService,
    category_repository_mock: Mock,
    db_mock: Mock,
    payload: CategoryUpdateSchema,
    expected_name: str,
) -> None:
    category = CategoryORM(id="cat-1", name="Категория 1")
    category_repository_mock.get_by_id.return_value = category

    result = category_service.update_category("cat-1", payload)

    category_repository_mock.get_by_id.assert_called_once_with(category_id="cat-1")
    db_mock.commit.assert_called_once_with()
    assert result.model_dump() == {
        "id": "cat-1",
        "name": expected_name,
    }


def test_update_category_raises_when_category_not_found(
    category_service: CategoryService,
    category_repository_mock: Mock,
    db_mock: Mock,
) -> None:
    category_repository_mock.get_by_id.return_value = None

    with pytest.raises(CategoryNotFound):
        category_service.update_category(
            "cat-1", CategoryUpdateSchema(name="Обновить имя")
        )

    db_mock.commit.assert_not_called()
