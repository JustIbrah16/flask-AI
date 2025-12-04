from extensions import db




class MaritalStatus(db.Model):
    __tablename__ = 'marital_statuses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

