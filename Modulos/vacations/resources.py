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
        reqs = VacationService.get_all_vacations()
        return reqs, 200

    @vacations_ns.expect(vacation_model)
    def post(self):
        try:
            data = request.get_json() or {}
            req = VacationService.create_vacation(data)
            schema = VacationSchema()
            return schema.dump(req), 201
        except Exception as e:
            return {'error': str(e)}, 400

@vacations_ns.route('/<int:id>')
class VacationDetail(Resource):
    def get(self, id):
        req = VacationService.get_vacation(id)
        if not req:
            return {'msg': 'not found'}, 404
        return req, 200

    @vacations_ns.expect(vacation_model)
    def put(self, id):
        try:
            data = request.get_json() or {}
            req = VacationService.update_vacation(id, data)
            if not req:
                return {'msg': 'not found'}, 404
            schema = VacationSchema()
            return schema.dump(req), 200
        except Exception as e:
            return {'error': str(e)}, 400

    def delete(self, id):
        deleted_id = VacationService.delete_vacation(id)
        if not deleted_id:
            return {'msg': 'not found'}, 404
        return {}, 204

@vacations_ns.route('/<int:id>/approve')
class VacationApprove(Resource):
    def put(self, id):
        req = VacationService.approve_vacation(id)
        if not req:
            return {'msg': 'not found'}, 404
        schema = VacationSchema()
        return schema.dump(req), 200

@vacations_ns.route('/<int:id>/reject')
class VacationReject(Resource):
    def put(self, id):
        req = VacationService.reject_vacation(id)
        if not req:
            return {'msg': 'not found'}, 404
        schema = VacationSchema()
        return schema.dump(req), 200

@vacations_ns.route('/employee/<int:employee_id>')
class EmployeeVacations(Resource):
    def get(self, employee_id):
        reqs = VacationService.get_employee_vacations(employee_id)
        return reqs, 200

