import pytest
from app.data_access.product_repository import ProductRepository
from app.models.Product import *

@pytest.fixture
def product_repository(db_session):
    return ProductRepository(db_session)

def test_add_weighted_veggie(product_repository):
    veggie = WeightedVeggie(
        vegName='Onion',
        weight=1.5,
        pricePerKilo=1.79
    )
    
    result = product_repository.add_product(veggie)
    assert isinstance(result, WeightedVeggie)
    assert result.vegName == 'Onion'
    assert result.weight == 1.5
    assert float(result.pricePerKilo) == 1.79
    assert result.type == 'weightedveggie'

def test_add_pack_veggie(product_repository):
    veggie = PackVeggie(
        vegName='Lettuce',
        numOfPack=2,
        pricePerPack=3.99
    )
    
    result = product_repository.add_product(veggie)
    assert isinstance(result, PackVeggie)
    assert result.vegName == 'Lettuce'
    assert result.numOfPack == 2
    assert float(result.pricePerPack) == 3.99
    assert result.type == 'packveggie'

def test_add_unit_veggie(product_repository):
    veggie = UnitPriceVeggie(
        vegName='Broccoli',
        quantity=3,
        pricePerUnit=2.49
    )
    
    result = product_repository.add_product(veggie)
    assert isinstance(result, UnitPriceVeggie)
    assert result.vegName == 'Broccoli'
    assert result.quantity == 3
    assert float(result.pricePerUnit) == 2.49
    assert result.type == 'unitpriceveggie'

def test_add_premadebox(product_repository):
    box = PremadeBox(
        boxSize='S',
        numOfBoxes=3,
        boxPrice=5
    )
    
    result = product_repository.add_product(box)
    assert isinstance(result, PremadeBox)
    assert result.boxSize == 'S'
    assert result.numOfBoxes == 3
    assert result.boxPrice == 5
    assert result.type == 'premadebox'

def test_get_product_by_id(product_repository):
    veggie = WeightedVeggie(
        vegName='Potato',
        weight=1.0,
        pricePerKilo=2.99
    )
    added_product = product_repository.add_product(veggie)
    
    result = product_repository.get_product(id=added_product.id)
    assert result.vegName == 'Potato'
    assert result.id == added_product.id

def test_update_premadebox_veggie(product_repository):
    box = PremadeBox(
        boxSize='S',
        numOfBoxes=3,
        boxPrice=5.00
    )
    box = product_repository.add_product(box)
    
    veggie1 = WeightedVeggie(
        vegName='Banana',
        weight=1.0,
        pricePerKilo=3.8
    )
    veggie2 = UnitPriceVeggie(
        vegName='Cucumber',
        quantity=1,
        pricePerUnit=1.99
    )
    veggie3 = UnitPriceVeggie(
        vegName='Avocado',
        quantity=2,
        pricePerUnit=1.98
    )
    
    veggies = [
        product_repository.add_product(veggie1),
        product_repository.add_product(veggie2),
        product_repository.add_product(veggie3)
    ]
    
    result = product_repository.update_premadebox_veggie(box.id, veggies)
    assert isinstance(result, PremadeBox)
    assert len(result.veggies) == 3
    assert any(v.vegName == 'Banana' for v in result.veggies)
    assert any(v.vegName == 'Cucumber' for v in result.veggies)
    assert any(v.vegName == 'Avocado' for v in result.veggies)

def test_get_all_products(product_repository):
    products = [
        WeightedVeggie(vegName='Kiwi', weight=1.0, pricePerKilo=5.99),
        PackVeggie(vegName='Spinach', numOfPack=2, pricePerPack=4.69),
    ]
    
    for product in products:
        product_repository.add_product(product)
    
    results = product_repository.get_product()
    assert any(p.type == 'weightedveggie' for p in results)
    assert any(p.type == 'packveggie' for p in results)