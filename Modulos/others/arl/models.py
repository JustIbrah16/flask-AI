from extensions import db



class ARL(db.Model):
    __tablename__ = 'arl_providers'  # ARL = Administradora de Riesgos Laborales
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

