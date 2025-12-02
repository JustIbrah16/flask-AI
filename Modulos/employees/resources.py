from flask_restx import Namespace, Resource, fields
from flask import request
from Modulos.employees.service import EmployeeService
from Modulos.employees.schemas import EmployeeSchema

employees_ns = Namespace('employees', description='Employee operations')

employee_model = employees_ns.model('Employee', {
    'identificacion': fields.Integer(required=True, description='Identificación / número de empleado'),
    'nombre': fields.String(required=True, description='Nombre completo'),
    'fecha_nacimiento': fields.Date(description='Fecha de nacimiento'),
    'correo': fields.String(required=True, description='Correo electrónico'),
    'contacto': fields.Integer(description='Teléfono'),
    'direccion': fields.String(description='Dirección'),
    'ciudad_id': fields.Integer(description='ID de la ciudad'),
    'cargo_id': fields.Integer(description='ID del cargo'),
    'area_id': fields.Integer(description='ID del área de trabajo'),
    'role_id': fields.Integer(description='ID del rol'),
    'jefe_inmediato': fields.String(description='Nombre del jefe inmediato'),
    'tipo_contrato_id': fields.Integer(description='ID del tipo de contrato'),
    'banco_id': fields.Integer(description='ID del banco'),
    'numero_cuenta_bancaria': fields.Integer(description='Número de cuenta bancaria'),
    'salario': fields.Float(description='Salario'),
    'fecha_ingreso': fields.Date(description='Fecha de ingreso'),
    'proyecto_id': fields.Integer(description='ID del proyecto'),
    'genero_id': fields.Integer(description='ID del género'),
    'camisa_id': fields.Integer(description='ID talla de camisa'),
    'pantalon': fields.Integer(description='Talla de pantalón'),
    'zapatos': fields.Integer(description='Talla de zapatos'),
    'abrigo_id': fields.Integer(description='ID talla de abrigo'),
    'eps_id': fields.Integer(description='ID de EPS'),
    'arl_id': fields.Integer(description='ID de ARL'),
    'estudios': fields.String(description='Información de estudios'),
    'estado_civil_id': fields.Integer(description='ID del estado civil'),
    'hijos': fields.Integer(description='Número de hijos'),
    'username': fields.String(required=True, description='Usuario del sistema'),
    'password': fields.String(required=True, description='Contraseña'),
    'is_active': fields.Integer(description='Estado activo: 0=inactivo, 1=activo, 2=licencia'),
})

@employees_ns.route('/')
class EmployeeList(Resource):
    def get(self):
        """Listar todos los empleados (resumen):

        Devuelve solo `nombre`, `identificacion`, `jefe_inmediato`, `proyecto`,
        ordenados alfabéticamente por `nombre`.
        """
        try:
            emps = EmployeeService.list_employees_brief()
            return {
                'message': 'Listado de empleados obtenido exitosamente',
                'data': emps
            }, 200
        except Exception as e:
            return {
                'message': 'Error al obtener el listado de empleados',
                'error': str(e)
            }, 500

    @employees_ns.expect(employee_model)
    def post(self):
        """Crear nuevo empleado"""
        data = request.get_json() or {}
        
        # Validar campos requeridos
        required_fields = ['identificacion', 'nombre', 'correo', 'username', 'password']
        missing = [f for f in required_fields if not data.get(f)]
        
        if missing:
            return {
                'message': 'Campos requeridos faltantes',
                'missing_fields': missing
            }, 400
        
        try:
            emp = EmployeeService.create_employee(data)
            schema = EmployeeSchema()
            return {
                'message': 'Empleado creado exitosamente',
                'data': schema.dump(emp)
            }, 201
        except Exception as e:
            return {
                'message': 'Error al crear el empleado',
                'error': str(e)
            }, 400

@employees_ns.route('/<int:id>')
class EmployeeDetail(Resource):
    def get(self, id):
        """Obtener detalles de un empleado"""
        try:
            emp = EmployeeService.get_employee(id)
            if not emp:
                return {
                    'message': 'Empleado no encontrado',
                    'employee_id': id
                }, 404
            schema = EmployeeSchema()
            return {
                'message': 'Empleado obtenido exitosamente',
                'data': schema.dump(emp)
            }, 200
        except Exception as e:
            return {
                'message': 'Error al obtener el empleado',
                'error': str(e)
            }, 500

    @employees_ns.expect(employee_model)
    def put(self, id):
        """Editar empleado"""
        try:
            emp = EmployeeService.get_employee(id)
            if not emp:
                return {
                    'message': 'Empleado no encontrado',
                    'employee_id': id
                }, 404
            data = request.get_json() or {}
            updated_emp = EmployeeService.update_employee(id, data)
            schema = EmployeeSchema()
            return {
                'message': 'Empleado actualizado exitosamente',
                'data': schema.dump(updated_emp)
            }, 200
        except Exception as e:
            return {
                'message': 'Error al actualizar el empleado',
                'error': str(e)
            }, 400

    def delete(self, id):
        """Inactivar empleado"""
        try:
            emp = EmployeeService.get_employee(id)
            if not emp:
                return {
                    'message': 'Empleado no encontrado',
                    'employee_id': id
                }, 404
            updated_emp = EmployeeService.delete_employee(id)
            schema = EmployeeSchema()
            return {
                'message': 'Empleado inactivado exitosamente',
                'data': schema.dump(updated_emp)
            }, 200
        except Exception as e:
            return {
                'message': 'Error al inactivar el empleado',
                'error': str(e)
            }, 400

@employees_ns.route('/<int:id>/toggle-status')
class EmployeeToggleStatus(Resource):
    def put(self, id):
        """Activar/inactivar empleado"""
        try:
            emp = EmployeeService.get_employee(id)
            if not emp:
                return {
                    'message': 'Empleado no encontrado',
                    'employee_id': id
                }, 404
            updated_emp = EmployeeService.toggle_employee_status(id)
            schema = EmployeeSchema()
            return {
                'message': 'Estado del empleado actualizado exitosamente',
                'data': schema.dump(updated_emp)
            }, 200
        except Exception as e:
            return {
                'message': 'Error al cambiar el estado del empleado',
                'error': str(e)
            }, 400

@employees_ns.route('/identificacion/<identificacion>')
class EmployeeByIdentificacion(Resource):
    def get(self, identificacion):
        """Obtener empleado por identificación"""
        try:
            from Modulos.employees.repository import EmployeeRepository
            emp = EmployeeRepository.get_by_identificacion(identificacion)
            if not emp:
                return {
                    'message': 'Empleado no encontrado',
                    'identificacion': identificacion
                }, 404
            schema = EmployeeSchema()
            return {
                'message': 'Empleado obtenido exitosamente',
                'data': schema.dump(emp)
            }, 200
        except Exception as e:
            return {
                'message': 'Error al obtener el empleado por identificación',
                'error': str(e)
            }, 400

