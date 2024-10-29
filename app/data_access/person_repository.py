from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.Person import *

class PersonRepository:
    """! Person repository class for data access.
    This class contains methods to interact with the DB model of Person.
    """
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def username_exists(self, username):
        """! Check if a username already exists in the database."""
        return self.db_session.query(Person).filter_by(username=username).first()
    
    def get_user(self, id=None, selectType=None):
        """! Get a user by ID or type or all users."""
        if id:
            return self.db_session.query(Person).get(id)     
        elif selectType:
            return self.db_session.query(Person).filter(or_(Person.type.ilike(f'%{selectType}'))).all()
        else:
            return self.db_session.query(Person).all()
    
    def generate_staff_id(self):
        """! Generate a unique employee ID for each staff member. starts with '000001', 6 digits long."""
        max_id = self.db_session.query(db.func.max(Staff.staffID)).scalar()
        if max_id:
            next_id = int(max_id) + 1
        else:
            next_id = 1
        return f"{next_id:06d}"
    
    def generate_customer_id(self):
        """! Generate a unique customer ID for each customer. starts with '10000001', 8 digits long."""
        max_id = self.db_session.query(db.func.max(Customer.custID)).scalar()
        if max_id:
            next_id = int(max_id) + 1
        else:
            next_id = 10000001
        return str(next_id)
        
    def add_user(self, user):
        """! Add a new user to the database."""
        try:
            self.db_session.add(user)
            self.db_session.commit()
            return user
        
        except Exception as e:
            self.db_session.rollback()
            raise e
        
    def update_user(self, user_id, updated_data):
        """! Update a user's data."""
        try:
            user = self.db_session.query(Person).get(user_id)
            for key, value in updated_data.items():
                setattr(user, key, value)
            
            self.db_session.commit()
            return user

        except Exception as e:
            self.db_session.rollback()
            raise e
        
    def delete_user(self, user_id):
        """! Delete a user from the database."""
        try:
            user = self.db_session.query(Person).get(user_id)
            
            self.db_session.delete(user)
            self.db_session.commit()
            return True
        
        except Exception as e:
            self.db_session.rollback()
            raise e
    

    