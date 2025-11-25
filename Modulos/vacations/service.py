from extensions import db
from datetime import datetime
from Modulos.vacations.model import VacationRequest


class VacationService:

    @staticmethod
    def get_all_vacations():
        vacations = VacationRequest.query.all()
        return [v.to_dict() for v in vacations]

    @staticmethod
    def get_vacation(vacation_id):
        vacation = VacationRequest.query.get(vacation_id)
        if not vacation:
            return None
        return vacation.to_dict()

    @staticmethod
    def get_employee_vacations(employee_id):
        vacations = VacationRequest.query.filter_by(employee_id=employee_id).all()
        return [v.to_dict() for v in vacations]

    @staticmethod
    def create_vacation(data):
        try:
            vacation = VacationRequest(
                employee_id=data["employee_id"],
                start_date=datetime.strptime(data["start_date"], "%Y-%m-%d").date(),
                end_date=datetime.strptime(data["end_date"], "%Y-%m-%d").date(),
                reason=data.get("reason", ""),
            )
            db.session.add(vacation)
            db.session.commit()
            return vacation
        except Exception as e:
            db.session.rollback()
            raise Exception(str(e))

    @staticmethod
    def update_vacation(vacation_id, data):
        vacation = VacationRequest.query.get(vacation_id)
        if not vacation:
            return None

        try:
            if "start_date" in data:
                vacation.start_date = datetime.strptime(data["start_date"], "%Y-%m-%d").date()
            if "end_date" in data:
                vacation.end_date = datetime.strptime(data["end_date"], "%Y-%m-%d").date()
            if "reason" in data:
                vacation.reason = data.get("reason")
            if "status" in data:
                vacation.status = data.get("status")
            
            db.session.commit()
            return vacation
        except Exception as e:
            db.session.rollback()
            raise Exception(str(e))

    @staticmethod
    def approve_vacation(vacation_id):
        vacation = VacationRequest.query.get(vacation_id)
        if not vacation:
            return None
        
        vacation.status = 'approved'
        db.session.commit()
        return vacation

    @staticmethod
    def reject_vacation(vacation_id):
        vacation = VacationRequest.query.get(vacation_id)
        if not vacation:
            return None
        
        vacation.status = 'rejected'
        db.session.commit()
        return vacation

    @staticmethod
    def delete_vacation(vacation_id):
        vacation = VacationRequest.query.get(vacation_id)
        if not vacation:
            return None

        db.session.delete(vacation)
        db.session.commit()
        return vacation_id

