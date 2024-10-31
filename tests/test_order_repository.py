import pytest
from decimal import Decimal
from datetime import datetime
from app.data_access.order_repository import OrderRepository
from app.data_access.product_repository import ProductRepository
from app.service.person_service import PersonService, PersonRepository
from app.models.Order import *
from app.models.Product import *
from app.models.Person import *


@pytest.fixture
def order_repository(db_session):
    return OrderRepository(db_session)

@pytest.fixture
def product_repository(db_session):
    return ProductRepository(db_session)

@pytest.fixture
def person_repository(db_session):
    return PersonRepository(db_session)

@pytest.fixture
def person_service(db_session):
    person_repository = PersonRepository(db_session)
    return PersonService(person_repository)

@pytest.fixture
def test_customer(person_repository, person_service):
    """Create a test customer for orders"""
    customer = PrivateCustomer(
        username='test2',
        password_hash=person_service.generate_hashed_password('123456'),
        custID=person_repository.generate_customer_id(),
        firstName='B',
        lastName='Test',
        custBalance=Decimal('0.00'),
        custAddress='123 road',
        maxOwing=Decimal('100.00')
    )
    return person_repository.add_user(customer)

@pytest.fixture
def sample_products(product_repository):
    products = {
        'weight': WeightedVeggie(
            vegName='Carrot',
            weight=1.5,
            pricePerKilo=2.8
        ),
        'pack': PackVeggie(
            vegName='Lettuce',
            numOfPack=2,
            pricePerPack=3.99
        ),
        'unit': UnitPriceVeggie(
            vegName='Broccoli',
            quantity=3,
            pricePerUnit=2.49
        )
    }
    
    for product in products.values():
        product_repository.add_product(product)
    
    return products


def test_place_order(order_repository, test_customer):
    order = Order(
        orderNumber=order_repository.generate_order_id(),
        orderCustomer='test2',
        customer_id=test_customer.id,
        orderStatus=OrderStatus.PENDING.value,
        orderPrice=Decimal('19.65'),
        totalAmount=Decimal('19.65'),
        deliveryMethod='Pickup',
        paymentMethod='None',
        isPaid=False
    )
    
    result = order_repository.place_order(order)
    assert isinstance(result, Order)
    assert result.orderStatus == OrderStatus.PENDING.value
    assert result.orderPrice == 19.65

def test_create_order_item(order_repository, sample_products, test_customer):
    order = Order(
        orderNumber=order_repository.generate_order_id(),
        orderCustomer='test_customer',
        customer_id=test_customer.id,
        orderStatus=OrderStatus.PENDING.value,
        orderPrice=Decimal('19.65'),
        totalAmount=Decimal('19.65'),
        deliveryMethod='Pickup',
        paymentMethod='None',
        isPaid=False
    )
    order = order_repository.place_order(order)
    
    orderitem = OrderItem(
        itemNumber=order_repository.generate_orderitem_id(order, 1),
        order_id=order.id
    )
    
    result = order_repository.create_orderitem(orderitem)
    assert isinstance(result, OrderItem)
    assert result.itemNumber.startswith(order.orderNumber)

def test_update_order_status(order_repository, test_customer):
    order = Order(
        orderNumber=order_repository.generate_order_id(),
        orderCustomer='test2',
        customer_id=test_customer.id,
        orderStatus=OrderStatus.PENDING.value,
        orderPrice=Decimal('19.65'),
        totalAmount=Decimal('19.65'),
        deliveryMethod='Pickup',
        paymentMethod='None',
        isPaid=False
    )
    order = order_repository.place_order(order)
    
    result = order_repository.update_order(order.id, status=OrderStatus.ACCEPTED.value)
    assert result.orderStatus == OrderStatus.ACCEPTED.value

def test_update_order_payment(order_repository, test_customer):
    order = Order(
        orderNumber=order_repository.generate_order_id(),
        orderCustomer='test2',
        customer_id=test_customer.id,
        orderStatus=OrderStatus.PENDING.value,
        orderPrice=Decimal('19.65'),
        totalAmount=Decimal('19.65'),
        deliveryMethod='Pickup',
        paymentMethod='None',
        isPaid=False
    )
    order = order_repository.place_order(order)
    
    result = order_repository.update_order(order.id, payment='Credit', isPaid=True)
    assert result.paymentMethod == 'Credit'
    assert result.isPaid is True

def test_update_orderitem_product(order_repository, sample_products, test_customer):
    order = Order(
        orderNumber=order_repository.generate_order_id(),
        orderCustomer='test_customer',
        customer_id=test_customer.id,
        orderStatus=OrderStatus.PENDING.value,
        orderPrice=Decimal('19.65'),
        totalAmount=Decimal('19.65'),
        deliveryMethod='Pickup',
        paymentMethod='None',
        isPaid=False
    )
    order = order_repository.place_order(order)
    
    orderitem = OrderItem(
        itemNumber=order_repository.generate_orderitem_id(order, 1),
        order_id=order.id
    )
    orderitem = order_repository.create_orderitem(orderitem)
    
    result = order_repository.update_orderitem_product(
        orderitem.itemNumber,
        sample_products['weight']
    )
    assert isinstance(result, OrderItem)
    assert result.product.vegName == 'Carrot'

def test_get_order_by_customer(order_repository, test_customer):
    customer_orders = []
    for i in range(2):
        order = Order(
            orderNumber=order_repository.generate_order_id(),
            orderCustomer='test2',
            customer_id=test_customer.id,
            orderStatus=OrderStatus.PENDING.value,
            orderPrice=Decimal('19.65'),
            totalAmount=Decimal('19.65'),
            deliveryMethod='Pickup',
            paymentMethod='None',
            isPaid=False
        )
        customer_orders.append(order_repository.place_order(order))
    
    results = order_repository.get_Order(order_customer='test2')
    assert len(results) >= 2
    assert all(order.orderCustomer == 'test2' for order in results)

def test_get_sales(order_repository, test_customer):
    today = datetime.now()
    
    # Day
    order1 = Order(
        orderNumber=order_repository.generate_order_id(),
        orderCustomer='test_customer',
        customer_id=test_customer.id,
        orderStatus=OrderStatus.COMPLETED.value,
        orderPrice=Decimal('19.65'),
        totalAmount=Decimal('19.65'),
        deliveryMethod='Pickup',
        paymentMethod='None',
        isPaid=False,
        orderDate=today
    )
    order_repository.place_order(order1)
    
    start_date = datetime.combine(today.date(), datetime.min.time())
    end_date = datetime.combine(today.date(), datetime.max.time())
    
    results = order_repository.get_sales(start_date, end_date)
    assert len(results) > 0
    assert results[0][0] >= Decimal('19.65') 
    assert results[0][1] >= 1 
