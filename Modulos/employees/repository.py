from extensions import db
from sqlalchemy import text
from Modulos.employees.models import Employee


class EmployeeRepository:

    @staticmethod
    def get_all():
        return Employee.query.all()
    
    @staticmethod
    def get_filtered(filters: dict):
        query = Employee.query

      
        if "boss_id" in filters:
            query = query.filter(
                Employee.boss_id == filters["boss_id"]
            )


        if "project_id" in filters:
            query = query.filter(
                Employee.project_id == filters["project_id"]
            )

   
        if "gender_id" in filters:
            query = query.filter(
                Employee.gender_id == filters["gender_id"]
            )

    
        if "is_active" in filters:
            query = query.filter(
                Employee.is_active == filters["is_active"]
            )

        return query.all()
    

    @staticmethod
    def get_by_id(emp_id):
        return Employee.query.get(emp_id)

    @staticmethod
    def get_by_identification(identification):
        return Employee.query.filter_by(identification=identification).first()

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
        return Employee.query.filter_by(email=email).first()

    @staticmethod
    def get_employees_with_delegar_jefe():
        """Retorna todos los empleados que tengan delegar_jefe = 1"""
        return Employee.query.filter_by(is_boss=1).all()

    @staticmethod
    def get_count():
        return db.session.query(Employee).count()