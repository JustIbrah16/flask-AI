from extensions import db
from datetime import datetime
from Modulos.roles.models import Role




class Area(db.Model):
    __tablename__ = 'areas'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
