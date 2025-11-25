from extensions import db
from Modulos.reports.model import Report


class ReportRepository:
    @staticmethod
    def get_all():
        return Report.query.all()

    @staticmethod
    def get_by_id(report_id):
        return Report.query.get(report_id)

    @staticmethod
    def get_by_employee_id(employee_id):
        return Report.query.filter_by(employee_id=employee_id).all()

    @staticmethod
    def create(data):
        report = Report(**data)
        db.session.add(report)
        db.session.commit()
        return report

    @staticmethod
    def update(report):
        db.session.add(report)
        db.session.commit()
        return report

    @staticmethod
    def delete(report):
        db.session.delete(report)
        db.session.commit()
