import pytest
from unittest.mock import MagicMock
from decimal import Decimal
from datetime import datetime, timedelta

from adv.adv_service.adv import Adv
from adv.adv_service.adv_service import AdvService
from adv.adv_service.exeptions import AdvNotNotFoundError


@pytest.fixture
def mock_adv_repository():
    """Фикстура, предоставляющая мок-объект репозитория объявлений."""
    return MagicMock()


@pytest.fixture
def adv_service(mock_adv_repository):
    """Фикстура, предоставляющая экземпляр AdvService с мок-репозиторием."""
    return AdvService(adv_repository=mock_adv_repository)


@pytest.fixture
def adv_get():
    """Фикстура, предоставляющая пример объекта Adv."""
    return Adv(
        id=1,
        name="Test adv_get",
        cost=Decimal("111.11"),
        chanel="Yandex",
        created_at=datetime(2025, 1, 2, 10, 0, 0),
        product_id=111,
    )


@pytest.fixture
def adv_post():
    """Фикстура, предоставляющая данные для нового объявления (без ID)."""
    return Adv(
        id=None,
        name="Test adv_post",
        cost=Decimal("222.99"),
        chanel="VK",
        created_at=datetime.now(),
        product_id=None,
    )


@pytest.fixture
def adv_update():
    """Фикстура, предоставляющая данные для обновления объявления."""
    return Adv(
        id=1,
        name="Test adv_update",
        cost=Decimal("333.55"),
        chanel="TG",
        created_at=datetime.now() + timedelta(days=1),
        product_id=222,
    )


def test_place_adv_adds_item_to_repository_and_returns_it(
    adv_service, mock_adv_repository, adv_post
):
    """
    Тестирует, что place_adv корректно вызывает метод add репозитория
    и возвращает результат этого вызова.
    """
    mock_adv_repository.add.return_value = adv_post

    returned_adv = adv_service.place_adv(adv_post)

    mock_adv_repository.add.assert_called_once_with(adv_post)
    assert returned_adv == adv_post


def test_get_adv_returns_adv_if_found(adv_service, mock_adv_repository, adv_get):
    """
    Тестирует, что get_adv возвращает объявление, если оно найдено.
    """
    mock_adv_repository.get.return_value = adv_get

    found_adv = adv_service.get_adv(1)

    mock_adv_repository.get.assert_called_once_with(1)
    assert found_adv == adv_get


def test_get_adv_raises_advnotfind_if_not_found(adv_service, mock_adv_repository):
    """
    Тестирует, что get_adv выбрасывает AdvNotNotFoundError, если объявление не найдено.
    """
    mock_adv_repository.get.return_value = None

    with pytest.raises(AdvNotNotFoundError) as e:
        adv_service.get_adv(999)

    mock_adv_repository.get.assert_called_once_with(999)
    assert "Advertisement with id 999 is not found" in str(e.value)


def test_update_adv_updates_adv_if_found_and_returns_updated(
    adv_service, mock_adv_repository, adv_get, adv_update
):
    """
    Тестирует, что update_adv корректно обновляет объявление, если оно найдено,
    и возвращает обновленный объект.
    """
    mock_adv_repository.get.return_value = adv_get
    mock_adv_repository.update.return_value = adv_update

    returned_adv = adv_service.update_adv(1, adv_update)

    mock_adv_repository.get.assert_called_once_with(1)
    mock_adv_repository.update.assert_called_once_with(1, adv_update)
    assert returned_adv == adv_update


def test_update_adv_raises_advnotfind_if_not_found(
    adv_service, mock_adv_repository, adv_update
):
    """
    Тестирует, что update_adv выбрасывает AdvNotNotFoundError, если объявление не найдено.
    """
    mock_adv_repository.get.return_value = None

    with pytest.raises(AdvNotNotFoundError) as e:
        adv_service.update_adv(999, adv_update)

    mock_adv_repository.get.assert_called_once_with(999)
    mock_adv_repository.update.assert_not_called()
    assert "Advertisement with id 999 is not found" in str(e.value)


def test_delete_adv_deletes_adv_if_found(adv_service, mock_adv_repository, adv_get):
    """
    Тестирует, что delete_adv корректно удаляет объявление, если оно найдено.
    """
    mock_adv_repository.get.return_value = adv_get

    adv_service.delete_adv(1)

    mock_adv_repository.get.assert_called_once_with(1)
    mock_adv_repository.delete.assert_called_once_with(1)


def test_delete_adv_raises_advnotfind_if_not_found(adv_service, mock_adv_repository):
    """
    Тестирует, что delete_adv выбрасывает AdvNotNotFoundError, если объявление не найдено.
    """
    mock_adv_repository.get.return_value = None

    with pytest.raises(AdvNotNotFoundError) as e:
        adv_service.delete_adv(999)

    mock_adv_repository.get.assert_called_once_with(999)
    mock_adv_repository.delete.assert_not_called()
    assert "Advertisement with id 999 is not found" in str(e.value)


def test_list_ads_calls_repository_with_correct_filters_and_returns_list(
    adv_service, mock_adv_repository, adv_get
):
    """
    Тестирует, что list_ads вызывает get_list репозитория с правильными параметрами
    и возвращает список объявлений.
    """
    mock_adv_repository.get_list.return_value = [
        adv_get,
        Adv(
            id=2,
            name="Adv testtttt",
            cost=Decimal("11.44"),
            chanel="VK",
            created_at=datetime(2023, 2, 1),
            product_id=103,
        ),
    ]

    result = adv_service.list_ads(
        limit=10,
        offset=5,
        sort_field="name",
        sort_order="asc",
        chanel="TG",
        since=datetime(2022, 1, 1),
        cost_gt=50,
    )
    mock_adv_repository.get_list.assert_called_once_with(
        limit=10,
        offset=5,
        sort_field="name",
        sort_order="asc",
        chanel="TG",
        since=datetime(2022, 1, 1),
        cost_gt=50,
    )
    assert len(result) == 2
    assert result[0] == adv_get

    mock_adv_repository.get_list.reset_mock()
    mock_adv_repository.get_list.return_value = [adv_get]
    result = adv_service.list_ads(limit=5)
    mock_adv_repository.get_list.assert_called_once_with(
        limit=5, offset=None, sort_field=None, sort_order=None, since=None
    )
    assert len(result) == 1
    assert result[0] == adv_get
