from sqlalchemy.orm import Session
from datetime import datetime
from app.models.Payment import *

class PaymentRepository:
    """! PaymentRepository class for data access.
    This class contains methods to interact with the DB model of Payment.
    """
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def generate_payment_id(self):
        """! Generate a unique payment ID for each payment. yyyyMMddHHmmSSfff, 17 digits long.
        @return: A unique payment ID.
        """
        try:
            db_time = db.session.query(
                db.func.concat(
                    db.func.date_format(db.func.now(6), '%Y%m%d%H%i%s'),
                    db.func.lpad(db.func.floor(db.func.microsecond(db.func.now(6))/1000), 3, '0')
                )).scalar()
            return db_time[:14] + db_time[14:17]
        except Exception as e:
            now = datetime.now()
            time_str = now.strftime('%Y%m%d%H%M%S%f')
            return time_str[:14] + time_str[14:17]
        
    def get_payment(self, customer_id=None, id=None):
        """! Get a payment by customer ID or ID or all payments.
        @param customer_id: Customer ID.
        @param id: Payment ID.
        @return: Payment object or list of Payment objects.
        """
        if customer_id:
            return self.db_session.query(Payment).filter(Payment.customer_id == customer_id).all()
        elif id:
            return self.db_session.query(Payment).get(id)
        else:
            return self.db_session.query(Payment).all() 
    
    def create_payment(self, payment):
        """! Create a payment.
        @param payment: Payment object.
        @return: Payment object or error message.
        """
        try:
            self.db_session.add(payment)
            self.db_session.commit()
            return payment
        except Exception as e:
            return str(e)
    
    