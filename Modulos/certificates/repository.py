from extensions import db
from Modulos.certificates.models import CertificateType, Certificate


class CertificateTypeRepository:
    @staticmethod
    def get_all():
        return CertificateType.query.order_by(CertificateType.name).all()

    @staticmethod
    def get_by_id(type_id):
        return CertificateType.query.get(type_id)

    @staticmethod
    def create(data):
        obj = CertificateType(**data)
        db.session.add(obj)
        db.session.commit()
        return obj

    @staticmethod
    def update(obj):
        db.session.add(obj)
        db.session.commit()
        return obj

    @staticmethod
    def delete(obj):
        db.session.delete(obj)
        db.session.commit()
        return True


class CertificateRepository:
    @staticmethod
    def get_all():
        return Certificate.query.order_by(Certificate.created_at.desc()).all()

    @staticmethod
    def get_by_id(cert_id):
        return Certificate.query.get(cert_id)

    @staticmethod
    def create(data):
        obj = Certificate(**data)
        db.session.add(obj)
        db.session.commit()
        return obj

    @staticmethod
    def update(obj):
        db.session.add(obj)
        db.session.commit()
        return obj

    @staticmethod
    def delete(obj):
        db.session.delete(obj)
        db.session.commit()
        return True

    @staticmethod
    def get_by_type(type_id):
        return Certificate.query.filter_by(certificate_type_id=type_id).order_by(Certificate.created_at.desc()).all()

    @staticmethod
    def get_by_subject_id(subject_id):
        return Certificate.query.filter_by(subject_identificacion=subject_id).order_by(Certificate.created_at.desc()).all()
