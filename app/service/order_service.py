from app.data_access.order_repository import OrderRepository
from app.models.Order import *
from .. import db
from datetime import datetime, timedelta
from decimal import Decimal


class OrderService:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def get_grouped(self, lst, type):
        rlt =[]
        if type == 'premadebox':
            for item in lst:
                if item['name'] in ['S', 'M', 'L']:
                    rlt.append(item)
        else:
            for item in lst:
                if item['type'] == type:
                    rlt.append(item)
            rlt_sort = sorted(rlt, key=lambda x: x['name'])
            rlt = rlt_sort
        return rlt
    
    def get_Order(self, order_id=None, order_customer=None):
        return self.order_repository.get_Order(order_id, order_customer)
    
    def place_order(self, **kwargs):
        try:
            order = Order(
                orderCustomer=kwargs.get('username'),
                customer_id=kwargs.get('customer_id'),
                orderNumber=self.order_repository.generate_order_id(),
                orderStatus=OrderStatus.PENDING.value,
                orderPrice=kwargs.get('orderPrice'),
                totalAmount=kwargs.get('totalAmount'),
                deliveryMethod=kwargs.get('deliveryMethod'),
                deliveryDistance=kwargs.get('deliveryDistance') if kwargs.get('deliveryDistance') else None,
                deliveryFee=kwargs.get('deliveryFee') if kwargs.get('deliveryFee') else None,
                discountAmount=kwargs.get('discountAmount') if kwargs.get('discountAmount') else None,
                paymentMethod=kwargs.get('paymentMethod')
                )
            rlt1 = self.order_repository.place_order(order)
            if isinstance(rlt1, str) is True:
                return rlt1
            
            orderitems = []
            for index_item in range(len(kwargs.get('items'))):
                orderitem = self._create_orderitem(rlt1, index_item + 1, kwargs.get('items')[index_item])
                orderitems.append(orderitem)

            rlt = self.order_repository.update_order_orderitem(rlt1.id, orderitems)
            return rlt
        except Exception as e:
            return str(e)
        
    def _create_orderitem(self, order: Order, index_item, item):
        orderitem = OrderItem(
            itemNumber=self.order_repository.generate_orderitem_id(order, index_item),
            order_id=order.id
            )
        rlt1 = self.order_repository.create_orderitem(orderitem)
        if isinstance(rlt1, str) is True:
            return rlt1
        
        from app.service.product_service import ProductService, ProductRepository
        productRepository = ProductRepository(self.order_repository.db_session)
        productService = ProductService(productRepository)
        rlt2 = productService.add_product(item)
        if isinstance(rlt2, str) is True:
            return rlt2
        
        rlt = self.order_repository.update_orderitem_product(rlt1.itemNumber, rlt2)
        return rlt
        
    def update_order(self, order_id, status=None, payment=None):
        try:
            return self.order_repository.update_order(order_id, status, payment)
        except Exception as e:
            return str(e)
        
    def check_minbalance(self, minbalance, totalAmount):
        if minbalance > totalAmount:
            return False
        else:
            return True
        
    def get_daily_sales(self):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=6)

        daily_sales = self.order_repository.get_sales(start_date, end_date)

        if isinstance(daily_sales, str) is True:
            result = daily_sales
        else:
            result={
                'date': f"{start_date.strftime("%d-%m-%Y %H:%M:%S")} ~ {end_date.strftime("%d-%m-%Y %H:%M:%S")}",
                'total_amount': float(daily_sales[0][0]) if daily_sales else 0,
                'order_count': daily_sales[0][1] if  daily_sales else 0
            }
        return result
    
    def get_weekly_sales(self):
        end_date = datetime.now()
        start_date = end_date - timedelta(weeks=1)
        
        weekly_sales = self.order_repository.get_sales(start_date, end_date)
        
        if isinstance(weekly_sales, str) is True:
            result = weekly_sales
        else:
            result={
                'date': f"{start_date.strftime("%d-%m-%Y")} ~ {end_date.strftime("%d-%m-%Y")}",
                'total_amount': float(weekly_sales[0][0]) if weekly_sales else 0,
                'order_count': weekly_sales[0][1] if  weekly_sales else 0
            }
        return result
    
    def get_monthly_sales(self):
        end_date = datetime.now()
        first_day = end_date.replace(day=1)
        last_month_last_day = first_day - timedelta(days=1)
        start_date = last_month_last_day.replace(day=1)
        
        monthly_sales = self.order_repository.get_sales(start_date, end_date)
        
        if isinstance(monthly_sales, str) is True:
            result = monthly_sales
        else:
            result={
                'date': f"{start_date.strftime("%d-%m-%Y")} ~ {end_date.strftime("%d-%m-%Y")}",
                'total_amount': float(monthly_sales[0][0]) if monthly_sales else 0,
                'order_count': monthly_sales[0][1] if  monthly_sales else 0
            }
        return result
    
    def get_yearly_sales(self):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)

        yearly_sales = self.order_repository.get_sales(start_date, end_date)
        
        if isinstance(yearly_sales, str) is True:
            result = yearly_sales
        else:
            result={
                'date': f"{start_date.strftime("%d-%m-%Y")} ~ {end_date.strftime("%d-%m-%Y")}",
                'total_amount': float(yearly_sales[0][0]) if yearly_sales else 0,
                'order_count': yearly_sales[0][1] if  yearly_sales else 0
            }
        return result
    
    def get_top_products(self, limit=5):
        top_products = self.order_repository.get_top_products(limit)
        
        if isinstance(top_products, str) is True:
            results = top_products
        else:
            results = [{
                'name': result[0],
                'quantity': float(result[2]) if result[2] else 0,
                'type': result[1],
            } for result in top_products]
        return results