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
        try:
            items = AttendanceService.get_all()
            schema = AttendanceSchema(many=True)
            return {
                'message': 'Listado de asistencia obtenido exitosamente',
                'data': schema.dump(items)
            }, 200
        except Exception as e:
            return {
                'message': 'Error al obtener el listado de asistencia',
                'error': str(e)
            }, 500

    @attendance_ns.expect(attendance_model)
    def post(self):
        """Crear registro manual de asistencia"""
        try:
            data = request.get_json() or {}
            item = AttendanceService.record(data)
            schema = AttendanceSchema()
            return {
                'message': 'Registro de asistencia creado exitosamente',
                'data': schema.dump(item)
            }, 201
        except Exception as e:
            return {
                'message': 'Error al crear el registro de asistencia',
                'error': str(e)
            }, 400


@attendance_ns.route('/<int:id>')
class AttendanceDetail(Resource):
    def get(self, id):
        try:
            from Modulos.attendance.repository import AttendanceRepository
            record = AttendanceRepository.get_by_id(id)
            if not record:
                return {
                    'message': 'Registro de asistencia no encontrado',
                    'attendance_id': id
                }, 404
            schema = AttendanceSchema()
            return {
                'message': 'Registro de asistencia obtenido exitosamente',
                'data': schema.dump(record)
            }, 200
        except Exception as e:
            return {
                'message': 'Error al obtener el registro de asistencia',
                'error': str(e)
            }, 500


@attendance_ns.route('/employee/<int:employee_id>')
class EmployeeAttendance(Resource):
    def get(self, employee_id):
        """Obtener asistencia del empleado (con filtros opcionales)"""
        try:
            from_date = request.args.get('from_date')
            to_date = request.args.get('to_date')
            
            if from_date:
                from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
            if to_date:
                to_date = datetime.strptime(to_date, "%Y-%m-%d").date()
            
            records = AttendanceService.get_by_employee(employee_id, from_date, to_date)
            return {
                'message': 'Asistencia del empleado obtenida exitosamente',
                'employee_id': employee_id,
                'data': records
            }, 200
        except Exception as e:
            return {
                'message': 'Error al obtener la asistencia del empleado',
                'error': str(e)
            }, 500


@attendance_ns.route('/employee/<int:employee_id>/today')
class EmployeeAttendanceToday(Resource):
    def get(self, employee_id):
        """Obtener asistencia de hoy del empleado"""
        try:
            record = AttendanceService.get_today_attendance(employee_id)
            if not record:
                return {
                    'message': 'Sin registro de asistencia para hoy',
                    'employee_id': employee_id
                }, 404
            return {
                'message': 'Asistencia de hoy obtenida exitosamente',
                'data': record
            }, 200
        except Exception as e:
            return {
                'message': 'Error al obtener la asistencia de hoy',
                'error': str(e)
            }, 500


@attendance_ns.route('/employee/<int:employee_id>/check-in')
class CheckIn(Resource):
    def post(self, employee_id):
        """Registrar entrada (check-in)"""
        try:
            record = AttendanceService.check_in(employee_id)
            if not record:
                return {
                    'message': 'El empleado ya ha registrado entrada hoy',
                    'employee_id': employee_id
                }, 400
            schema = AttendanceSchema()
            return {
                'message': 'Entrada registrada exitosamente',
                'data': schema.dump(record)
            }, 201
        except Exception as e:
            return {
                'message': 'Error al registrar la entrada',
                'error': str(e)
            }, 400


@attendance_ns.route('/employee/<int:employee_id>/check-out')
class CheckOut(Resource):
    def post(self, employee_id):
        """Registrar salida (check-out) y calcular horas"""
        try:
            record = AttendanceService.check_out(employee_id)
            if not record:
                return {
                    'message': 'Sin registro de entrada para hoy',
                    'employee_id': employee_id
                }, 400
            schema = AttendanceSchema()
            return {
                'message': 'Salida registrada exitosamente',
                'data': schema.dump(record)
            }, 200
        except Exception as e:
            return {
                'message': 'Error al registrar la salida',
                'error': str(e)
            }, 400


@attendance_ns.route('/employee/<int:employee_id>/summary')
class AttendanceSummary(Resource):
    def get(self, employee_id):
        """Obtener resumen de asistencia y horas trabajadas"""
        try:
            from_date = request.args.get('from_date')
            to_date = request.args.get('to_date')
            
            if not from_date or not to_date:
                return {
                    'message': 'Parámetros requeridos faltantes',
                    'required_params': ['from_date', 'to_date'],
                    'format': 'YYYY-MM-DD'
                }, 400
            
            from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
            to_date = datetime.strptime(to_date, "%Y-%m-%d").date()
            
            summary = AttendanceService.get_employee_summary(employee_id, from_date, to_date)
            return {
                'message': 'Resumen de asistencia obtenido exitosamente',
                'employee_id': employee_id,
                'period': {
                    'from': str(from_date),
                    'to': str(to_date)
                },
                'data': summary
            }, 200
        except ValueError:
            return {
                'message': 'Formato de fecha inválido',
                'format': 'Use YYYY-MM-DD'
            }, 400
        except Exception as e:
            return {
                'message': 'Error al obtener el resumen de asistencia',
                'error': str(e)
            }, 500
