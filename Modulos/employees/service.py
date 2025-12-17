from Modulos.employees.repository import EmployeeRepository
from Modulos.employees.entities import (
    EmployeeBriefEntity,
    EmployeeDetailEntity,
    EmployeeCreateEntity,
    EmployeeUpdateEntity
)


# ============================================================
# MAPPERS
# ============================================================
def map_detail(emp):
    return {
        "id": emp.id,
        "identificacion": emp.identificacion,
        "nombre": emp.nombre,
        "fecha_nacimiento": emp.fecha_nacimiento,
        "correo": emp.correo,
        "contacto": emp.contacto,
        "direccion": emp.direccion,
        "ciudad": emp.ciudad.name if emp.ciudad else None,
        "cargo": emp.cargo.name if emp.cargo else None,
        "area": emp.area.name if emp.area else None,
        "role": emp.role.name if emp.role else None,
        "jefe_inmediato": emp.jefe_inmediato,
        "tipo_contrato": emp.tipo_contrato.name if emp.tipo_contrato else None,
        "banco": emp.banco.name if emp.banco else None,
        "numero_cuenta_bancaria": emp.numero_cuenta_bancaria,
        "salario": emp.salario,
        "fecha_ingreso": emp.fecha_ingreso,
        "proyecto": emp.proyecto.name if emp.proyecto else None,
        "estado": "activo" if emp.is_active else "inactivo",
        "genero": emp.genero.name if emp.genero else None,
        "camisa": emp.camisa.name if emp.camisa else None,
        "pantalon": emp.pantalon,
        "zapatos": emp.zapatos,
        "abrigo": emp.abrigo.name if emp.abrigo else None,
        "eps": emp.eps.name if emp.eps else None,
        "arl": emp.arl.name if emp.arl else None,
        "estudios": emp.estudios,
        "estado_civil": emp.estado_civil.name if emp.estado_civil else None,
        "hijos": emp.hijos,
        "username": emp.username,
        "is_active": emp.is_active,
        "created_at": emp.created_at,
        "updated_at": emp.updated_at,
    }


def map_brief(emp):
    return {
        "nombre": emp.nombre,
        "identificacion": emp.identificacion,
        "jefe_inmediato": emp.jefe_inmediato,
        "proyecto": emp.proyecto.name if emp.proyecto else None
    }


# ============================================================
# SERVICE
# ============================================================
class EmployeeService:

    @staticmethod
    def list_brief():
        emps = EmployeeRepository.get_all()
        return EmployeeBriefEntity(many=True).dump(
            [map_brief(e) for e in emps]
        )

    @staticmethod
    def list_all():
        emps = EmployeeRepository.get_all()
        return EmployeeDetailEntity(many=True).dump(
            [map_detail(e) for e in emps]
        )

    @staticmethod
    def get_by_id(emp_id):
        emp = EmployeeRepository.get_by_id(emp_id)
        if not emp:
            return None
        return EmployeeDetailEntity().dump(map_detail(emp))

    @staticmethod
    def get_by_identificacion(identificacion):
        emp = EmployeeRepository.get_by_identificacion(identificacion)
        if not emp:
            return None
        return EmployeeDetailEntity().dump(map_detail(emp))

    @staticmethod
    def create(data):
        valid = EmployeeCreateEntity().load(data)
        password = valid.pop("password")

        emp = EmployeeRepository.create(valid)
        emp.set_password(password)

        EmployeeRepository.update(emp)
        return EmployeeDetailEntity().dump(map_detail(emp))

    @staticmethod
    def update(emp_id, data):
        emp = EmployeeRepository.get_by_id(emp_id)
        if not emp:
            return None

        # Validación parcial → solo valida los campos enviados
        valid = EmployeeUpdateEntity().load(data, partial=True)

        # Actualiza solo los campos que vienen
        for k, v in valid.items():
            setattr(emp, k, v)

        EmployeeRepository.update(emp)
        return EmployeeDetailEntity().dump(map_detail(emp))

    @staticmethod
    def deactivate(emp_id):
        emp = EmployeeRepository.get_by_id(emp_id)
        if not emp:
            return None

        emp = EmployeeRepository.soft_delete(emp)
        return EmployeeDetailEntity().dump(map_detail(emp))
