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
        try:
            q = ReportsService.attendance_summary()
            return {
                'message': 'Resumen de asistencia obtenido exitosamente',
                'data': q
            }, 200
        except Exception as e:
            return {
                'message': 'Error al obtener el resumen de asistencia',
                'error': str(e)
            }, 500

@reports_ns.route('/')
class ReportList(Resource):
    def get(self):
        try:
            reports = ReportsService.get_all_reports()
            return {
                'message': 'Listado de reportes obtenido exitosamente',
                'data': reports
            }, 200
        except Exception as e:
            return {
                'message': 'Error al obtener el listado de reportes',
                'error': str(e)
            }, 500

    @reports_ns.expect(report_model)
    def post(self):
        try:
            data = request.get_json() or {}
            report = ReportsService.create_report(data)
            schema = ReportSchema()
            return {
                'message': 'Reporte creado exitosamente',
                'data': schema.dump(report)
            }, 201
        except Exception as e:
            return {
                'message': 'Error al crear el reporte',
                'error': str(e)
            }, 400

@reports_ns.route('/<int:id>')
class ReportDetail(Resource):
    def get(self, id):
        try:
            report = ReportsService.get_report(id)
            if not report:
                return {
                    'message': 'Reporte no encontrado',
                    'report_id': id
                }, 404
            return {
                'message': 'Reporte obtenido exitosamente',
                'data': report
            }, 200
        except Exception as e:
            return {
                'message': 'Error al obtener el reporte',
                'error': str(e)
            }, 500

    @reports_ns.expect(report_model)
    def put(self, id):
        try:
            data = request.get_json() or {}
            report = ReportsService.update_report(id, data)
            if not report:
                return {
                    'message': 'Reporte no encontrado',
                    'report_id': id
                }, 404
            return {
                'message': 'Reporte actualizado exitosamente',
                'data': report.to_dict()
            }, 200
        except Exception as e:
            return {
                'message': 'Error al actualizar el reporte',
                'error': str(e)
            }, 400

    def delete(self, id):
        try:
            deleted_id = ReportsService.delete_report(id)
            if not deleted_id:
                return {
                    'message': 'Reporte no encontrado',
                    'report_id': id
                }, 404
            return {
                'message': 'Reporte eliminado exitosamente'
            }, 200
        except Exception as e:
            return {
                'message': 'Error al eliminar el reporte',
                'error': str(e)
            }, 400

@reports_ns.route('/employee/<int:employee_id>')
class EmployeeReports(Resource):
    def get(self, employee_id):
        try:
            reports = ReportsService.get_employee_reports(employee_id)
            return {
                'message': 'Reportes del empleado obtenidos exitosamente',
                'employee_id': employee_id,
                'data': reports
            }, 200
        except Exception as e:
            return {
                'message': 'Error al obtener los reportes del empleado',
                'error': str(e)
            }, 500

