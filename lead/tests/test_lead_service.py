from unittest.mock import MagicMock

import pytest

from lead.lead_service.exeptions import LeadNotNotFoundError
from lead.lead_service.lead import Lead
from lead.lead_service.lead_service import LeadService


@pytest.fixture
def mock_lead_repository():
    """Фикстура, предоставляющая мок-объект репозитория лидов."""
    return MagicMock()


@pytest.fixture
def lead_service(mock_lead_repository):
    """Фикстура, предоставляющая экземпляр LeadService с мок-репозиторием."""
    return LeadService(lead_repository=mock_lead_repository)


@pytest.fixture
def lead_get():
    """Фикстура, предоставляющая пример объекта Lead."""
    return Lead(
        id=1,
        name="Test lead_get name",
        first_name="Test lead_get first_name",
        phone="89995556611",
        email="exmp_22@mail.com",
        adv_id="1",
        is_active=False,
        is_archived=True,
    )


@pytest.fixture
def lead_post():
    """Фикстура, предоставляющая данные для нового Lead (без ID)."""
    return Lead(
        id=None,
        name="Test lead_post name",
        first_name="Test lead_post first_name",
        phone="89995556622",
        email="exmp_new_lead_22@mail.com",
        adv_id="1",
        is_active=None,
        is_archived=None
    )


@pytest.fixture
def lead_update():
    """Фикстура, предоставляющая данные для обновления Lead."""
    return Lead(
        id=None,
        name="Test lead_update name",
        first_name="Test lead_update first_name",
        phone="89991111111",
        email="updated_dexmp_22@mail.com",
        adv_id="3",
        is_active=True,
        is_archived=False,
    )


def test_place_lead__adds_item_to_repository_and_returns_it(
        lead_service, mock_lead_repository, lead_post
):
    """
    Тестирует, что place_lead корректно вызывает метод add репозитория
    и возвращает результат этого вызова.
    """
    mock_lead_repository.add.return_value = lead_post

    returned_lead = lead_service.place_lead(lead_post)

    mock_lead_repository.add.assert_called_once_with(lead_post)
    assert returned_lead == lead_post


def test_get_lead_returns_lead_id_found(lead_service, mock_lead_repository, lead_get):
    """
      Тестирует, что get_lead возвращает объявление, если оно найдено.
      """
    mock_lead_repository.get.return_value = lead_get

    found_lead = lead_service.get_lead(1)
    mock_lead_repository.get.assert_called_once_with(1)
    assert found_lead == lead_get


def test_get_lead_raises_lead_not_find_if_not_found(lead_service, mock_lead_repository):
    """
    Тестирует, что get_lead выбрасывает LeadNotNotFoundError, если объявление не найдено.
    """
    mock_lead_repository.get.return_value = None

    with pytest.raises(LeadNotNotFoundError) as e:
        lead_service.get_lead(999)

    mock_lead_repository.get.assert_called_once_with(999)
    assert "Lead with id 999 is not found" in str(e.value)

def test_update_lead_updates_lead_if_found_and_returns_updated(
        lead_service, mock_lead_repository,lead_get, lead_update
):
    """
        Тестирует, что update_lead корректно обновляет объявление, если оно найдено,
        и возвращает обновленный объект.
        """
    mock_lead_repository.get.return_value = lead_get
    mock_lead_repository.update.return_value = lead_update

    returned_lead = lead_service.update_lead(1, lead_update)

    mock_lead_repository.get.assert_called_once_with(1)
    mock_lead_repository.update.assert_called_once_with(1, lead_update)
    assert returned_lead == lead_update


def test_update_lead_raises_lead_not_find_if_not_found(
    lead_service, mock_lead_repository, lead_update
):
    """
    Тестирует, что update_lead выбрасывает LeadNotNotFoundError, если лида не найдено.
    """
    mock_lead_repository.get.return_value = None

    with pytest.raises(LeadNotNotFoundError) as e:
        lead_service.update_lead(999, lead_update)

    mock_lead_repository.get.assert_called_once_with(999)
    mock_lead_repository.update.assert_not_called()
    assert "Lead with id 999 is not found" in str(e.value)


def test_delete_lead_deletes_lead_if_found(lead_service, mock_lead_repository, lead_get):
    """
    Тестирует, что delete_lead корректно удаляет лида, если оно найдено.
    """
    mock_lead_repository.get.return_value = lead_get

    lead_service.delete_lead(1)

    mock_lead_repository.get.assert_called_once_with(1)
    mock_lead_repository.delete.assert_called_once_with(1)


def test_delete_lead_raises_lead_not_find_if_not_found(lead_service, mock_lead_repository):
    """
    Тестирует, что delete_lead выбрасывает LeadNotNotFoundError, если лид не найден.
    """
    mock_lead_repository.get.return_value = None

    with pytest.raises(LeadNotNotFoundError) as e:
        lead_service.delete_lead(999)

    mock_lead_repository.get.assert_called_once_with(999)
    mock_lead_repository.delete.assert_not_called()
    assert "Lead with id 999 is not found" in str(e.value)


def test_list_ads_calls_repository_with_correct_filters_and_returns_list(
    lead_service, mock_lead_repository, lead_get
):
    """
    Тестирует, что list_leads вызывает get_list репозитория с правильными параметрами
    и возвращает список объявлений.
    """
    mock_lead_repository.get_list.return_value = [
        lead_get,
        Lead(
            id=2,
            name="Test list_leads name",
            first_name="Test lead_get first_name",
            phone="89995556611",
            email="exmp_22@mail.com",
            adv_id="1",
            is_active=False,
            is_archived=True,
        )
    ]

    result = lead_service.list_leads(
        limit=10,
        offset=5,
        sort_field="name",
        sort_order="asc",
        email="exmp_22@mail.com",
        cost_gt=50,
    )
    mock_lead_repository.get_list.assert_called_once_with(
        limit=10,
        offset=5,
        sort_field="name",
        sort_order="asc",
        email="exmp_22@mail.com",
        cost_gt=50,
    )
    assert len(result) == 2
    assert result[0] == lead_get

    mock_lead_repository.get_list.reset_mock()
    mock_lead_repository.get_list.return_value = [lead_get]
    result = lead_service.list_leads(limit=5)
    mock_lead_repository.get_list.assert_called_once_with(
        limit=5, offset=None, sort_field=None, sort_order=None
    )
    assert len(result) == 1
    assert result[0] == lead_get
