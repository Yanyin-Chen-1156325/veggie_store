import pytest
from decimal import Decimal
from app.service.order_service import OrderService
from app.models.Order import Order, OrderStatus
from app.service.person_service import PersonService
from app.data_access.person_repository import PersonRepository

@pytest.fixture
def person_service(db_session):
    person_repository = PersonRepository(db_session)
    return PersonService(person_repository)

@pytest.fixture
def order_service(db_session):
    from app.data_access.order_repository import OrderRepository
    order_repository = OrderRepository(db_session)
    return OrderService(order_repository)

@pytest.fixture
def test_customer(person_service):
    """Create a test customer for orders"""
    customer_data = {
        'type': 'privatecustomer',
        'username': 'test2',
        'password': '123456',
        'firstName': 'B',
        'lastName': 'Test',
        'custBalance': '0.00',
        'custAddress': '123 road',
        'maxOwing': '100.00'
    }
    return person_service.add_user(**customer_data)

def test_place_order(order_service, test_customer):
    order_data = {
        'username': 'test2',
        'customer_id': test_customer.id,
        'orderPrice': Decimal('50.99'),
        'totalAmount': Decimal('60.99'),
        'deliveryMethod': 'Delivery',
        'deliveryDistance': 5,
        'deliveryFee': Decimal('10.00'),
        'paymentMethod': None,
        'isPaid': False,
        'items': [
            {
                'type': 'weight',
                'name': 'Carrot',
                'quantity': 2,
                'value': Decimal('2.99')
            }
        ]
    }
    
    order = order_service.place_order(**order_data)
    assert isinstance(order, Order)
    assert order.orderStatus == OrderStatus.PENDING.value
    assert order.orderPrice == float(order_data['orderPrice'])
    assert order.totalAmount == order_data['totalAmount']
    assert order.deliveryMethod == order_data['deliveryMethod']
    assert order.deliveryDistance == order_data['deliveryDistance']
    assert order.deliveryFee == order_data['deliveryFee']
    assert order.customer_id == test_customer.id
    
    assert len(order.orderitems) == 1
    item = order.orderitems[0]
    assert item.product.type == 'weightedveggie'
    assert item.product.vegName == 'Carrot'

def test_get_order_by_customer(order_service, test_customer):
    order_data = {
        'username': 'private',
        'customer_id': test_customer.id,
        'orderPrice': Decimal('29.90'),
        'totalAmount': Decimal('29.90'),
        'deliveryMethod': 'Pickup',
        'paymentMethod': 'Balance',
        'isPaid': True,
        'items': [
            {
                'type': 'weight',
                'name': 'Carrot',
                'quantity': 10,
                'value': Decimal('2.99')
            }
        ]
    }
    
    order = order_service.place_order(**order_data)
    assert isinstance(order, Order)
    
    results = order_service.get_Order(order_customer='private')
    assert isinstance(results, list)
    assert len(results) > 0
    assert all(order.orderCustomer == 'private' for order in results)

def test_update_order_status(order_service, test_customer):
    """Test updating order status"""
    order_data = {
        'username': 'private',
        'customer_id': test_customer.id,
        'orderPrice': Decimal('25.99'),
        'totalAmount': Decimal('25.99'),
        'deliveryMethod': 'Pickup',
        'paymentMethod': 'Balance',
        'isPaid': True,
        'items': [
            {
                'type': 'weight',
                'name': 'Carrot',
                'quantity': 2,
                'value': Decimal('2.99')
            }
        ]
    }
    
    order = order_service.place_order(**order_data)
    assert isinstance(order, Order)
    
    result = order_service.update_order(order.id, status=OrderStatus.ACCEPTED.value)
    assert result.orderStatus == OrderStatus.ACCEPTED.value

def test_invalid_order_status_update(order_service, test_customer):
    order_data = {
        'username': 'private',
        'customer_id': test_customer.id,
        'orderPrice': Decimal('29.90'),
        'totalAmount': Decimal('29.90'),
        'deliveryMethod': 'Pickup',
        'paymentMethod': 'Balance',
        'isPaid': True,
        'items': [
            {
                'type': 'weight',
                'name': 'Carrot',
                'quantity': 10,
                'value': Decimal('2.99')
            }
        ]
    }
    
    order = order_service.place_order(**order_data)
    assert isinstance(order, Order)
    
    result = order_service.update_order(order.id, status='INVALID_STATUS')
    assert isinstance(result, str)