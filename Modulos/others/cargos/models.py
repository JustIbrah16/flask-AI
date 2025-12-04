from extensions import db




class Position(db.Model):
    __tablename__ = 'positions'  # cargos
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
