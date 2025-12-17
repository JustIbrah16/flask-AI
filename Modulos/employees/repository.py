from extensions import db
from Modulos.employees.models import Employee


class EmployeeRepository:

    @staticmethod
    def get_all():
        return Employee.query.all()

    @staticmethod
    def get_by_id(emp_id):
        return Employee.query.get(emp_id)

    @staticmethod
    def get_by_identificacion(identificacion):
        return Employee.query.filter_by(identificacion=identificacion).first()

    @staticmethod
    def create(data):
        emp = Employee(**data)
        db.session.add(emp)
        db.session.commit()
        return emp

    @staticmethod
    def update(emp):
        db.session.add(emp)
        db.session.commit()
        return emp

    @staticmethod
    def soft_delete(emp):
        emp.is_active = 0
        db.session.add(emp)
        db.session.commit()
        return emp

    @staticmethod
    def get_employee_by_username(username: str):
        """Retorna un empleado por su username"""
        return Employee.query.filter_by(username=username).first()

    @staticmethod
    def get_employee_by_email(email: str):
        """Retorna un empleado por su email"""
        return Employee.query.filter_by(email=email).first()