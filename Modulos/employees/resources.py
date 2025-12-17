from flask_restx import Namespace, Resource, fields
from flask import request
from marshmallow import ValidationError

from Modulos.employees.service import EmployeeService

employees_ns = Namespace("employees", description="Gestión de empleados")

# =======================
# Swagger Models
# =======================

employee_create_model = employees_ns.model("EmployeeCreate", {
    "nombre": fields.String(required=True),
    "identificacion": fields.Integer(required=True),
    "correo": fields.String(required=True),

    "username": fields.String(required=True),
    "password": fields.String(required=True),

    "contacto": fields.Integer,
    "direccion": fields.String,

    "ciudad_id": fields.Integer,
    "cargo_id": fields.Integer,
    "area_id": fields.Integer,
    "role_id": fields.Integer,
    "proyecto_id": fields.Integer,

    "jefe_inmediato": fields.String,
    "salario": fields.Float,

    "banco_id": fields.Integer,
    "numero_cuenta_bancaria": fields.Integer,

    "genero_id": fields.Integer,
    "camisa_id": fields.Integer,
    "abrigo_id": fields.Integer,
    "zapatos_id": fields.Integer,
    "estudios_id": fields.Integer,
    "pantalon_id": fields.Integer,
    "fecha_de_ingreso": fields.Date,
    "fecha_nacimiento": fields.Date,

    "eps_id": fields.Integer,
    "arl_id": fields.Integer,

    "estado_civil_id": fields.Integer,
    "hijos": fields.Integer,

    "tipo_contrato_id": fields.Integer
})

employee_update_model = employees_ns.model("EmployeeUpdate", {
    "nombre": fields.String,
    "correo": fields.String,
    "contacto": fields.Integer,
    "direccion": fields.String,
    "salario": fields.Float,
    "jefe_inmediato": fields.String,
    "proyecto_id": fields.Integer
})

# =======================
# Routes
# =======================

@employees_ns.route("/")
class Employees(Resource):

    def get(self):
        return {
            "message": "Listado resumido",
            "data": EmployeeService.list_brief()
        }, 200

    @employees_ns.expect(employee_create_model, validate=True)
    def post(self):
        data = request.get_json()
        emp = EmployeeService.create(data)
        return {
            "message": "Empleado creado",
            "data": emp
        }, 201


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

    @employees_ns.expect(employee_update_model, validate=True)
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


@employees_ns.route("/identificacion/<int:identificacion>")
class EmployeeByIdentificacion(Resource):

    def get(self, identificacion):
        emp = EmployeeService.get_by_identificacion(identificacion)
        if not emp:
            return {"message": "Empleado no encontrado"}, 404
        return {"data": emp}, 200
