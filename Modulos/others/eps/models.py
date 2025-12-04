from extensions import db



class EPS(db.Model):
    __tablename__ = 'eps_providers'  # EPS = Empresa Promotora de Salud
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
