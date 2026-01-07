from extensions import db


class StateEmploye(db.Model):
    __tablename__ = 'state_employe'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
