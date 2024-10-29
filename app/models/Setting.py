from app.database import db

class Setting(db.Model):
    __tablename__ = 'setting'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))

    def __str__(self):
        return f"<Setting {self.name}={self.value}>"
    