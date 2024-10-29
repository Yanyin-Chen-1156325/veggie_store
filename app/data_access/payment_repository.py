from sqlalchemy.orm import Session
from datetime import datetime
from app.models.Payment import *

class PaymentRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def generate_payment_id(self):
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
        if customer_id:
            return self.db_session.query(Payment).filter(Payment.customer_id == customer_id).all()
        elif id:
            return self.db_session.query(Payment).get(id)
        else:
            return self.db_session.query(Payment).all() 
    
    def create_payment(self, payment):
        try:
            self.db_session.add(payment)
            self.db_session.commit()
            return payment
        except Exception as e:
            return str(e)
    
    