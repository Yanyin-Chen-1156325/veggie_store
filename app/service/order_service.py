from app.data_access.order_repository import OrderRepository
from app.models.Order import *
from .. import db
from datetime import datetime, timedelta

class OrderService:
    """! OrderService class for business logic.
    This class contains methods to interact with the OrderRepository class.
    """
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def get_grouped(self, lst, type):
        """! Get a list of products grouped by type.
        @param lst: List of products.
        @param type: Type of product.
        @return: List of products.
        """
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
        """! Get an order by ID or customer or all orders.
        @param order_id: Order ID.
        @param order_customer: Customer ID.
        @return: Order object or list of Order objects.
        """
        return self.order_repository.get_Order(order_id, order_customer)
    
    def place_order(self, **kwargs):
        """! Place an order.
        @param kwargs: Order details.
        @return: Order object or error message.
        """
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
                paymentMethod=kwargs.get('paymentMethod'),
                isPaid=kwargs.get('isPaid')
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
        """! Create an order item.
        @param order: Order object.
        @param index_item: Index of the item.
        @param item: Item details.
        @return: OrderItem object or error message.
        """
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
        
    def update_order(self, order_id, status=None, payment=None, isPaid=False):
        """! Update an order's status or payment method.
        @param order_id: Order ID.
        @param status: Order status.
        @param payment: Payment method.
        @return: Order object or error message.
        """
        try:
            return self.order_repository.update_order(order_id, status, payment, isPaid)
        except Exception as e:
            return str(e)
        
    def check_minbalance(self, minbalance, totalAmount):
        """! Check if the total amount is greater than the minimum balance for corporate customers.
        @param minbalance: Minimum balance.
        @param totalAmount: Total amount.
        @return: True if the total amount is greater than the minimum balance, False otherwise.
        """
        if minbalance > totalAmount:
            return False
        else:
            return True
        
    def get_daily_sales(self):
        """! Get daily sales.
        @return: Total amount and order count.
        """
        date = datetime.now().date()
        start_date = datetime.combine(date, datetime.min.time())  # 00:00:00
        end_date = datetime.combine(date, datetime.max.time())    # 23:59:59.999999

        daily_sales = self.order_repository.get_sales(start_date, end_date)

        if isinstance(daily_sales, str) is True:
            result = daily_sales
        else:
            result={
                'date': f"{start_date.strftime('%d-%m-%Y')} ~ ",
                'total_amount': float(daily_sales[0][0]) if daily_sales[0][0] else 0,
                'order_count': daily_sales[0][1] if  daily_sales[0][1] else 0
            }
        return result
    
    def get_weekly_sales(self):
        """! Get weekly sales.
        @return: Total amount and order count.
        """
        date = datetime.now().date()
        # Monday for the current week
        start_date = date - timedelta(days=date.weekday())
        start_date = datetime.combine(start_date, datetime.min.time())
        # Sunday for the current week
        end_date = start_date + timedelta(days=6)
        end_date = datetime.combine(end_date, datetime.max.time())
        
        weekly_sales = self.order_repository.get_sales(start_date, end_date)
        
        if isinstance(weekly_sales, str) is True:
            result = weekly_sales
        else:
            result={
                'date': f"{start_date.strftime('%d-%m-%Y')} ~ {end_date.strftime('%d-%m-%Y')}",
                'total_amount': float(weekly_sales[0][0]) if weekly_sales[0][0] else 0,
                'order_count': weekly_sales[0][1] if  weekly_sales[0][1] else 0
            }
        return result
    
    def get_monthly_sales(self):
        """! Get monthly sales.
        @return: Total amount and order count.
        """
        today = datetime.now()
        year = today.year
        month = today.month
        import calendar
        # Get the last day of the month
        _, last_day = calendar.monthrange(year, month)
        start_date = datetime(year, month, 1)
        end_date = datetime(year, month, last_day, 23, 59, 59, 999999)
        
        monthly_sales = self.order_repository.get_sales(start_date, end_date)
        
        if isinstance(monthly_sales, str) is True:
            result = monthly_sales
        else:
            result={
                'date': f"{start_date.strftime('%d-%m-%Y')} ~ {end_date.strftime('%d-%m-%Y')}",
                'total_amount': float(monthly_sales[0][0]) if monthly_sales[0][0] else 0,
                'order_count': monthly_sales[0][1] if  monthly_sales[0][1] else 0
            }
        return result
    
    def get_yearly_sales(self):
        """! Get yearly sales.
        @return: Total amount and order count.
        """
        year = datetime.now().year
        start_date = datetime(year, 1, 1)
        end_date = datetime(year, 12, 31, 23, 59, 59, 999999)

        yearly_sales = self.order_repository.get_sales(start_date, end_date)
        
        if isinstance(yearly_sales, str) is True:
            result = yearly_sales
        else:
            result={
                'date': f"{start_date.strftime('%d-%m-%Y')} ~ {end_date.strftime('%d-%m-%Y')}",
                'total_amount': float(yearly_sales[0][0]) if yearly_sales[0][0] else 0,
                'order_count': yearly_sales[0][1] if  yearly_sales[0][1] else 0
            }
        return result
    
    def get_top_products(self, limit=5):
        """! Get the top products by quantity sold
        @param limit: Number of top products. Default is 5.
        @return: List of top products.
        """
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