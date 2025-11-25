from extensions import db
from Modulos.vacations.models import VacationRequest

class VacationRepository:
    @staticmethod
    def get_all():
        return VacationRequest.query.all()

    @staticmethod
    def get_by_id(req_id):
        return VacationRequest.query.get(req_id)

    @staticmethod
    def create(data):
        req = VacationRequest(**data)
        db.session.add(req)
        db.session.commit()
        return req

    @staticmethod
    def update(req):
        db.session.add(req)
        db.session.commit()
        return req

    @staticmethod
    def delete(req):
        db.session.delete(req)
        db.session.commit()
