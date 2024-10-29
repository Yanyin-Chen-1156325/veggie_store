from werkzeug.security import generate_password_hash, check_password_hash
from decimal import Decimal
from app.data_access.person_repository import *

class PersonService:
    """! Person service class for business logic.
    This class contains methods to interact with the PersonRepository class.
    """
    def __init__(self, person_repository: PersonRepository):
        self.person_repository = person_repository

    def generate_hashed_password(self, password):
        """! Generate a hashed password."""
        return generate_password_hash(password)
    
    def verify_password(self, db_password, password):
        """! Verify a password against a hashed password."""
        return check_password_hash(db_password, password)

    def username_exists(self, username):
        """! Check if a username already exists in the database."""
        return self.person_repository.username_exists(username)
    
    def get_user(self, id=None, selectType=None):
        """! Get a user by ID or type or all users."""
        return self.person_repository.get_user(id, selectType)
    
    def add_user(self, **kwargs):
        """! Add a new user to the database."""
        try:
            if self.username_exists(kwargs.get('username')):
                return "Username already exists"
            
            user_type = kwargs.get('type')
            if user_type == 'staff':
                staff = Staff(
                    username=kwargs.get('username'),
                    staffID=self.person_repository.generate_staff_id(),
                    firstName=kwargs.get('firstName'),
                    lastName=kwargs.get('lastName'),
                    deptName=kwargs.get('deptName'),
                    dateJoined= db.func.now()
                    )
                staff.password_hash = self.generate_hashed_password(kwargs.get('password'))
                rlt = self.person_repository.add_user(staff)
            elif user_type == 'privatecustomer':
                privateCustomer = PrivateCustomer(
                    username=kwargs.get('username'),
                    custID=self.person_repository.generate_customer_id(),
                    firstName=kwargs.get('firstName'),
                    lastName=kwargs.get('lastName'),
                    custBalance= Decimal(kwargs.get('custBalance')),
                    custAddress=kwargs.get('custAddress'),
                    maxOwing=Decimal(kwargs.get('maxOwing'))
                    )
                privateCustomer.password_hash = self.generate_hashed_password(kwargs.get('password'))
                rlt = self.person_repository.add_user(privateCustomer)
            elif user_type == 'corporatecustomer':
                corporateCustomer = CorporateCustomer(
                    username=kwargs.get('username'),
                    custID=self.person_repository.generate_customer_id(),
                    firstName=kwargs.get('firstName'),
                    lastName=kwargs.get('lastName'),
                    custBalance= Decimal(kwargs.get('custBalance')),
                    custAddress=kwargs.get('custAddress'),
                    maxOwing=Decimal(kwargs.get('maxOwing')),
                    discount=kwargs.get('discount'),
                    minBalance=kwargs.get('minBalance')
                    )
                corporateCustomer.password_hash = self.generate_hashed_password(kwargs.get('password'))
                rlt = self.person_repository.add_user(corporateCustomer)
            else:
                rlt = "Invalid user type"
            return rlt  
        except Exception as e:
            return str(e)
        
    def update_user(self, **kwargs):
        """! Update a user's data."""
        try:
            user = self.get_user(kwargs.get('id'))
            if user is None:
                return f"No user found with ID: {kwargs.get('id')}"
            
            updated_data = {
                'firstName': kwargs.get('firstName'),
                'lastName': kwargs.get('lastName')
            }

            password = kwargs.get('password')
            if password and password.strip():
                updated_data['password_hash'] = self.generate_hashed_password(password)

            if user.type == 'staff':
                updated_data.update({
                    'deptName': kwargs.get('deptName')
                })
            elif user.type == 'privatecustomer':
                updated_data.update({
                    'custAddress': kwargs.get('custAddress'),
                    'maxOwing': kwargs.get('maxOwing')
                })
            elif user.type == 'corporatecustomer':
                updated_data.update({
                    'custAddress': kwargs.get('custAddress'),
                    'maxOwing': kwargs.get('maxOwing'),
                    'discount': kwargs.get('discount'),
                    'minBalance': kwargs.get('minBalance')
                })

            return self.person_repository.update_user(user.id, updated_data)
        except Exception as e:
            return str(e)
        
    def delete_user(self, user_id):
        """! Delete a user from the database."""
        try:
            user = self.get_user(user_id)
            if user is None:
                return f"No user found with ID: {user_id}"
            
            return self.person_repository.delete_user(user_id)
        except Exception as e:
            return str(e)
    
    def update_balance(self, user_id, amount):
        """! Update a user's balance which is the money user owning."""
        try:
            user = self.get_user(user_id)
            if user is None:
                return f"No user found with ID: {user_id}"
            
            if user.custBalance + Decimal(amount) <0:
                return f"Balance [{user.custBalance}] is less than the amount [{abs(amount)}]!"
            updated_data = {
                'custBalance': user.custBalance + Decimal(amount)
            }
            
            return self.person_repository.update_user(user_id, updated_data)
        except Exception as e:
            return str(e)