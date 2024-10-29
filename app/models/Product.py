from app.database import db

premadebox_veggie = db.Table('premadebox_veggie',
    db.Column('premadebox_id', db.Integer, db.ForeignKey('premadebox.product_id')),
    db.Column('veggie_id', db.Integer, db.ForeignKey('veggie.product_id'))
)

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    type = db.Column(db.String(50), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'product',
        'polymorphic_on': type
    }

class PremadeBox(Product):
    __tablename__ = 'premadebox'
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    boxSize = db.Column(db.String(5), nullable=False)
    numOfBoxes = db.Column(db.Integer, nullable=False)
    boxPrice = db.Column(db.Numeric(10, 2), nullable=False)
    veggies = db.relationship('Veggie', secondary=premadebox_veggie) # many-to-many relationship

    __mapper_args__ = {
        'polymorphic_identity': 'premadebox',
    }

class Veggie(Product):
    __tablename__ = 'veggie'
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    vegName = db.Column(db.String(100), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'veggie',
    }

class WeightedVeggie(Veggie):
    __tablename__ = 'weightedveggie'
    veggie_id = db.Column(db.Integer, db.ForeignKey('veggie.product_id'), primary_key=True)
    weight = db.Column(db.Numeric(10, 2), nullable=False)
    pricePerKilo = db.Column(db.Numeric(10, 2), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'weightedveggie',
    }

class PackVeggie(Veggie):
    __tablename__ = 'packveggie'
    veggie_id = db.Column(db.Integer, db.ForeignKey('veggie.product_id'), primary_key=True)
    numOfPack = db.Column(db.Integer, nullable=False)
    pricePerPack = db.Column(db.Numeric(10, 2), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'packveggie',
    }

class UnitPriceVeggie(Veggie):
    __tablename__ = 'unitpriceveggie'
    veggie_id = db.Column(db.Integer, db.ForeignKey('veggie.product_id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    pricePerUnit = db.Column(db.Numeric(10, 2), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'unitpriceveggie',
    }