from flask_restx import Namespace, Resource, fields
from flask import request
from marshmallow import ValidationError

from Modulos.employees.service import EmployeeService

employees_ns = Namespace("employees", description="Gestión de empleados")

# =======================
# Swagger Models
# =======================
password_model = employees_ns.model('UpdatePassword', {
    'password': fields.String(required=True, description='La nueva contraseña del empleado')
})

state_employe_model = employees_ns.model('UpdateStateEmploye', {
    'state_employe_id': fields.Integer(required=True, description='El ID del estado del empleado')
})
employee_create_model = employees_ns.model("EmployeeCreate", {
    "name": fields.String(required=True),
    "identification": fields.Integer(required=True),
    "email": fields.String(required=True),

    "username": fields.String(required=True),

    "phone": fields.Integer,
    "address": fields.String,

    "city_id": fields.Integer,
    "position_id": fields.Integer,
    "area_id": fields.Integer,
    "role_id": fields.Integer,
    "project_id": fields.Integer,

    "is_boss": fields.Integer,
    "boss_id": fields.Integer,
    "salary": fields.Float,

    "bank_id": fields.Integer,
    "account_number": fields.Integer,

    "gender_id": fields.Integer,
    "shirt_size_id": fields.Integer,
    "coat_size_id": fields.Integer,
    "shoes_size": fields.Integer,
    "studies": fields.String,
    "pants_size": fields.Integer,
    "entry_date": fields.Date,
    "date_of_birth": fields.Date,

    "eps_id": fields.Integer,
    "arl_id": fields.Integer,

    "marital_status_id": fields.Integer,
    "children": fields.Integer,

    "contract_type_id": fields.Integer
})

employee_update_model = employees_ns.model("EmployeeUpdate", {
    "name": fields.String,
    "email": fields.String,
    "phone": fields.Integer,
    "address": fields.String,
    "salary": fields.Float,
    "boss_id": fields.Integer,
    "project_id": fields.Integer
})

# =======================
# Routes
# =======================

@employees_ns.route("/")
class Employees(Resource):
    @employees_ns.param(
        "boss_id", "ID del jefe inmediato", type=int, required=False
    )
    @employees_ns.param(
        "project_id", "ID del proyecto", type=int, required=False
    )
    @employees_ns.param(
        "gender_id", "ID del género", type=int, required=False
    )
    @employees_ns.param(
        "is_active", "Estado (1=activo, 0=inactivo)", type=int, required=False
    )

    def get(self):
        return {
            "message": "Listado de empleados resumido",
            "data": EmployeeService.list_brief(request.args)
        }, 200

    @employees_ns.expect(employee_create_model, validate=True)
    def post(self):
        data = request.get_json()
        emp = EmployeeService.create(data)
        return {
            "message": "Empleado creado",
            "data": emp
        }, 201

@employees_ns.route("/update-password/<int:emp_id>")
class EmployeeUpdatePassword(Resource):
    @employees_ns.expect(password_model)
    def put(self, emp_id):
        data = request.get_json()
        password = data.get("password")
        
        if not password:
            return {"message": "Contraseña no proporcionada"}, 400

        result = EmployeeService.update_password(emp_id, password)
        if not isinstance(result, dict):
            return {"message": "Error inesperado al actualizar contraseña"}, 500

        if not result.get("success"):
            return {"message": result.get("message", "No se pudo actualizar la contraseña")}, result.get("status", 400)

        return {"message": result.get("message", "Contraseña actualizada correctamente")}, 200


@employees_ns.route("/update-state/<int:emp_id>")
class EmployeeUpdateState(Resource):
    @employees_ns.expect(state_employe_model)
    def put(self, emp_id):
        """Actualiza el estado del empleado (activo, inactivo, licencia, etc.)"""
        data = request.get_json()
        state_employe_id = data.get("state_employe_id")
        
        if not state_employe_id:
            return {"message": "El ID del estado no fue proporcionado"}, 400

        result = EmployeeService.update_state(emp_id, state_employe_id)
        if not result.get("success"):
            return {"message": result.get("message", "No se pudo actualizar el estado")}, result.get("status", 400)

        return {"message": result.get("message", "Estado actualizado correctamente")}, 200


@employees_ns.route("/count")
class EmployeeCount(Resource):
    def get(self):
        """Obtiene el número total de empleados registrados"""
        total = EmployeeService.get_total_employees()
        return {"total": total}, 200
        


@employees_ns.route("/all")
class EmployeesAll(Resource):

    def get(self):
        return {
            "message": "Listado completo",
            "data": EmployeeService.list_all()
        }, 200


@employees_ns.route("/<int:emp_id>")
class EmployeeById(Resource):

    def get(self, emp_id):
        emp = EmployeeService.get_by_id(emp_id)
        if not emp:
            return {"message": "Empleado no encontrado"}, 404
        return {"data": emp}, 200

    @employees_ns.expect(employee_create_model, validate=True)
    def put(self, emp_id):
        data = request.get_json()

        try:
            emp = EmployeeService.update(emp_id, data)
        except ValidationError as e:
            return {"message": "Error de validación", "errors": e.messages}, 400

        if not emp:
            return {"message": "Empleado no encontrado"}, 404

        return {
            "message": "Empleado actualizado",
            "data": emp
        }, 200

    def delete(self, emp_id):
        emp = EmployeeService.deactivate(emp_id)
        if not emp:
            return {"message": "Empleado no encontrado"}, 404
        return {
            "message": "Empleado inactivado",
            "data": emp
        }, 200


@employees_ns.route("/identification/<int:identification>")
class EmployeeByIdentification(Resource):

    def get(self, identification):
        emp = EmployeeService.get_by_identification(identification)
        if not emp:
            return {"message": "Empleado no encontrado"}, 404
        return {"data": emp}, 200


@employees_ns.route("/delegar-jefe/list")
class EmployeesWithDelegarJefe(Resource):
    def get(self):
        """Obtiene todos los empleados autorizados para delegar jefe (delegar_jefe = 1)"""
        emps = EmployeeService.get_employees_with_delegar_jefe()
        return {
            "data": emps
        }, 200
