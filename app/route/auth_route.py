from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_user, login_required, logout_user, current_user
from app.service import *
from .. import db

auth = Blueprint('auth', __name__)
personRepository = PersonRepository(db.session)
personService = PersonService(personRepository)

@auth.route('/')
def home():
    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = personService.username_exists(username)
        if user and personService.verify_password(user.password_hash, password):
            login_user(user)
            return redirect(url_for('product.list_products'))
        flash('Invalid username or password.', 'error')
    else:
        if current_user.is_authenticated:
            return redirect(url_for('product.list_products'))
        else:
            user = personService.get_user(1)
            username = user.username
            password = "123456"

    return render_template('login.html', username=username, password=password)

@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    session.pop('shopping_list', None)
    logout_user()
    return redirect(url_for('auth.home'))