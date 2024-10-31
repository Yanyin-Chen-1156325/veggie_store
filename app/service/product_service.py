from app.data_access.product_repository import ProductRepository
from app.models.Product import *

class ProductService:
    """! ProductService class for business logic.
    This class contains methods to interact with the ProductRepository class.
    """
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def veggie_exists(self, vegName):
        """! Check if a veggie exists in the DB.
        @param vegName: Veggie name.
        @return: Veggie object if the veggie exists, None otherwise.
        """
        return self.product_repository.veggie_exists(vegName)
    
    def premadebox_exists(self, boxSize):
        """! Check if a premadebox exists in the DB.
        @param boxSize: Box size.
        @return: PremadeBox object if the box exists, None otherwise.
        """
        return self.product_repository.premadebox_exists(boxSize)

    def get_product(self, id=None, selectType=None):
        """! Get a product by ID or type or all products.
        @param id: Product ID.
        @param selectType: Product type.
        @return: Product object or list of Product objects.
        """
        return self.product_repository.get_product(id, selectType)
    
    def add_product(self, item):
        """! create a product.
        @param item: Product details.
        @return: Product object or error message.
        """
        try:
            if item['type'] == 'premadebox':
                premadebox = PremadeBox(
                    boxSize=item['name'],
                    numOfBoxes=item['quantity'],
                    boxPrice=item['value']
                    )
                
                rlt1 = self.product_repository.add_product(premadebox)
                if isinstance(rlt1, str) is True:
                    return rlt1
                
                veggies = []
                for veggie in item['boxitem']:
                    veggie_in_box = self.create_veggie(veggie, rlt1.numOfBoxes)
                    veggies.append(veggie_in_box)

                product = self.product_repository.update_premadebox_veggie(rlt1.id, veggies)
            else:
                product = self.create_veggie(item) 

            return product
        except Exception as e:
            return str(e)
        
    def create_veggie(self, item, premadebox_quantity=None):
        """! Create a veggie.
        @param item: Veggie details.
        @return: Veggie object or error message.
        """
        try:
            if item['type'] == 'weight':
                product = WeightedVeggie(vegName=item['name'],
                                        weight=item['quantity'] if premadebox_quantity is None else float(item['quantity']) * int(premadebox_quantity),
                                        pricePerKilo=item['value'])
            elif item['type'] == 'pack':
                product = PackVeggie(vegName=item['name'],
                                    numOfPack=item['quantity'] if premadebox_quantity is None else int(item['quantity']) * int(premadebox_quantity),
                                    pricePerPack=item['value'])
            elif item['type'] == 'unit':
                product = UnitPriceVeggie(vegName=item['name'],
                                        quantity=item['quantity'] if premadebox_quantity is None else int(item['quantity']) * int(premadebox_quantity),
                                        pricePerUnit=item['value'])
            else:
                return "Invalid veggie type"
            
            return self.product_repository.add_product(product) 
        except Exception as e:
            return str(e)