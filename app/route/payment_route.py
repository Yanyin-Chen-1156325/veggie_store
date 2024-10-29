from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_required, current_user
from app.service import *
from .. import db

payment = Blueprint('payment', __name__)
orderRepository = OrderRepository(db.session)
orderService = OrderService(orderRepository)
paymentRepository = PaymentRepository(db.session)
paymentService = PaymentService(paymentRepository)
personRepository = PersonRepository(db.session)
personService = PersonService(personRepository)

@payment.route('/payment')
@login_required
def list_payments():
    """! List payments. If the user is a staff, list all payments. If the user is a customer, list only their payments."""
    if current_user.type == 'staff':
        payments = paymentService.get_payment()
    else:
        payments = paymentService.get_payment(current_user.id)
    return render_template('payment_list.html', payments=payments)

@payment.route('/payment/view_payment', methods=['GET'])
@login_required
def view_payment():
    """! View a payment details."""
    payment_id = request.args.get('payment_id')
    payment = paymentService.get_payment(id=payment_id)
    return render_template('payment_form.html', payment=payment)

@payment.route('/make_a_payment')
@login_required
def pay():
    """! Payment page for making a payment."""
    order_id = request.args.get('order_id')
    order = None
    if order_id is not None:
        order = orderService.get_Order(order_id)
    return render_template('payment.html', order=order)

@payment.route('/payment/process_payment', methods=['POST'])
@login_required
def process_payment():
    """! Process a payment."""
    order_id = request.form.get('order_id')
    payment_method = request.form.get('payment_method')
    if payment_method == 'Credit':
        credit = {
            'payment_method': payment_method,
            'cardNumber': request.form.get('cardNumber'),
            'cardExpiryDate': request.form.get('cardExpiryDate'),
            'cardHolder': request.form.get('cardHolder'),
            'cardType': request.form.get('cardType'),
            'cardCVV': request.form.get('cardCVV'),
            'paymentAmount': request.form.get('paymentAmount'),
            'customer_id': current_user.id
        }
        rlt = paymentService.create_payment(**credit)
    elif payment_method == 'Debit':
        debit = {
            'payment_method': payment_method,
            'bankName': request.form.get('bankName'),
            'debitCardNumber': request.form.get('debitCardNumber'),
            'paymentAmount': request.form.get('paymentAmount'),
            'customer_id': current_user.id
        }
        rlt = paymentService.create_payment(**debit)
    else:
        rlt ='Invalid payment method'
    if isinstance(rlt, str) is not True:
        session.pop('shopping_list', None)
        flash('Process payment success', 'success')
        if order_id == '':
            rlt = personService.update_balance(current_user.id, -rlt.paymentAmount)
            return redirect(url_for('payment.list_payments'))
        else:
            rlt = orderService.update_order(order_id, None, payment_method) 
        if isinstance(rlt, str) is True:
            flash('Failed to update order payment or customer balance. ' + rlt, 'error')
    else:
        flash('Failed to process payment. ' + rlt, 'error')
    return redirect(url_for('order.view_order', id=order_id))