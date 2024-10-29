import pytest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Query
from app.service.person_service import *
from decimal import Decimal

"""! Test the PersonRepository class."""
@pytest.fixture
def mock_session():
    session = Mock()
    session.query.return_value = Mock(spec=Query)
    return session

@pytest.fixture
def person_repository(mock_session):
    return PersonRepository(mock_session)

def test_PersonRepository_username_exists(person_repository, mock_session):
    mock_query = mock_session.query.return_value
    mock_query.filter_by.return_value.first.return_value = Staff(
        username="staff",
        firstName="Admin",
        lastName="Admin",
    )

    result = person_repository.username_exists("staff")
    assert result is not None
    assert result.username == "staff"

    mock_query.filter_by.return_value.first.return_value = None
    test = person_repository.username_exists("test")
    assert test is None

def test_PersonRepository_get_user(person_repository, mock_session):
    mock_query = mock_session.query.return_value
    mock_query.get.return_value = Staff(
        username="staff",
        firstName="Admin",
        lastName="Admin",
    )

    result = person_repository.get_user(1)
    assert result is not None
    assert result.username == "staff"

    mock_query.get.return_value = None
    test = person_repository.get_user(2)
    assert test is None

"""! Test the PersonService class."""
@pytest.fixture
def mock_person_repository():
    return Mock()

@pytest.fixture
def person_service(mock_person_repository):
    return PersonService(mock_person_repository)

def test_PersonService_username_exists(person_service, mock_person_repository):
    # Arrange
    mock_person_repository.username_exists.return_value = True
    username = "testuser"
    result = person_service.username_exists(username)

    # Assert
    assert result is True