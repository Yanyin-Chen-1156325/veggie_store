import pytest
from app.service.setting_service import SettingService

@pytest.fixture
def setting_service(db_session):
    from app.data_access.setting_repository import SettingRepository
    setting_repository = SettingRepository(db_session)
    return SettingService(setting_repository)

def test_create_basic_setting(setting_service):
    setting_data = {
        'type': 'Person_form',
        'name': 'minbalance',
        'value': '10',
        'description': 'Default minimum balance rate for corporate customers'
    }
    
    result = setting_service.create_setting(**setting_data)
    assert result.type == setting_data['type']
    assert result.name == setting_data['name']
    assert result.value == setting_data['value']
    assert result.description == setting_data['description']

def test_create_premadebox_setting(setting_service):
    setting_data = {
        'type': 'Premadebox',
        'name': 'size_num_price',
        'value': 'M_5_12.00',
        'description': 'Premadebox M'
    }
    
    result = setting_service.create_setting(**setting_data)
    assert result.type == 'Premadebox'
    assert result.name == 'size_num_price'
    assert result.value == 'M_5_12.00'

def test_get_premadebox_settings(setting_service):
    setting_data = {
        'type': 'Premadebox',
        'name': 'size_num_price',
        'value': 'L_7_23.00',
        'description': 'Premadebox L'
    }
    setting_service.create_setting(**setting_data)
    
    result = setting_service.get_setting(type='Premadebox')
    assert isinstance(result, list)
    assert len(result) > 0
    assert 'size' in result[0]
    assert 'num' in result[0]
    assert 'price' in result[0]
    assert result[0]['size'] == 'L'
    assert result[0]['num'] == '7'
    assert result[0]['price'] == '23.00'

def test_create_product_form_setting(setting_service):
    setting_data = {
        'type': 'Product_form',
        'name': 'Premadebox_S',
        'value': 'Avocad_2_unit_1.98',
        'description': 'Premadebox Small with 3 items'
    }
    
    result = setting_service.create_setting(**setting_data)
    assert result.type == 'Product_form'
    assert result.name.startswith('Premadebox_')
    assert result.value.count('_') == 3 

def test_get_product_form_premadebox_settings(setting_service):
    setting_data = {
        'type': 'Product_form',
        'name': 'Premadebox_S',
        'value': 'Banana_1_weight_3.8',
        'description': 'Premadebox Small with 3 items'
    }
    setting_service.create_setting(**setting_data)
    
    result = setting_service.get_setting(type='Product_form', name='Premadebox_S')
    assert isinstance(result, list)
    assert len(result) > 0
    assert 'type' in result[0]
    assert 'name' in result[0]
    assert 'quantity' in result[0]
    assert 'price' in result[0]
    assert result[0]['name'] == 'Banana'
    assert result[0]['type'] == 'weight'

def test_empty_settings(setting_service):
    result = setting_service.get_setting(type='NonExistent')
    assert isinstance(result, list)
    assert len(result) == 0

def test_create_invalid_setting(setting_service):
    invalid_setting = {
        'type': 'Basic'
        # Missing name and value
    }
    
    with pytest.raises(Exception):
        setting_service.create_setting(**invalid_setting)