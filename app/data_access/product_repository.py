from sqlalchemy.orm import Session
from app.models.Product import *

class ProductRepository:
    """! ProductRepository class for data access.
    This class contains methods to interact with the DB model of Product.
    """
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def veggie_exists(self, vegName):
        """! Check if a veggie exists in the DB.
        @param vegName: Veggie name.
        @return: Veggie object if the veggie exists, None otherwise.
        """
        return self.db_session.query(Veggie).filter_by(vegName=vegName).first()

    def premadebox_exists(self, boxSize):
        """! Check if a premade box exists in the DB.
        @param boxSize: Box size.
        @return: PremadeBox object if the box exists, None otherwise.
        """
        return self.db_session.query(PremadeBox).filter_by(boxSize=boxSize).first()

    def get_product(self, id=None, selectType=None):
        """! Get a product by ID or type or all products.
        @param id: Product ID.
        @param selectType: Product type.
        @return: Product object or list of Product objects.
        """
        if id:
            return self.db_session.query(Product).get(id)
        elif selectType:
                self.db_session.query(Product).filter_by(type=selectType).all() 
        else:
            return self.db_session.query(Product).all()
        
    def add_product(self, product):
        """! Add a product.
        @param product: Product object.
        @return: Product object or error message.
        """
        try:
            self.db_session.add(product)
            self.db_session.commit()
            return product
        except Exception as e:
            self.db_session.rollback()
            return str(e)
        
    def update_premadebox_veggie(self, product_id, veggies):
        """! Update a connection between premadeboxs and veggies.
        @param product_id: Product ID.
        @param veggies: List of veggies.
        @return: Product object or error message.
        """
        try:
            product = self.db_session.query(PremadeBox).get(product_id)
            product.veggies = veggies
            self.db_session.commit()
            return product
        except Exception as e:
            return str(e)
    