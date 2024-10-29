from flask import Blueprint, render_template
from flask_login import login_required
from app.service import *
from .. import db

product = Blueprint('product', __name__)
settingRepository = SettingRepository(db.session)
settingService = SettingService(settingRepository)

@product.route('/product')
@login_required
def list_products():
    premadeboxs = settingService.get_setting(**{'type':'Premadebox', 'name':'size_num_price'})
    small_box = settingService.get_setting(**{'type':'Product_form', 'name':'Premadebox_S'})
    medium_box = settingService.get_setting(**{'type':'Product_form', 'name':'Premadebox_M'})
    large_box = settingService.get_setting(**{'type':'Product_form', 'name':'Premadebox_L'})
    weighted_veggies = settingService.get_setting(**{'type':'weightedveggie'})
    pack_veggies = settingService.get_setting(**{'type':'packveggie'})
    unit_price_veggies = settingService.get_setting(**{'type':'unitpriceveggie'})
    return render_template('product_list.html', premadeboxs=premadeboxs, weighted_veggies=weighted_veggies, pack_veggies=pack_veggies, unit_price_veggies=unit_price_veggies, small_box=small_box, medium_box=medium_box, large_box=large_box)

