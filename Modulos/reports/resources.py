from flask_restx import Namespace, Resource, fields
from flask import request
from Modulos.reports.service import ReportsService
from Modulos.reports.schemas import ReportSchema

reports_ns = Namespace('reports', description='Reporting')

report_model = reports_ns.model('Report', {
    'employee_id': fields.Integer(required=True),
    'title': fields.String(required=True),
    'description': fields.String,
    'report_type': fields.String,  # daily, weekly, monthly, incident
    'status': fields.String(default='pending'),
})

@reports_ns.route('/attendance-summary')
class AttendanceSummary(Resource):
    def get(self):
        q = ReportsService.attendance_summary()
        return q, 200

@reports_ns.route('/')
class ReportList(Resource):
    def get(self):
        reports = ReportsService.get_all_reports()
        return reports, 200

    @reports_ns.expect(report_model)
    def post(self):
        data = request.get_json() or {}
        report = ReportsService.create_report(data)
        schema = ReportSchema()
        return schema.dump(report), 201

@reports_ns.route('/<int:id>')
class ReportDetail(Resource):
    def get(self, id):
        report = ReportsService.get_report(id)
        if not report:
            return {'msg': 'not found'}, 404
        return report, 200

    @reports_ns.expect(report_model)
    def put(self, id):
        data = request.get_json() or {}
        report = ReportsService.update_report(id, data)
        if not report:
            return {'msg': 'not found'}, 404
        return report.to_dict(), 200

    def delete(self, id):
        deleted_id = ReportsService.delete_report(id)
        if not deleted_id:
            return {'msg': 'not found'}, 404
        return {}, 204

@reports_ns.route('/employee/<int:employee_id>')
class EmployeeReports(Resource):
    def get(self, employee_id):
        reports = ReportsService.get_employee_reports(employee_id)
        return reports, 200

