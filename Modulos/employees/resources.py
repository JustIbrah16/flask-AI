from flask_restx import Namespace, Resource
from flask import request

from Modulos.employees.service import EmployeeService


employees_ns = Namespace(
    "employees",
    description="Gestión de empleados"
)

# ============================================================
# LISTAR RESUMEN
# ============================================================
@employees_ns.route("/")
class EmployeeList(Resource):
    def get(self):
        """Listar empleados (vista resumida: nombre, identificación, jefe, proyecto)"""
        result = EmployeeService.get_all_brief()
        return {"message": "Listado de empleados", "data": result}, 200

    def post(self):
        """Crear un nuevo empleado"""
        json_data = request.get_json()
        new_emp = EmployeeService.create_employee(json_data)
        return {"message": "Empleado creado exitosamente", "data": new_emp}, 201


# ============================================================
# LISTAR TODOS DETALLADOS
# ============================================================
@employees_ns.route("/all")
class EmployeeListDetailed(Resource):
    def get(self):
        """Listar todos los empleados con información completa"""
        result = EmployeeService.get_all()
        return {"message": "Listado detallado de empleados", "data": result}, 200


# ============================================================
# BUSCAR POR ID
# ============================================================
@employees_ns.route("/<int:emp_id>")
class EmployeeById(Resource):
    def get(self, emp_id):
        """Obtener empleado por ID"""
        emp = EmployeeService.get_by_id(emp_id)
        if not emp:
            return {"message": "Empleado no encontrado"}, 404
        return {"message": "Empleado encontrado", "data": emp}, 200

    def put(self, emp_id):
        """Actualizar información de un empleado"""
        json_data = request.get_json()
        updated = EmployeeService.update_employee(emp_id, json_data)

        if not updated:
            return {"message": "Empleado no encontrado"}, 404

        return {"message": "Empleado actualizado", "data": updated}, 200

    def delete(self, emp_id):
        """Eliminar empleado (físico)"""
        deleted = EmployeeService.delete_employee(emp_id)
        if not deleted:
            return {"message": "Empleado no encontrado"}, 404

        return {"message": "Empleado eliminado correctamente"}, 200


# ============================================================
# BUSCAR POR IDENTIFICACIÓN
# ============================================================
@employees_ns.route("/identificacion/<int:identificacion>")
class EmployeeByIdentificacion(Resource):
    def get(self, identificacion):
        """Buscar empleado por número de identificación"""
        emp = EmployeeService.get_by_identificacion(identificacion)
        
        if not emp:
            return {"message": "Empleado no encontrado"}, 404

        return {"message": "Empleado encontrado", "data": emp}, 200


# ============================================================
# INACTIVAR EMPLEADO
# ============================================================
@employees_ns.route("/<int:emp_id>/deactivate")
class EmployeeDeactivate(Resource):
    def patch(self, emp_id):
        """Inactivar empleado (is_active = 0)"""
        emp = EmployeeService.deactivate_employee(emp_id)
        
        if not emp:
            return {"message": "Empleado no encontrado"}, 404

        return {"message": "Empleado desactivado", "data": emp}, 200
