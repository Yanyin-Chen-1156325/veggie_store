from app.database import db
from sqlalchemy.orm import backref
from enum import Enum

class OrderStatus(Enum):
    PENDING = "pending"
    CANCELLED = "cancelled" 
    ACCEPTED = "accepted"
    DELIVERY = "delivery"
    PICK_UP = "pick up"
    COMPLETED = "completed"               

class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    orderCustomer = db.Column(db.String(100), nullable=False) # username
    orderDate  = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    orderNumber = db.Column(db.String(10), unique=True, nullable=False)
    orderStatus = db.Column(db.String(10), nullable=False)
    orderPrice = db.Column(db.Float, nullable=False)
    deliveryMethod = db.Column(db.String(20), nullable=False) # delivery or pickup
    deliveryDistance = db.Column(db.Float, nullable=True)
    deliveryFee = db.Column(db.Numeric(10, 2), nullable=True)
    discountAmount = db.Column(db.Numeric(10, 2), nullable=True)
    totalAmount = db.Column(db.Numeric(10, 2), nullable=True)
    paymentMethod = db.Column(db.String(20), nullable=True) # credit card or debit card or balance
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.person_id'))
    orderitems = db.relationship('OrderItem', backref='order')

class OrderItem(db.Model):
    __tablename__ = 'orderitem'
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    itemNumber = db.Column(db.String(16), primary_key=True, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship('Product', backref=backref('orderitem', uselist=False))