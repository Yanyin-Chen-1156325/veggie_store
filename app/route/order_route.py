from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_required, current_user
from decimal import Decimal
from app.service import *
from app.models.Order import OrderStatus
from .. import db

order = Blueprint('order', __name__)
orderRepository = OrderRepository(db.session)
orderService = OrderService(orderRepository)
personRepository = PersonRepository(db.session)
personService = PersonService(personRepository)
settingRepository = SettingRepository(db.session)
settingService = SettingService(settingRepository)

def format_decimal(value):
    return Decimal(str(value)).quantize(Decimal('0.01'))

@order.route('/order/add_to_list', methods=['POST'])
@login_required
def add_to_list():
    if 'user_id' not in session or session['user_id'] != current_user.id:
        session['shopping_list'] = []
        session['user_id'] = current_user.id
    
    name = request.form.get('name')
    value = request.form.get('singleprice')
    quantity = request.form.get('quantity')
    current_tab = request.form.get('current_tab')
    if current_tab == 'premadebox':
        boxitem_items = request.form.getlist('boxitem_item')
        items = []
        for item_str in boxitem_items:
            _type, _name, _quantity, _price = item_str.split(',')
            items.append({
                'type': _type,
                'name': _name,
                'quantity': _quantity,
                'value': _price
            })

    if not all([name, value, quantity]):
        flash('Missing required information', 'error')
        return redirect(url_for('product.list_products'))
    
    if 'shopping_list' not in session:
        session['shopping_list'] = []

    session['user_id'] = current_user.id

    item = {
        'type': current_tab,
        'name': name,
        'value': value,
        'quantity': quantity,
        'item_price': Decimal(value) * Decimal(quantity)
    }
    if current_tab == 'premadebox':
        item['boxitem'] = items

    for x in session['shopping_list']:
        if x['name'] == item['name']:
            x['quantity'] = int(x['quantity']) + int(item['quantity'])
            x['item_price'] = Decimal(x['item_price']) + Decimal(item['item_price'])
            session.modified = True
            flash('Item added to your list', 'success')
            return redirect(url_for('product.list_products'))
    
    session['shopping_list'].append(item)
    session.modified = True  # Ensure the session is saved
    flash('Item added to your list', 'success')
    return redirect(url_for('product.list_products'))

@order.route('/order/view_list')
@login_required
def view_list():
    if 'shopping_list' not in session:
        session['shopping_list'] = []
    elif 'user_id' not in session or session['user_id'] != current_user.id:
        session['shopping_list'] = []

    weightList = orderService.get_grouped(session['shopping_list'], 'weight')
    packList = orderService.get_grouped(session['shopping_list'], 'pack')
    unitList = orderService.get_grouped(session['shopping_list'], 'unit')
    premadebox = orderService.get_grouped(session['shopping_list'], 'premadebox')
    order_price = sum([format_decimal(item['item_price']) for item in session['shopping_list']])
    max_distance = settingService.get_setting(**{'type':'ShoppingList_form', 'name':'max_distance'})
    max_distance = max_distance[0].value if max_distance else None
    delivery_fee = settingService.get_setting(**{'type':'ShoppingList_form', 'name':'delivery_fee'})
    delivery_fee = delivery_fee[0].value if delivery_fee else None
    return render_template('shopping_list.html', order_price=order_price, weightList=weightList, packList=packList, unitList=unitList, premadebox=premadebox, max_distance=max_distance, delivery_fee=delivery_fee)

@order.route('/order/remove_from_list', methods=['POST'])
@login_required
def remove_from_list():
    name = request.form.get('name')
    if 'shopping_list' in session:
        for item in session['shopping_list']:
            if item['name'] == name:
                session['shopping_list'].remove(item)
                session.modified = True
                flash('Item removed from your list', 'success')
                break
    return redirect(url_for('order.view_list'))

@order.route('/order/clear_list')
@login_required
def clear_list():
    session.pop('shopping_list', None)
    flash('Your shopping list has been cleared', 'success')
    return redirect(url_for('product.list_products'))

@order.route('/order/place_order', methods=['POST'])
@login_required
def place_order():
    if 'shopping_list' not in session or not session['shopping_list']:
        flash('Your shopping list is empty', 'error')
        return redirect(url_for('product.view_list'))
    total_price = request.form.get('total_price')
    order = {
        'username': current_user.username,
        'customer_id': current_user.id,
        'orderPrice': request.form.get('order_price'),
        'totalAmount': total_price,
        'deliveryMethod': request.form.get('deliveryMethod'),
        'deliveryDistance': request.form.get('deliveryDistance') if request.form.get('deliveryDistance') else None,
        'paymentMethod': 'Balance' if request.form.get('paymentType') == 'later' else None,
        'deliveryFee': request.form.get('delivery_fee') if request.form.get('delivery_fee') else None,
        'discountAmount': request.form.get('discount_amount') if request.form.get('discount_amount') else None,
        'items': session.get('shopping_list', [])
    }

    if current_user.type == 'corporatecustomer':
        if orderService.check_minbalance(format_decimal(current_user.minBalance), format_decimal(order['totalAmount'])) is not True:
            flash('Failed to place order. The total amount is less than the minimum balance for corporate customers.', 'error')
            return redirect(url_for('order.view_list'))

    rlt = orderService.place_order(**order)
    if isinstance(rlt, str) is not True:
        if rlt.paymentMethod == 'Balance':
            rlt = personService.update_balance(current_user.id, total_price)
            session.pop('shopping_list', None)
            flash('Order placed successfully', 'success')
            return redirect(url_for('order.view_list'))
        else:
            flash('Order placed successfully', 'success')
            return redirect(url_for('payment.pay', order_id=rlt.id))
    else:
        flash('Failed to place order.' + rlt, 'error')
        return redirect(url_for('order.view_list'))
    
@order.route('/order')
@login_required
def list_orders():
    if current_user.type == 'staff':
        orders = orderService.get_Order()
    else:
        orders = orderService.get_Order(None, current_user.username)
    return render_template('order_list.html', orders=orders)

@order.route('/order/view_order', methods=['GET'])
@login_required
def view_order():
    order_id = request.args.get('id')
    order = orderService.get_Order(order_id)
    return render_template('order_form.html', order=order)
    
@order.route('/order/update_status', methods=['POST'])
@login_required
def update_status():
    order_id = request.form.get('id')
    action = request.form.get('action')

    ck = orderService.get_Order(order_id)
    if action == 'cancel':
        if ck.paymentMethod == 'Balance':
            rlt = personService.update_balance(ck.customer_id, -ck.totalAmount)
            if isinstance(rlt, str) is True:
                flash('Failed to update balance. ' + rlt, 'error')
                return redirect(url_for('order.view_order', id=ck.id))
            else:
                pass
        else:
            flash(f'Payment has been returned to [{ ck.paymentMethod} Card]', 'success')
           
        rlt = orderService.update_order(order_id, OrderStatus.CANCELLED.value)
        if isinstance(rlt, str) is not True:
            flash('Order cancelled successfully', 'success')
        else:
            flash('Failed to update order status. ' + rlt, 'error')
        return redirect(url_for('order.view_order', id=ck.id))

    if action == 'accept':
        rlt = orderService.update_order(order_id, OrderStatus.ACCEPTED.value)
    elif action =='delivery':
        rlt = orderService.update_order(order_id, OrderStatus.DELIVERY.value)
    elif action == 'pickup':
        rlt = orderService.update_order(order_id, OrderStatus.PICK_UP.value)
    elif action == 'complete':
        rlt = orderService.update_order(order_id, OrderStatus.COMPLETED.value)

    if isinstance(rlt, str) is not True:
        flash(f'Order {action} successfully', 'success')  
    else:
        flash('Failed to update order status. ' + rlt, 'error')
    return redirect(url_for('order.view_order', id=ck.id))



