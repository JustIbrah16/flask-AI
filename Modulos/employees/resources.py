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
employee_create_model = employees_ns.model("EmployeeCreate", {
    "nombre": fields.String(required=True),
    "identificacion": fields.Integer(required=True),
    "correo": fields.String(required=True),

    "username": fields.String(required=True),

    "contacto": fields.Integer,
    "direccion": fields.String,

    "ciudad_id": fields.Integer,
    "cargo_id": fields.Integer,
    "area_id": fields.Integer,
    "role_id": fields.Integer,
    "proyecto_id": fields.Integer,

    "delegar_jefe": fields.Integer,
    "jefe_inmediato": fields.Integer,
    "salario": fields.Float,

    "banco_id": fields.Integer,
    "numero_cuenta_bancaria": fields.Integer,

    "genero_id": fields.Integer,
    "camisa_id": fields.Integer,
    "abrigo_id": fields.Integer,
    "zapatos": fields.Integer,
    "estudios": fields.String,
    "pantalon": fields.Integer,
    "fecha_ingreso": fields.Date,
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
    "jefe_inmediato": fields.Integer,
    "proyecto_id": fields.Integer
})

# =======================
# Routes
# =======================

@employees_ns.route("/")
class Employees(Resource):
    @employees_ns.param(
        "jefe_id", "ID del jefe inmediato", type=int, required=False
    )
    @employees_ns.param(
        "proyecto_id", "ID del proyecto", type=int, required=False
    )
    @employees_ns.param(
        "genero_id", "ID del género", type=int, required=False
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

        success = EmployeeService.update_password(emp_id, password)
        if not success:
            return {"message": "Empleado no encontrado"}, 404

        return {"message": "Contraseña actualizada correctamente"}, 200




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


@employees_ns.route("/delegar-jefe/list")
class EmployeesWithDelegarJefe(Resource):
    def get(self):
        """Obtiene todos los empleados autorizados para delegar jefe (delegar_jefe = 1)"""
        emps = EmployeeService.get_employees_with_delegar_jefe()
        return {
          
            "data": emps
        }, 200
