from app.data_access.product_repository import ProductRepository
from app.models.Product import *

class ProductService:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def veggie_exists(self, vegName):
        return self.product_repository.veggie_exists(vegName)
    
    def premadebox_exists(self, boxSize):
        return self.product_repository.premadebox_exists(boxSize)

    def get_product(self, id=None, selectType=None):
        return self.product_repository.get_product(id, selectType)
    
    def add_product(self, item):
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
                    veggie_in_box = self.create_veggie(veggie)
                    veggies.append(veggie_in_box)

                product = self.product_repository.update_premadebox_veggie(rlt1.id, veggies)
            else:
                product = self.create_veggie(item) 

            return product
        except Exception as e:
            return str(e)
        
    def create_veggie(self, item):
        try:
            if item['type'] == 'weight':
                product = WeightedVeggie(vegName=item['name'],
                                        weight=item['quantity'],
                                        pricePerKilo=item['value'])
            elif item['type'] == 'pack':
                product = PackVeggie(vegName=item['name'],
                                    numOfPack=item['quantity'],
                                    pricePerPack=item['value'])
            elif item['type'] == 'unit':
                product = UnitPriceVeggie(vegName=item['name'],
                                        quantity=item['quantity'],
                                        pricePerUnit=item['value'])
            else:
                return "Invalid veggie type"
            
            return self.product_repository.add_product(product) 
        except Exception as e:
            return str(e)