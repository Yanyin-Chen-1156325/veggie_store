import pytest
from decimal import Decimal
from app.service.payment_service import PaymentService
from app.models.Payment import CreditCardPayment, DebitCardPayment
from app.service.person_service import PersonService
from app.data_access.person_repository import PersonRepository

@pytest.fixture
def person_service(db_session):
    person_repository = PersonRepository(db_session)
    return PersonService(person_repository)

@pytest.fixture
def payment_service(db_session):
    from app.data_access.payment_repository import PaymentRepository
    payment_repository = PaymentRepository(db_session)
    return PaymentService(payment_repository)

@pytest.fixture
def test_customer(person_service):
    """Create a test customer for payments"""
    customer_data = {
        'type': 'privatecustomer',
        'username': 'corporate',
        'password': '123456',
        'firstName': 'C',
        'lastName': 'Test',
        'custBalance': '0.00',
        'custAddress': '456 road',
        'maxOwing': '500.00'
    }
    return person_service.add_user(**customer_data)

def test_create_credit_payment(payment_service, test_customer):
    payment_data = {
        'payment_method': 'Credit',
        'cardNumber': '1234123412341234',
        'cardExpiryDate': '12/25',
        'cardHolder': 'Corporate',
        'cardType': 'Visa',
        'cardCVV': '123',
        'paymentAmount': Decimal('100.00'),
        'paymentType': 'Credit',
        'customer_id': test_customer.id
    }
    
    result = payment_service.create_payment(**payment_data)
    assert isinstance(result, CreditCardPayment)
    assert result.cardNumber == payment_data['cardNumber']
    assert result.cardHolder == payment_data['cardHolder']
    assert result.cardType == payment_data['cardType']
    assert result.paymentAmount == payment_data['paymentAmount']
    assert result.customer_id == test_customer.id

def test_create_debit_payment(payment_service, test_customer):
    payment_data = {
        'payment_method': 'Debit',
        'bankName': 'ANZ Bank',
        'debitCardNumber': '1111111111111111',
        'paymentAmount': Decimal('50.00'),
        'paymentType': 'Debit',
        'customer_id': test_customer.id
    }
    
    result = payment_service.create_payment(**payment_data)
    assert isinstance(result, DebitCardPayment)
    assert result.bankName == payment_data['bankName']
    assert result.debitCardNumber == payment_data['debitCardNumber']
    assert result.paymentAmount == payment_data['paymentAmount']
    assert result.customer_id == test_customer.id

def test_invalid_payment_method(payment_service, test_customer):
    payment_data = {
        'payment_method': 'Invalid',
        'paymentAmount': Decimal('100.00'),
        'paymentType': 'Balance',
        'customer_id': test_customer.id
    }
    
    result = payment_service.create_payment(**payment_data)
    assert result == 'Invalid payment method'

def test_get_payment_by_id(payment_service, test_customer):
    payment_data = {
        'payment_method': 'Credit',
        'cardNumber': '1234123412341234',
        'cardExpiryDate': '12/25',
        'cardHolder': 'Corporate',
        'cardType': 'Visa',
        'cardCVV': '123',
        'paymentAmount': Decimal('100.00'),
        'paymentType': 'Credit',
        'customer_id': test_customer.id
    }
    
    payment = payment_service.create_payment(**payment_data)
    assert isinstance(payment, CreditCardPayment)
    
    result = payment_service.get_payment(id=payment.id)
    assert result.paymentID == payment.paymentID
    assert result.paymentAmount == payment_data['paymentAmount']

def test_get_payment_by_customer(payment_service, test_customer):
    credit_payment = {
       'payment_method': 'Credit',
        'cardNumber': '1234123412341234',
        'cardExpiryDate': '12/25',
        'cardHolder': 'Corporate',
        'cardType': 'Visa',
        'cardCVV': '123',
        'paymentAmount': Decimal('100.00'),
        'paymentType': 'Credit',
        'customer_id': test_customer.id
    }
    
    debit_payment = {
         'payment_method': 'Debit',
        'bankName': 'ANZ Bank',
        'debitCardNumber': '1111111111111111',
        'paymentAmount': Decimal('50.00'),
        'paymentType': 'Debit',
        'customer_id': test_customer.id
    }
    
    payment_service.create_payment(**credit_payment)
    payment_service.create_payment(**debit_payment)
    
    # Get payments by customer
    results = payment_service.get_payment(customer_id=test_customer.id)
    assert isinstance(results, list)
    assert len(results) == 2
    assert all(payment.customer_id == test_customer.id for payment in results)

def test_create_payment_invalid_data(payment_service, test_customer):
    payment_data = {
        'payment_method': 'Credit',
        'cardNumber': '1111111111111111',
        # Missing other required fields
        'customer_id': test_customer.id
    }
    
    result = payment_service.create_payment(**payment_data)
    assert isinstance(result, str)

def test_create_payment_invalid_customer(payment_service):
    payment_data = {
        'payment_method': 'Credit',
        'cardNumber': '4111111111111111',
        'cardExpiryDate': '12/25',
        'cardHolder': 'Test Customer',
        'cardType': 'Visa',
        'cardCVV': '123',
        'paymentAmount': Decimal('100.00'),
        'paymentType': 'Purchase',
        'customer_id': 999999  # Invalid customer ID
    }
    
    result = payment_service.create_payment(**payment_data)
    assert isinstance(result, str)

def test_get_payment_nonexistent_id(payment_service):
    result = payment_service.get_payment(id=999999)
    assert result is None or isinstance(result, str)