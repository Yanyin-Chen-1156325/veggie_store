from .person_repository import PersonRepository
from .product_repository import ProductRepository
from .order_repository import OrderRepository
from .payment_repository import PaymentRepository
from .setting_repository import SettingRepository

"""! This is a list of all the modules that are imported when you use from app.data_access import *."""
__all__ = [
    'PersonRepository',
    'ProductRepository',
    'OrderRepository',
    'PaymentRepository',
    'SettingRepository'
    ] 