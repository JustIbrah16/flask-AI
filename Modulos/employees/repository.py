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
    def get_by_username(username):
        return Employee.query.filter_by(username=username).first()

    @staticmethod
    def get_by_identificacion(identificacion):
        return Employee.query.filter_by(identificacion=identificacion).first()

    @staticmethod
    def get_all_ordered_by_name():
        return Employee.query.order_by(Employee.nombre.asc()).all()

    @staticmethod
    def get_by_correo(correo):
        return Employee.query.filter_by(correo=correo).first()

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
    def delete(emp):
        db.session.delete(emp)
        db.session.commit()
