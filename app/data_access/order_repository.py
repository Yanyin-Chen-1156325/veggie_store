from sqlalchemy.orm import Session
from app.models.Order import *
from app.models.Product import *

class OrderRepository:
    """! OrderRepository class for data access.
    This class contains methods to interact with the DB model of Order.
    """
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def generate_order_id(self):
        """! Generate a unique order ID for each order. starts with '1000000001', 10 digits long.
        @return: A unique order ID.
        """
        max_id = self.db_session.query(db.func.max(Order.orderNumber)).scalar()
        if max_id:
            next_id = int(max_id) + 1
        else:
            next_id = 1000000001
        return str(next_id)
    
    def generate_orderitem_id(self, order: Order, index):
        """! Generate a unique order item ID for each order item. OrderID + 6 digitals serial number.
        @param order: Order object.
        @param index: Serial number of the order item.
        @return: A unique order item ID.
        """
        index_str = str(index).zfill(6)
        return order.orderNumber + index_str
    
    def get_Order(self, order_id=None, order_customer=None):
        """! Get an order by ID or customer or all orders.
        @param order_id: Order ID.
        @param order_customer: Customer ID.
        @return: Order object or list of Order objects.
        """
        if order_id:
            return self.db_session.query(Order).get(order_id)
        elif order_customer:
            return self.db_session.query(Order).filter_by(orderCustomer=order_customer).all()
        else:
            return self.db_session.query(Order).all()
    
    def place_order(self, order):
        """! Place an order.
        @param order: Order object.
        @return: Order object or error message.
        """
        try:       
            self.db_session.add(order)
            self.db_session.commit()
            return order
        except Exception as e:
            return str(e)

    def create_orderitem(self, orderitem):
        """! Create an order item.
        @param orderitem: OrderItem object.
        @return: OrderItem object or error message.
        """
        try:       
            self.db_session.add(orderitem)
            self.db_session.commit()
            return orderitem
        except Exception as e:
            return str(e)
    
    def update_order(self, order_id, status=None, payment=None, isPaid=False):
        """! Update an order's status or payment method.
        @param order_id: Order ID.
        @param status: Order status.
        @param payment: Payment method.
        @return: Order object or error message.
        """
        order = self.db_session.query(Order).get(order_id)
        if status:
            order.orderStatus = status
        if payment:
            order.paymentMethod = payment
        if isPaid:
            order.isPaid = isPaid
        self.db_session.commit()
        return order
    
    def update_orderitem_product(self, orderitem_id, product):
        """! Update a conection between order item and product.
        @param orderitem_id: OrderItem ID.
        @param product: Product object.
        @return: OrderItem object or error message.
        """
        try:
            orderitem = self.db_session.query(OrderItem).get(orderitem_id)
            orderitem.product = product
            self.db_session.commit()
            return orderitem
        except Exception as e:
            return str(e)
        
    def update_order_orderitem(self, order_id, orderitems):
        """! Update a connection between order and order items.
        @param order_id: Order ID.
        @param orderitems: List of OrderItem objects.
        @return: Order object or error message.
        """
        try:
            order = self.db_session.query(Order).get(order_id)
            order.orderitems = orderitems
            self.db_session.commit()
            return order
        except Exception as e:
            return str(e)
        
    def get_sales(self, start_date, end_date):
        """! Get the total sales and number of orders between two dates. Excludes cancelled orders.
        @param start_date: Start date.
        @param end_date: End date.
        @return: List of total sales and number of orders.
        """
        try:
            sales = db.session.query(
                    db.func.sum(Order.totalAmount).label('total_amount'),
                    db.func.count(Order.id).label('order_count')
                ).filter(
                    Order.orderDate.between(start_date, end_date),
                    (Order.orderStatus != OrderStatus.CANCELLED.value)
                ).all()
            
            return sales
        except Exception as e: 
            return str(e)

    def get_active_orders_with_items(self):
        """! Get all non-cancelled orders with their items and products
        @return: List of orders with their items
        """
        try:
            orders = (
                self.db_session.query(Order)
                .filter(Order.orderStatus != OrderStatus.CANCELLED.value)
                .options(db.joinedload(Order.orderitems)
                        .joinedload(OrderItem.product))
                .all()
            )
            return orders
        except Exception as e:
            print(f"Error in get_active_orders: {str(e)}")
            return str(e)
        