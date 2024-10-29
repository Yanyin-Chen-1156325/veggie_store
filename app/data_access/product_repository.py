from sqlalchemy.orm import Session
from app.models.Product import *

class ProductRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def veggie_exists(self, vegName):
        return self.db_session.query(Veggie).filter_by(vegName=vegName).first()

    def premadebox_exists(self, boxSize):
        return self.db_session.query(PremadeBox).filter_by(boxSize=boxSize).first()

    def get_product(self, id=None, selectType=None):
        if id:
            return self.db_session.query(Product).get(id)
        elif selectType:
                self.db_session.query(Product).filter_by(type=selectType).all() 
        else:
            return self.db_session.query(Product).all()
        
    def add_product(self, product):
        try:
            self.db_session.add(product)
            self.db_session.commit()
            return product
        except Exception as e:
            self.db_session.rollback()
            return str(e)
        
    def update_premadebox_veggie(self, product_id, veggies):
        try:
            product = self.db_session.query(PremadeBox).get(product_id)
            product.veggies = veggies
            self.db_session.commit()
            return product
        except Exception as e:
            return str(e)
    