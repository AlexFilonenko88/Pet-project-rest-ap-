from unittest.mock import Mock

import pytest
from sqlalchemy.orm import Session

from app.repositories.category import CategoryRepository
from app.repositories.task import TaskRepository
from app.services.category import CategoryService
from app.services.task import TaskService


@pytest.fixture
def db_mock() -> Mock:
    """Создаём мок сессии БД один раз и переиспользуем в тестах"""

    return Mock(spec=Session)


@pytest.fixture
def task_repository_mock() -> Mock:
    """Создаём мок TaskRepository один раз и переиспользуем в тестах"""

    return Mock(spec=TaskRepository)


@pytest.fixture
def category_repository_mock() -> Mock:
    """Создаём мок CategoryRepository один раз и переиспользуем в тестах"""

    return Mock(spec=CategoryRepository)


@pytest.fixture
def task_service(db_mock: Mock, task_repository_mock: Mock) -> TaskService:
    """TaskService с замоканными зависимостями"""
    # task_service = TaskService(db_mock)
    # task_service.repository = repository_mock

    return TaskService(db=db_mock, task_repository=task_repository_mock)


@pytest.fixture
def category_service(db_mock: Mock, category_repository_mock: Mock) -> CategoryService:
    """CategoryService с замоканными зависимостями"""

    return CategoryService(db=db_mock, category_repository=category_repository_mock)
