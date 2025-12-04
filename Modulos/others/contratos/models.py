from extensions import db

# Tablas maestras (plurales)


class ContractType(db.Model):
    __tablename__ = 'contract_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
