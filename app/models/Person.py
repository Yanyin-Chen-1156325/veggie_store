from app.database import db
from flask_login import UserMixin

class Person(UserMixin, db.Model):
    __tablename__ = 'person'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    firstName = db.Column(db.String(100), nullable=False)
    lastName = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'person',
        'polymorphic_on': type
    }
    
class Staff(Person):
    __tablename__ = "staff"
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)
    staffID = db.Column(db.String(6), unique=True, nullable=False)
    dateJoined = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    deptName = db.Column(db.String(100), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'staff',
    }

class Customer(Person):
    __tablename__ = 'customer'
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)
    custID = db.Column(db.String(8), unique=True, nullable=False)
    custBalance = db.Column(db.Numeric(10, 2), nullable=False)
    custAddress = db.Column(db.String(200), nullable=False)
    maxOwing = db.Column(db.Numeric(10, 2), nullable=False)
    payments = db.relationship('Payment', backref='customer') # one-to-many relationship
    orders = db.relationship('Order', backref='customer') # one-to-many relationship

    __mapper_args__ = {
        'polymorphic_identity': 'customer',
    }
    
class PrivateCustomer(Customer):
    __tablename__ = 'privatecustomer'
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.person_id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'privatecustomer',
    }

class CorporateCustomer(Customer):
    __tablename__ = 'corporatecustomer'
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.person_id'), primary_key=True)
    discount = db.Column(db.Numeric(3, 2), nullable=False)
    minBalance = db.Column(db.Numeric(10, 2), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'corporatecustomer',
    }