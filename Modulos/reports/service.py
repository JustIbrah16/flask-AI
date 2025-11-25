from extensions import db
from Modulos.attendance.model import Attendance
from Modulos.reports.repository import ReportRepository
from Modulos.reports.model import Report
from sqlalchemy import func

class ReportsService:
    @staticmethod
    def attendance_summary():
        # Example of a raw query with SQLAlchemy
        summary = db.session.query(
            Attendance.employee_id,
            func.count(Attendance.id).label('total_records')
        ).group_by(Attendance.employee_id).all()
        
        # Convert result to a list of dicts
        return [
            {'employee_id': row.employee_id, 'total_records': row.total_records}
            for row in summary
        ]

    @staticmethod
    def get_all_reports():
        reports = ReportRepository.get_all()
        return [r.to_dict() for r in reports]

    @staticmethod
    def get_report(report_id):
        report = ReportRepository.get_by_id(report_id)
        if not report:
            return None
        return report.to_dict()

    @staticmethod
    def get_employee_reports(employee_id):
        reports = ReportRepository.get_by_employee_id(employee_id)
        return [r.to_dict() for r in reports]

    @staticmethod
    def create_report(data):
        return ReportRepository.create(data)

    @staticmethod
    def update_report(report_id, data):
        report = ReportRepository.get_by_id(report_id)
        if not report:
            return None
        
        for key, value in data.items():
            if hasattr(report, key):
                setattr(report, key, value)
        
        return ReportRepository.update(report)

    @staticmethod
    def delete_report(report_id):
        report = ReportRepository.get_by_id(report_id)
        if not report:
            return None
        ReportRepository.delete(report)
        return report_id
