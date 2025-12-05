from extensions import db
from Modulos.employees.models import Employee

class EmployeeRepository:
    """Repositorio para operaciones CRUD sobre empleados"""

    @staticmethod
    def get_all_employees():
        """Retorna todos los empleados"""
        return Employee.query.all()

    @staticmethod
    def get_employee_by_id(emp_id: int):
        """Retorna un empleado por su ID"""
        return Employee.query.get(emp_id)

    @staticmethod
    def get_employee_by_username(username: str):
        """Retorna un empleado por su username"""
        return Employee.query.filter_by(username=username).first()

    @staticmethod
    def get_employee_by_identificacion(identificacion: int):
        """Retorna un empleado por su número de identificación"""
        return Employee.query.filter_by(identificacion=identificacion).first()

    @staticmethod
    def get_all_employees_ordered_by_name():
        """Retorna todos los empleados ordenados alfabéticamente por nombre"""
        return Employee.query.order_by(Employee.nombre.asc()).all()

    @staticmethod
    def get_employee_by_email(correo: str):
        """Retorna un empleado por su correo"""
        return Employee.query.filter_by(correo=correo).first()

    @staticmethod
    def create_employee(data: dict):
        """Crea un nuevo empleado"""
        emp = Employee(**data)
        db.session.add(emp)
        db.session.commit()
        return emp

    @staticmethod
    def update_employee(emp: Employee):
        """Actualiza un empleado existente"""
        db.session.add(emp)
        db.session.commit()
        return emp

    @staticmethod
    def delete_employee(emp: Employee):
        """Elimina un empleado (uso interno, por defecto solo inactiva)"""
        db.session.delete(emp)
        db.session.commit()
