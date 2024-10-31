import pytest
from decimal import Decimal
from app.service.person_service import *

@pytest.fixture
def person_service(db_session):
    person_repository = PersonRepository(db_session)
    return PersonService(person_repository)

def test_password_hashing(person_service):
    password = "123456"
    hashed = person_service.generate_hashed_password(password)
    
    assert hashed != password
    assert person_service.verify_password(hashed, password) is True
    assert person_service.verify_password(hashed, "111111") is False

def test_add_staff(person_service):
    staff = {
        'type': 'staff',
        'username': 'test1',
        'password': '111111',
        'firstName': 'A',
        'lastName': 'Test',
        'deptName': 'IT'
    }
    
    result = person_service.add_user(**staff)
    assert result.username == staff['username']
    assert result.firstName == staff['firstName']
    assert result.lastName == staff['lastName']
    assert result.deptName == staff['deptName']
    assert result.type == 'staff'

def test_add_private_customer(person_service):
    customer_data = {
        'type': 'privatecustomer',
        'username': 'test2',
        'password': '111111',
        'firstName': 'B',
        'lastName': 'Test',
        'custBalance': '0.00',
        'custAddress': '123 road',
        'maxOwing': '100.00'
    }
    
    result = person_service.add_user(**customer_data)
    assert hasattr(result, 'id')
    assert result.username == customer_data['username']
    assert result.firstName == customer_data['firstName']
    assert result.custBalance == Decimal('0.00')
    assert result.maxOwing == Decimal('100.00')
    assert result.type == 'privatecustomer'

def test_add_corporate_customer(person_service):
    customer_data = {
        'type': 'corporatecustomer',
        'username': 'test3',
        'password': '111111',
        'firstName': 'C',
        'lastName': 'Test',
        'custBalance': '0.00',
        'custAddress': '456 road',
        'maxOwing': '500.00',
        'discount': 0.1,
        'minBalance': 10
    }
    
    result = person_service.add_user(**customer_data)
    assert result.username == customer_data['username']
    assert result.minBalance == customer_data['minBalance']
    assert result.type == 'corporatecustomer'

def test_duplicate_username(person_service):
    user_data = {
        'type': 'staff',
        'username': 'staff',
        'password': '123456',
        'firstName': 'Test',
        'lastName': 'User',
        'deptName': 'IT'
    }
    
    person_service.add_user(**user_data)
    
    result = person_service.add_user(**user_data)
    assert result == "Username already exists"

def test_update_user(person_service):
    user_data = {
        'type': 'staff',
        'username': 'update_test',
        'password': '123456',
        'firstName': 'Before',
        'lastName': 'Update',
        'deptName': 'IT'
    }
    
    user = person_service.add_user(**user_data)
    
    # Update user
    update_data = {
        'id': user.id,
        'firstName': 'After',
        'lastName': 'Update',
        'deptName': 'HR',
        'password': '111111'
    }
    
    updated_user = person_service.update_user(**update_data)
    assert updated_user.firstName == 'After'
    assert updated_user.deptName == 'HR'
    assert person_service.verify_password(updated_user.password_hash, '111111')

def test_delete_user(person_service):
    user_data = {
        'type': 'staff',
        'username': 'delete_test',
        'password': '123456',
        'firstName': 'Delete',
        'lastName': 'Test',
        'deptName': 'IT'
    }
    
    user = person_service.add_user(**user_data)
    
    result = person_service.delete_user(user.id)
    assert result is True
    assert person_service.get_user(user.id) is None

def test_update_balance(person_service):
    customer_data = {
        'type': 'privatecustomer',
        'username': 'balance_test',
        'password': '123456',
        'firstName': 'Balance',
        'lastName': 'Test',
        'custBalance': '0.00',
        'custAddress': 'Test Address',
        'maxOwing': '100.00'
    }
    
    customer = person_service.add_user(**customer_data)
    
    # Test adding to balance
    result = person_service.update_balance(customer.id, '50.00')
    assert result.custBalance == Decimal('50.00')
    
    # Test subtracting from balance
    result = person_service.update_balance(customer.id, '-30.00')
    assert result.custBalance == Decimal('20.00')
    
    # Test insufficient balance
    result = person_service.update_balance(customer.id, '-150.00')
    assert isinstance(result, str)