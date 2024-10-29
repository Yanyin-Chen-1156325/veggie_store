from flask import Flask
from flask_login import LoginManager
import config
import data
import pymysql
from app.database import db, init_db

pymysql.install_as_MySQLdb()

login_manager = LoginManager()
login_manager.login_view = 'auth.home'

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{config.dbuser}:{config.dbpass}@{config.dbhost}:{config.dbport}/{config.dbname}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'COMP642 S2'

    init_db(app)
    login_manager.init_app(app)

    """! Register blueprints."""
    from .route.auth_route import auth as auth_blueprint
    from .route.person_route import person as person_blueprint
    from .route.product_route import product as product_blueprint
    from .route.order_route import order as order_blueprint
    from .route.payment_route import payment as payment_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(person_blueprint)
    app.register_blueprint(product_blueprint)
    app.register_blueprint(order_blueprint)
    app.register_blueprint(payment_blueprint)

    with app.app_context():
        db.create_all()

        """! Initialize the database with some data."""
        from app.service.setting_service import SettingService, SettingRepository
        setting_repository = SettingRepository(db.session)
        setting_service = SettingService(setting_repository)
        init_setting(setting_service, data.settings)
        from app.service.person_service import PersonService, PersonRepository
        person_repository = PersonRepository(db.session)
        person_service = PersonService(person_repository)
        init_person(person_service, data.staff, data.privatecustomer, data.corporatecustomer)

    return app

@login_manager.user_loader
def load_user(user_id):
    from .models import Person
    return Person.query.get(int(user_id))

def init_setting(setting_service, settings):
    for setting in settings:
        if not setting_service.get_setting(**setting):
            obj = setting_service.create_setting(**setting)

def init_person(person_service, staffs, private_customers, corporate_customers):
    for staff in staffs:
        if not person_service.username_exists(staff['username']):
            obj = person_service.add_user(**staff)

    for customer in private_customers:
        if not person_service.username_exists(customer['username']):
            obj = person_service.add_user(**customer)

    for customer in corporate_customers:
        if not person_service.username_exists(customer['username']):
            obj = person_service.add_user(**customer)