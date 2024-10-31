import pytest
from app.data_access.person_repository import PersonRepository
from app.models.Person import *
from werkzeug.security import generate_password_hash
from decimal import Decimal

@pytest.fixture
def person_repository(db_session):
    return PersonRepository(db_session)

def test_generate_staff_id(person_repository):
    staff_id = person_repository.generate_staff_id()
    assert staff_id == '000001'
    
    staff = Staff(
        username='test1',
        password_hash=generate_password_hash('123456'),
        staffID=staff_id,
        firstName='A',
        lastName='Test',
        deptName='IT'
    )
    person_repository.add_user(staff)
    
    next_staff_id = person_repository.generate_staff_id()
    assert next_staff_id == '000002'

def test_generate_customer_id(person_repository):
    customer_id = person_repository.generate_customer_id()
    assert customer_id == '10000001'
    
    customer = PrivateCustomer(
        username='test2',
        password_hash=generate_password_hash('123456'),
        custID=customer_id,
        firstName='B',
        lastName='Test',
        custBalance=Decimal('0.00'),
        custAddress='123 road',
        maxOwing=Decimal('100.00')
    )
    person_repository.add_user(customer)
    
    next_customer_id = person_repository.generate_customer_id()
    assert next_customer_id == '10000002'

def test_add_staff(person_repository):
    staff = Staff(
        username='test11',
        password_hash=generate_password_hash('123456'),
        staffID=person_repository.generate_staff_id(),
        firstName='AA',
        lastName='Test',
        deptName='IT'
    )
    
    result = person_repository.add_user(staff)
    assert result.username == 'test11'
    assert result.type == 'staff'
    assert result.deptName == 'IT'

def test_add_private_customer(person_repository):
    customer = PrivateCustomer(
        username='test22',
        password_hash=generate_password_hash('123456'),
        custID=person_repository.generate_customer_id(),
        firstName='BB',
        lastName='Test',
        custBalance=Decimal('0.00'),
        custAddress='123 road',
        maxOwing=Decimal('100.00')
    )
    
    result = person_repository.add_user(customer)
    assert result.username == 'test22'
    assert result.type == 'privatecustomer'
    assert result.maxOwing == Decimal('100.00')

def test_add_corporate_customer(person_repository):
    customer = CorporateCustomer(
        username='test33',
        password_hash=generate_password_hash('123456'),
        custID=person_repository.generate_customer_id(),
        firstName='CC',
        lastName='Test',
        custBalance=Decimal('0.00'),
        custAddress='456 road',
        maxOwing=Decimal('500.00'),
        discount=float(0.1),
        minBalance=10
    )
    
    result = person_repository.add_user(customer)
    assert result.username == 'test33'
    assert result.type == 'corporatecustomer'
    assert float(result.discount) == 0.1
    assert result.minBalance == 10

def test_username_exists(person_repository):
    staff = Staff(
        username='test111',
        password_hash=generate_password_hash('123456'),
        staffID=person_repository.generate_staff_id(),
        firstName='AAA',
        lastName='Test',
        deptName='IT'
    )
    person_repository.add_user(staff)
    
    assert person_repository.username_exists('test111') is not None
    assert person_repository.username_exists('test123') is None

def test_get_user_by_id(person_repository):
    staff = Staff(
        username='test1111',
        password_hash=generate_password_hash('123456'),
        staffID=person_repository.generate_staff_id(),
        firstName='AAAA',
        lastName='Test',
        deptName='IT'
    )
    added_staff = person_repository.add_user(staff)
    
    result = person_repository.get_user(id=added_staff.id)
    assert result.username == 'test1111'
    assert result.id == added_staff.id

def test_get_user_by_type(person_repository):
    staff = Staff(
        username='test11111',
        password_hash=generate_password_hash('123456'),
        staffID=person_repository.generate_staff_id(),
        firstName='AAAAA',
        lastName='Test',
        deptName='IT'
    )
    person_repository.add_user(staff)
    
    results = person_repository.get_user(selectType='staff')
    assert len(results) > 0
    assert all(user.type == 'staff' for user in results)

def test_update_user(person_repository):
    staff = Staff(
        username='staff111111',
        password_hash=generate_password_hash('123456'),
        staffID=person_repository.generate_staff_id(),
        firstName='AAAAAA',
        lastName='Test',
        deptName='IT'
    )
    added_staff = person_repository.add_user(staff)
    
    updated_data = {
        'firstName': 'Updated',
        'deptName': 'HR'
    }
    result = person_repository.update_user(added_staff.id, updated_data)
    
    assert result.firstName == 'Updated'
    assert result.deptName == 'HR'

def test_delete_user(person_repository):
    """Test deleting user"""
    staff = Staff(
        username='staff1111111',
        password_hash=generate_password_hash('123456'),
        staffID=person_repository.generate_staff_id(),
        firstName='AAAAAAA',
        lastName='Test',
        deptName='IT'
    )
    added_staff = person_repository.add_user(staff)
    
    result = person_repository.delete_user(added_staff.id)
    assert result is True
    assert person_repository.get_user(id=added_staff.id) is None

def test_duplicate_username(person_repository):
    staff1 = Staff(
        username='staff1',
        password_hash=generate_password_hash('123456'),
        staffID=person_repository.generate_staff_id(),
        firstName='A',
        lastName='Test',
        deptName='IT'
    )
    person_repository.add_user(staff1)
    
    staff2 = Staff(
        username='staff1',
        password_hash=generate_password_hash('123456'),
        staffID=person_repository.generate_staff_id(),
        firstName='A',
        lastName='Test',
        deptName='IT'
    )
    
    with pytest.raises(Exception):
        person_repository.add_user(staff2)

def test_get_all_users(person_repository):
    staff = Staff(
        username='staff1',
        password_hash=generate_password_hash('123456'),
        staffID=person_repository.generate_staff_id(),
        firstName='A',
        lastName='Test',
        deptName='IT'
    )
    
    customer = PrivateCustomer(
        username='test2',
        password_hash=generate_password_hash('123456'),
        custID=person_repository.generate_customer_id(),
        firstName='B',
        lastName='Test',
        custBalance=Decimal('0.00'),
        custAddress='123 road',
        maxOwing=Decimal('100.00')
    )
    
    person_repository.add_user(staff)
    person_repository.add_user(customer)
    
    results = person_repository.get_user()
    assert len(results) >= 2
    assert any(user.type == 'staff' for user in results)
    assert any(user.type == 'privatecustomer' for user in results)