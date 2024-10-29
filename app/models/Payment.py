from app.database import db

class Payment(db.Model):
    __tablename__ = 'payment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    paymentAmount = db.Column(db.Numeric(10, 2), nullable=False)
    paymentDate = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    paymentID = db.Column(db.String(17), unique=True, nullable=False)
    paymentType = db.Column(db.String(10), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.person_id'))

    __mapper_args__ = {
        'polymorphic_identity': 'payment',
        'polymorphic_on': type
    }

class CreditCardPayment(Payment):
    __tablename__ = 'creditcardpayment'
    payment_id = db.Column(db.Integer, db.ForeignKey('payment.id'), primary_key=True)
    cardNumber = db.Column(db.String(16), nullable=False)
    cardExpiryDate = db.Column(db.String(7), nullable=False)
    cardHolder = db.Column(db.String(100), nullable=False)
    cardType = db.Column(db.String(20), nullable=False)
    cardCVV = db.Column(db.String(3), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'creditcardpayment',
    }

class DebitCardPayment(Payment):
    __tablename__ = 'debitcardpayment'
    payment_id = db.Column(db.Integer, db.ForeignKey('payment.id'), primary_key=True)
    bankName = db.Column(db.String(100), nullable=False)
    debitCardNumber = db.Column(db.String(16), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'debitcardpayment',
    }