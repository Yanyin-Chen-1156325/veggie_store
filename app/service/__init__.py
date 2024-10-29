from .person_service import PersonService, PersonRepository
from .product_service import ProductService, ProductRepository
from .order_service import OrderService, OrderRepository
from .payment_service import PaymentService, PaymentRepository
from .setting_service import SettingService, SettingRepository

"""! This is a list of all the modules that are imported when you use from app.service import *."""
__all__ = [
    'SettingService', 'SettingRepository',
    'ProductService', 'ProductRepository',
    'OrderService', 'OrderRepository',
    'PaymentService', 'PaymentRepository',
    'PersonService',  'PersonRepository'
    ] 