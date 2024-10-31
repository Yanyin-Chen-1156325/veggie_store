import pytest
from app.models.Setting import Setting
from app.data_access.setting_repository import SettingRepository

@pytest.fixture
def setting_repository(db_session):
    return SettingRepository(db_session)

def test_create_setting(setting_repository):
    setting_data = {
        'type': 'Person_form',
        'name': 'minbalance',
        'value': '10',
        'description': 'Default minimum balance rate for corporate customers'
    }
    
    result = setting_repository.create_setting(**setting_data)
    assert isinstance(result, Setting)
    assert result.type == setting_data['type']
    assert result.name == setting_data['name']
    assert result.value == setting_data['value']
    assert result.description == setting_data['description']

def test_get_setting_by_type(setting_repository):
    settings_data = [
        {
            'type': 'Person_form',
            'name': 'type',
            'value': 'privatecustomer',
            'description': 'Default person type in the form'
        },
        {
            'type': 'Person_form',
            'name': 'type',
            'value': 'corporatecustomer',
            'description': 'Default person type in the form'
        },
        {
            'type': 'Premadebox',
            'name': 'size_num_price',
            'value': 'S_3_5.00',
            'description': 'Premadebox S'
        }
    ]
    
    for setting in settings_data:
        setting_repository.create_setting(**setting)
    
    results = setting_repository.get_setting(type='Person_form')
    assert len(results) == 2
    assert all(result.type == 'Person_form' for result in results)

def test_get_setting_by_name(setting_repository):
    setting_data = {
        'type': 'Person_form',
        'name': 'minbalance',
        'value': '10',
        'description': 'Default minimum balance rate for corporate customers'
    }
    setting_repository.create_setting(**setting_data)
    
    results = setting_repository.get_setting(type='Person_form', name='minbalance')
    assert len(results) == 1
    assert results[0].name == 'minbalance'

def test_get_setting_multiple_filters(setting_repository):
    """Test getting settings with multiple filters"""
    # Create test settings
    setting_data = {
                'type': 'Person_form',
                'name': 'discount',
                'value': '0.1',
                'description': 'Default discount rate for corporate customers'
            }
    setting_repository.create_setting(**setting_data)
    
    # Test getting with multiple filters
    results = setting_repository.get_setting(
        type='Person_form',
        name='discount',
        value='0.1'
    )
    assert len(results) == 1
    assert results[0].type == 'Person_form'
    assert results[0].name == 'discount'
    assert results[0].value == '0.1'

def test_get_setting_no_results(setting_repository):
    results = setting_repository.get_setting(type='NonExistentType')
    assert isinstance(results, list)
    assert len(results) == 0

def test_get_premadebox_settings(setting_repository):
    """Test getting Premadebox settings"""
    setting_data = {
        'type': 'Premadebox',
        'name': 'size_num_price',
        'value': 'M_5_12.00',
        'description': 'Premadebox M'
    }

    setting_repository.create_setting(**setting_data)
    
    results = setting_repository.get_setting(type='Premadebox')
    assert len(results) == 1
    assert results[0].type == 'Premadebox'
    assert '_' in results[0].value

def test_get_product_form_settings(setting_repository):
    """Test getting Product_form settings"""
    setting_data = {
        'type': 'Product_form',
        'name': 'Premadebox_M',
        'value': 'Potato_1_weight_2.99',
        'description': 'Premadebox Small with 5 items',
    }
    
    setting_repository.create_setting(**setting_data)
    
    results = setting_repository.get_setting(type='Product_form')
    assert len(results) == 1
    assert results[0].type == 'Product_form'
    assert results[0].name.startswith('Premadebox_')