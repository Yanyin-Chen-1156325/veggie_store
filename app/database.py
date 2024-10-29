from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    """! Initialize the DB."""
    db.init_app(app)