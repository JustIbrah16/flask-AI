from flask_restx import Namespace, Resource, fields
from flask import request
from Modulos.attendance.service import AttendanceService
from Modulos.attendance.schemas import AttendanceSchema
from datetime import datetime


attendance_ns = Namespace('attendance', description='Attendance operations')


attendance_model = attendance_ns.model('Attendance', {
    'employee_id': fields.Integer(required=True),
    'check_in': fields.DateTime,
    'check_out': fields.DateTime,
    'attendance_date': fields.Date,
    'status': fields.String(description="present, absent, late, half-day"),
    'notes': fields.String,
})


@attendance_ns.route('/')
class AttendanceList(Resource):
    def get(self):
        items = AttendanceService.get_all()
        schema = AttendanceSchema(many=True)
        return schema.dump(items), 200

    @attendance_ns.expect(attendance_model)
    def post(self):
        """Crear registro manual de asistencia"""
        data = request.get_json() or {}
        item = AttendanceService.record(data)
        schema = AttendanceSchema()
        return schema.dump(item), 201


@attendance_ns.route('/<int:id>')
class AttendanceDetail(Resource):
    def get(self, id):
        from Modulos.attendance.repository import AttendanceRepository
        record = AttendanceRepository.get_by_id(id)
        if not record:
            return {'msg': 'not found'}, 404
        schema = AttendanceSchema()
        return schema.dump(record), 200


@attendance_ns.route('/employee/<int:employee_id>')
class EmployeeAttendance(Resource):
    def get(self, employee_id):
        """Obtener asistencia del empleado (con filtros opcionales)"""
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        
        if from_date:
            from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
        if to_date:
            to_date = datetime.strptime(to_date, "%Y-%m-%d").date()
        
        records = AttendanceService.get_by_employee(employee_id, from_date, to_date)
        return records, 200


@attendance_ns.route('/employee/<int:employee_id>/today')
class EmployeeAttendanceToday(Resource):
    def get(self, employee_id):
        """Obtener asistencia de hoy del empleado"""
        record = AttendanceService.get_today_attendance(employee_id)
        if not record:
            return {'msg': 'no record for today'}, 404
        return record, 200


@attendance_ns.route('/employee/<int:employee_id>/check-in')
class CheckIn(Resource):
    def post(self, employee_id):
        """Registrar entrada (check-in)"""
        try:
            record = AttendanceService.check_in(employee_id)
            if not record:
                return {'msg': 'already checked in today'}, 400
            schema = AttendanceSchema()
            return schema.dump(record), 201
        except Exception as e:
            return {'error': str(e)}, 400


@attendance_ns.route('/employee/<int:employee_id>/check-out')
class CheckOut(Resource):
    def post(self, employee_id):
        """Registrar salida (check-out) y calcular horas"""
        try:
            record = AttendanceService.check_out(employee_id)
            if not record:
                return {'msg': 'no check-in for today'}, 400
            schema = AttendanceSchema()
            return schema.dump(record), 200
        except Exception as e:
            return {'error': str(e)}, 400


@attendance_ns.route('/employee/<int:employee_id>/summary')
class AttendanceSummary(Resource):
    def get(self, employee_id):
        """Obtener resumen de asistencia y horas trabajadas"""
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        
        if not from_date or not to_date:
            return {'error': 'from_date and to_date are required'}, 400
        
        try:
            from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
            to_date = datetime.strptime(to_date, "%Y-%m-%d").date()
            
            summary = AttendanceService.get_employee_summary(employee_id, from_date, to_date)
            return summary, 200
        except ValueError:
            return {'error': 'invalid date format (use YYYY-MM-DD)'}, 400
