from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.service import *
from .. import db

person = Blueprint('person', __name__)
personRepository = PersonRepository(db.session)
personService = PersonService(personRepository)
orderRepository = OrderRepository(db.session)
orderService = OrderService(orderRepository)
settingRepository = SettingRepository(db.session)
settingService = SettingService(settingRepository)

@person.route('/person')
@login_required
def list_persons():
    if current_user.type == 'staff':
        selectType = request.args.get('select_type')
        if selectType:
            persons = personService.get_user(None, selectType)
        else:
            persons = personService.get_user()
    elif current_user.type in ['privatecustomer', 'corporatecustomer']:
        persons = [personService.get_user(current_user.id)]
    else:
        persons = []
    return render_template('person_list.html', persons=persons)

@person.route('/person/create', methods=['POST'])
@login_required
def create_person():
    mode = "add"
    if request.method == 'POST':
        person = {
            'type' : request.form.get('type'),
            'firstName' : request.form.get('firstName'),
            'lastName' : request.form.get('lastName'),
            'username' : request.form.get('username'),
            'password' : request.form.get('password'),
            'deptName' : request.form.get('deptName'),
            'custAddress' : request.form.get('custAddress'),
            'maxOwing' : request.form.get('maxOwing') if request.form.get('maxOwing') else settingService.get_setting(**{'type':'Person_form', 'name':'maxOwing'}),
            'discount' : request.form.get('discount'), 
            'minBalance' : request.form.get('minBalance'), 
            'custBalance' : 0
        }

        if not all([person['type'], person['firstName'], person['lastName'], person['username'], person['password']]):
            person_type = settingService.get_setting(**{'type':'Person_form', 'name':'type'})
            privateCust_maxOwing = settingService.get_setting(**{'type':'Person_form', 'name':'maxOwing'})
            privateCust_maxOwing = privateCust_maxOwing[0].value if privateCust_maxOwing else None
            corporateCust_discount = settingService.get_setting(**{'type':'Person_form', 'name':'discount'})
            corporateCust_discount = corporateCust_discount[0].value if corporateCust_discount else None
            corporateCust_minbalance = settingService.get_setting(**{'type':'Person_form', 'name':'minBalance'})
            corporateCust_minbalance = corporateCust_minbalance[0].value if corporateCust_minbalance else None
            return render_template('person_form.html', mode=mode, person_type=person_type, privateCust_maxOwing=privateCust_maxOwing, corporateCust_discount=corporateCust_discount, corporateCust_minbalance=corporateCust_minbalance)

        rlt = personService.add_user(**person)
        if isinstance(rlt, str) is not True:
            flash('User created successfully.','success')
            return redirect(url_for('person.view_person', id=rlt.id))  
        else:
            flash(f'Failed to create User. ' + rlt, 'error')
            if person['type'] == 'staff':
                select_type = 'staff'
            else:
                select_type = 'customer'
            return redirect(url_for('person.list_persons', select_type=select_type))
        
    return render_template('person_list.html')

@person.route('/person/edit', methods=['GET', 'POST'])
@login_required
def edit_person():
    mode = "edit"
    id = request.args.get('id')
    if request.method == 'POST':
        user = personService.get_user(id)
        person = {
            'id' : user.id,
            'type' : user.type,
            'firstName' : request.form.get('firstName'),
            'lastName' : request.form.get('lastName'),
            'username' : user.username,
            'password' : request.form.get('password'),
            'deptName' : request.form.get('deptName'),
            'custAddress' : request.form.get('custAddress'),
            'maxOwing' : request.form.get('maxOwing'),
            'discount' : request.form.get('discount'), 
            'minBalance' : request.form.get('minBalance'),
            'custBalance' : None if user.type == 'staff' else user.custBalance
        }

        rlt = personService.update_user(**person)
        if isinstance(rlt, str) is not True:
            flash('User updated successfully.', 'success')
        else:
            flash(f'Failed to update User. ID: ' + str(id) + ", " + rlt, 'error')
        return redirect(url_for('person.view_person', id=id))
    else:
        person = personService.get_user(id)
        person_type = settingService.get_setting(**{'type':'Person_form', 'name':'type'})
    return render_template('person_form.html', person=person, mode=mode, person_type=person_type)

@person.route('/person/view', methods=['GET'])
@login_required
def view_person():
    id = request.args.get('id')
    mode = "view"
    person = personService.get_user(id)
    return render_template('person_form.html', person=person, mode=mode)

@person.route('/person/delete', methods=['POST'])
@login_required
def delete_person():
    id = request.form.get('id')
    rlt = personService.delete_user(id)
    if isinstance(rlt, str) is not True:
            flash('User deleted successfully.' , 'success')
    else:
        flash(f'Failed to delete User. ID: ' + id + ", " + rlt, 'error')
    return redirect(url_for('person.list_persons'))

@person.route('/person/report')
@login_required
def sales_report():
    daily_sales = orderService.get_daily_sales()
    if isinstance(daily_sales, str) is True:
        flash(f'Failed to get daily sales. ' + daily_sales, 'error')
    weekly_sales = orderService.get_weekly_sales()
    if isinstance(weekly_sales, str) is True:
        flash(f'Failed to get weekly sales. ' + weekly_sales, 'error')
    monthly_sales = orderService.get_monthly_sales()
    if isinstance(monthly_sales, str) is True:
        flash(f'Failed to get monthly sales. ' + monthly_sales, 'error')
    yearly_sales = orderService.get_yearly_sales()
    if isinstance(yearly_sales, str) is True:
        flash(f'Failed to get yearly sales. ' + yearly_sales, 'error')
    top_products = orderService.get_top_products()
    if isinstance(top_products, str) is True:
        flash(f'Failed to get top products. ' + top_products, 'error')
    return render_template('report.html', daily_sales=daily_sales, weekly_sales=weekly_sales, monthly_sales=monthly_sales, yearly_sales=yearly_sales, top_products=top_products)