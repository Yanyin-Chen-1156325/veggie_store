import pytest
import os
from flask import Flask
from flask_login import LoginManager
import pymysql
pymysql.install_as_MySQLdb()
import config
from app.database import db

@pytest.fixture
def app():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_path = os.path.join(base_dir, 'app', 'templates')
    app = Flask(__name__, template_folder=template_path)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{config.dbuser}:{config.dbpass}@{config.dbhost}:{config.dbport}/{config.dbname}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'testKey'
    
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)

    from app.route.auth_route import auth as auth_blueprint
    from app.route.person_route import person as person_blueprint
    from app.route.product_route import product as product_blueprint
    from app.route.order_route import order as order_blueprint
    from app.route.payment_route import payment as payment_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(person_blueprint)
    app.register_blueprint(product_blueprint)
    app.register_blueprint(order_blueprint)
    app.register_blueprint(payment_blueprint)

    
    with app.app_context():
        db.create_all()
    
    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def db_session(app):
    with app.app_context():
        db.create_all()
        yield db.session

        db.session.remove()
        db.session.commit()

