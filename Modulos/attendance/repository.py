from extensions import db
from Modulos.attendance.model import Attendance
from datetime import datetime, date

class AttendanceRepository:
    @staticmethod
    def get_all():
        return Attendance.query.all()

    @staticmethod
    def get_by_employee_id(employee_id):
        return Attendance.query.filter_by(employee_id=employee_id).all()

    @staticmethod
    def get_by_employee(employee_id, from_date=None, to_date=None):
        query = Attendance.query.filter_by(employee_id=employee_id)
        
        if from_date:
            query = query.filter(Attendance.attendance_date >= from_date)
        if to_date:
            query = query.filter(Attendance.attendance_date <= to_date)
        
        return query.all()

    @staticmethod
    def get_by_date(employee_id, attendance_date):
        return Attendance.query.filter_by(
            employee_id=employee_id,
            attendance_date=attendance_date
        ).first()

    @staticmethod
    def get_by_id(attendance_id):
        return Attendance.query.get(attendance_id)

    @staticmethod
    def create(data):
        att = Attendance(**data)
        db.session.add(att)
        db.session.commit()
        return att

    @staticmethod
    def update(attendance):
        db.session.add(attendance)
        db.session.commit()
        return attendance

    @staticmethod
    def delete(attendance):
        db.session.delete(attendance)
        db.session.commit()
