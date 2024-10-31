import pytest
from app.service.product_service import *
from app.models.Product import *

@pytest.fixture
def product_service(db_session):
    product_repository = ProductRepository(db_session)
    return ProductService(product_repository)

def test_add_weighted_veggie(product_service):
    veggie_data = {
        'type': 'weight',
        'name': 'Carrot',
        'quantity': 1.5,
        'value': 3
    }
    
    result = product_service.create_veggie(veggie_data)
    assert isinstance(result, WeightedVeggie)
    assert result.vegName == veggie_data['name']
    assert result.weight == veggie_data['quantity']
    assert result.pricePerKilo == veggie_data['value']
    assert result.type == 'weightedveggie'

def test_add_pack_veggie(product_service):
    veggie_data = {
        'type': 'pack',
        'name': 'Mushrooms',
        'quantity': 2,
        'value': 3
    }
    
    result = product_service.create_veggie(veggie_data)
    assert isinstance(result, PackVeggie)
    assert result.vegName == veggie_data['name']
    assert result.numOfPack == veggie_data['quantity']
    assert result.pricePerPack == veggie_data['value']
    assert result.type == 'packveggie'

def test_add_unit_veggie(product_service):
    veggie_data = {
        'type': 'unit',
        'name': 'Lettuce',
        'quantity': 3,
        'value': 2
    }
    
    result = product_service.create_veggie(veggie_data)
    assert isinstance(result, UnitPriceVeggie)
    assert result.vegName == veggie_data['name']
    assert result.quantity == veggie_data['quantity']
    assert result.pricePerUnit == veggie_data['value']
    assert result.type == 'unitpriceveggie'

def test_add_premade_box(product_service):
    box_data = {
        'type': 'premadebox',
        'name': 'S',
        'quantity': 10,
        'value': 30,
        'boxitem': [
            {
                'type': 'weight',
                'name': 'Potato',
                'quantity': 2.0,
                'value': 2
            },
            {
                'type': 'pack',
                'name': 'Tomatoes',
                'quantity': 1,
                'value': 3
            }
        ]
    }
    
    result = product_service.add_product(box_data)
    assert isinstance(result, PremadeBox)
    assert result.boxSize == box_data['name']
    assert result.numOfBoxes == box_data['quantity']
    assert result.boxPrice == box_data['value']
    assert len(result.veggies) == 2
    assert result.type == 'premadebox'

def test_get_product(product_service):
    veggie_data = {
        'type': 'weight',
        'name': 'Broccoli',
        'quantity': 0.5,
        'value': 5
    }
    
    product = product_service.create_veggie(veggie_data)
    
    result = product_service.get_product(id=product.id)
    assert result.vegName == veggie_data['name']

def test_veggie_exists(product_service):
    """Test veggie existence check"""
    veggie_data = {
        'type': 'weight',
        'name': 'Cucumber',
        'quantity': 1.0,
        'value': 2
    }
    
    product_service.create_veggie(veggie_data)
    
    assert product_service.veggie_exists('Cucumber') is not None
    assert product_service.veggie_exists('Banana') is None

def test_premadebox_exists(product_service):
    """Test premade box existence check"""
    box_data = {
        'type': 'premadebox',
        'name': 'M',
        'quantity': 5,
        'value': 35.99,
        'boxitem': []
    }
    
    product_service.add_product(box_data)
    
    assert product_service.premadebox_exists('M') is not None
    assert product_service.premadebox_exists('TEST') is None

def test_invalid_product_type(product_service):
    """Test adding product with invalid type"""
    invalid_data = {
        'type': 'invalid',
        'name': 'Mashroom',
        'quantity': 1,
        'value': 2
    }
    
    result = product_service.create_veggie(invalid_data)
    assert result == "Invalid veggie type"