import pytest
from decimal import Decimal
from datetime import datetime
from werkzeug.security import generate_password_hash
from app.data_access.payment_repository import PaymentRepository
from app.data_access.person_repository import PersonRepository
from app.models.Payment import *
from app.models.Person import *

@pytest.fixture
def payment_repository(db_session):
    return PaymentRepository(db_session)

@pytest.fixture
def person_repository(db_session):
    return PersonRepository(db_session)

@pytest.fixture
def test_customer(person_repository):
    customer = PrivateCustomer(
        username='test2',
        password_hash=generate_password_hash('123456'),
        custID=person_repository.generate_customer_id(),
        firstName='B',
        lastName='Test',
        custBalance=Decimal('50.00'),
        custAddress='123 road',
        maxOwing=Decimal('100.00')
    )
    return person_repository.add_user(customer)

def test_generate_payment_id(payment_repository):
    payment_id = payment_repository.generate_payment_id()
    
    assert len(payment_id) == 17
    datetime.strptime(payment_id[:14], '%Y%m%d%H%M%S')
    assert payment_id[14:].isdigit()
    assert int(payment_id[14:]) < 1000

def test_create_credit_card_payment(payment_repository, test_customer):
    payment = CreditCardPayment(
        paymentID=payment_repository.generate_payment_id(),
        cardNumber='1234123412341234',
        cardExpiryDate='12/25',
        cardHolder='A',
        cardType='Visa',
        cardCVV='123',
        paymentAmount=Decimal('20.00'),
        paymentType='Balance',
        customer_id=test_customer.id
    )
    
    result = payment_repository.create_payment(payment)
    assert isinstance(result, CreditCardPayment)
    assert result.cardNumber == '1234123412341234'
    assert result.cardHolder == 'A'
    assert result.paymentAmount == Decimal('20.00')
    assert result.customer_id == test_customer.id

def test_create_debit_card_payment(payment_repository, test_customer):
    payment = DebitCardPayment(
        paymentID=payment_repository.generate_payment_id(),
        bankName='ANZ Bank',
        debitCardNumber='1111111111111111',
        paymentAmount=Decimal('50.00'),
        paymentType='Direct',
        customer_id=test_customer.id
    )
    
    result = payment_repository.create_payment(payment)
    assert isinstance(result, DebitCardPayment)
    assert result.bankName == 'ANZ Bank'
    assert result.debitCardNumber == '1111111111111111'
    assert result.paymentAmount == Decimal('50.00')
    assert result.customer_id == test_customer.id

def test_get_payment_by_id(payment_repository, test_customer):
    payment = CreditCardPayment(
        paymentID=payment_repository.generate_payment_id(),
        cardNumber='1234123412341234',
        cardExpiryDate='12/25',
        cardHolder='A',
        cardType='Visa',
        cardCVV='123',
        paymentAmount=Decimal('20.00'),
        paymentType='Balance',
        customer_id=test_customer.id
    )
    
    created_payment = payment_repository.create_payment(payment)
    
    result = payment_repository.get_payment(id=created_payment.id)
    assert result.paymentID == created_payment.paymentID
    assert result.paymentAmount == Decimal('20.00')
    assert isinstance(result, CreditCardPayment)

def test_get_payments_by_customer(payment_repository, test_customer):
    payments = [
        CreditCardPayment(
            paymentID=payment_repository.generate_payment_id(),
            cardNumber='1234123412341234',
            cardExpiryDate='12/25',
            cardHolder='A',
            cardType='Visa',
            cardCVV='123',
            paymentAmount=Decimal('20.00'),
            paymentType='Balance',
            customer_id=test_customer.id
        ),
        DebitCardPayment(
            paymentID=payment_repository.generate_payment_id(),
            bankName='ANZ Bank',
            debitCardNumber='1111111111111111',
            paymentAmount=Decimal('50.00'),
            paymentType='Direct',
            customer_id=test_customer.id
        )
    ]
    
    for payment in payments:
        payment_repository.create_payment(payment)
    
    results = payment_repository.get_payment(customer_id=test_customer.id)
    assert isinstance(results, list)
    assert len(results) >= 2
    assert all(payment.customer_id == test_customer.id for payment in results)

def test_get_all_payments(payment_repository, test_customer):
    payments = [
        CreditCardPayment(
            paymentID=payment_repository.generate_payment_id(),
            cardNumber='1234123412341234',
            cardExpiryDate='12/25',
            cardHolder='A',
            cardType='Visa',
            cardCVV='123',
            paymentAmount=Decimal('20.00'),
            paymentType='Balance',
            customer_id=test_customer.id
        ),
        DebitCardPayment(
            paymentID=payment_repository.generate_payment_id(),
            bankName='ANZ Bank',
            debitCardNumber='1111111111111111',
            paymentAmount=Decimal('50.00'),
            paymentType='Direct',
            customer_id=test_customer.id
        )
    ]
    
    for payment in payments:
        payment_repository.create_payment(payment)
    
    results = payment_repository.get_payment()
    assert isinstance(results, list)
    assert len(results) >= 2

def test_create_payment_with_invalid_data(payment_repository, test_customer):
    payment = CreditCardPayment(
        paymentID=payment_repository.generate_payment_id(),
        cardNumber='1234123412341234',
        cardExpiryDate='12/25',
        cardHolder='A',
        cardType='Visa',
        cardCVV='123',
        paymentAmount=Decimal('20.00'),
        paymentType='Balance',
        customer_id=999999  # Invalid ID
    )
    
    result = payment_repository.create_payment(payment)
    assert isinstance(result, str)