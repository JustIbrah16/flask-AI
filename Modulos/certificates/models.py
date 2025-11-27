from extensions import db
from datetime import datetime
from Modulos.employees.models import Employee # Importar Employee


class CertificateType(db.Model):
    __tablename__ = 'certificate_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=True)
    template = db.Column(db.Text, nullable=True)  # plantilla o contenido base
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'template': self.template,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class Certificate(db.Model):
    __tablename__ = 'certificates'
    id = db.Column(db.Integer, primary_key=True)

    certificate_type_id = db.Column(db.Integer, db.ForeignKey('certificate_types.id'))
    certificate_type = db.relationship('CertificateType', backref='certificates')

    # Información sobre el certificado generado
    created_by = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=True)
    creator = db.relationship('Employee', foreign_keys=[created_by], backref='created_certificates')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Datos básicos del sujeto del certificado (puedes adaptar según necesidades)
    subject_name = db.Column(db.String(200), nullable=False)
    subject_identificacion = db.Column(db.BigInteger, nullable=True)
    subject_email = db.Column(db.String(120), nullable=True)

    # Contenido final del certificado (HTML/Texto/JSON según uso)
    certificate_content = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'certificate_type_id': self.certificate_type_id,
            'certificate_type': self.certificate_type.name if self.certificate_type else None,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'subject_name': self.subject_name,
            'subject_identificacion': self.subject_identificacion,
            'subject_email': self.subject_email,
            'certificate_content': self.certificate_content,
        }
