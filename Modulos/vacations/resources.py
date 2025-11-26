from flask_restx import Namespace, Resource, fields
from flask import request
from Modulos.vacations.service import VacationService
from Modulos.vacations.schemas import VacationSchema

vacations_ns = Namespace('vacations', description='Vacation operations')
vacation_model = vacations_ns.model('Vacation', {
    'employee_id': fields.Integer(required=True),
    'start_date': fields.Date(required=True),
    'end_date': fields.Date(required=True),
    'reason': fields.String,
    'status': fields.String(default='pending'),
})

@vacations_ns.route('/')
class VacationList(Resource):
    def get(self):
        try:
            reqs = VacationService.get_all_vacations()
            return {
                'message': 'Listado de vacaciones obtenido exitosamente',
                'data': reqs
            }, 200
        except Exception as e:
            return {
                'message': 'Error al obtener el listado de vacaciones',
                'error': str(e)
            }, 500

    @vacations_ns.expect(vacation_model)
    def post(self):
        try:
            data = request.get_json() or {}
            req = VacationService.create_vacation(data)
            schema = VacationSchema()
            return {
                'message': 'Solicitud de vacaciones creada exitosamente',
                'data': schema.dump(req)
            }, 201
        except Exception as e:
            return {
                'message': 'Error al crear la solicitud de vacaciones',
                'error': str(e)
            }, 400

@vacations_ns.route('/<int:id>')
class VacationDetail(Resource):
    def get(self, id):
        try:
            req = VacationService.get_vacation(id)
            if not req:
                return {
                    'message': 'Solicitud de vacaciones no encontrada',
                    'vacation_id': id
                }, 404
            return {
                'message': 'Solicitud de vacaciones obtenida exitosamente',
                'data': req
            }, 200
        except Exception as e:
            return {
                'message': 'Error al obtener la solicitud de vacaciones',
                'error': str(e)
            }, 500

    @vacations_ns.expect(vacation_model)
    def put(self, id):
        try:
            data = request.get_json() or {}
            req = VacationService.update_vacation(id, data)
            if not req:
                return {
                    'message': 'Solicitud de vacaciones no encontrada',
                    'vacation_id': id
                }, 404
            schema = VacationSchema()
            return {
                'message': 'Solicitud de vacaciones actualizada exitosamente',
                'data': schema.dump(req)
            }, 200
        except Exception as e:
            return {
                'message': 'Error al actualizar la solicitud de vacaciones',
                'error': str(e)
            }, 400

    def delete(self, id):
        try:
            deleted_id = VacationService.delete_vacation(id)
            if not deleted_id:
                return {
                    'message': 'Solicitud de vacaciones no encontrada',
                    'vacation_id': id
                }, 404
            return {
                'message': 'Solicitud de vacaciones eliminada exitosamente'
            }, 200
        except Exception as e:
            return {
                'message': 'Error al eliminar la solicitud de vacaciones',
                'error': str(e)
            }, 400

@vacations_ns.route('/<int:id>/approve')
class VacationApprove(Resource):
    def put(self, id):
        try:
            req = VacationService.approve_vacation(id)
            if not req:
                return {
                    'message': 'Solicitud de vacaciones no encontrada',
                    'vacation_id': id
                }, 404
            schema = VacationSchema()
            return {
                'message': 'Solicitud de vacaciones aprobada exitosamente',
                'data': schema.dump(req)
            }, 200
        except Exception as e:
            return {
                'message': 'Error al aprobar la solicitud de vacaciones',
                'error': str(e)
            }, 400

@vacations_ns.route('/<int:id>/reject')
class VacationReject(Resource):
    def put(self, id):
        try:
            req = VacationService.reject_vacation(id)
            if not req:
                return {
                    'message': 'Solicitud de vacaciones no encontrada',
                    'vacation_id': id
                }, 404
            schema = VacationSchema()
            return {
                'message': 'Solicitud de vacaciones rechazada exitosamente',
                'data': schema.dump(req)
            }, 200
        except Exception as e:
            return {
                'message': 'Error al rechazar la solicitud de vacaciones',
                'error': str(e)
            }, 400

@vacations_ns.route('/employee/<int:employee_id>')
class EmployeeVacations(Resource):
    def get(self, employee_id):
        try:
            reqs = VacationService.get_employee_vacations(employee_id)
            return {
                'message': 'Vacaciones del empleado obtenidas exitosamente',
                'employee_id': employee_id,
                'data': reqs
            }, 200
        except Exception as e:
            return {
                'message': 'Error al obtener las vacaciones del empleado',
                'error': str(e)
            }, 500

