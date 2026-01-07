from Modulos.employees.repository import EmployeeRepository
from Modulos.employees.models import Employee
from Modulos.employees.entities import  EmployeeBriefEntity, EmployeeDetailEntity, EmployeeCreateEntity, EmployeeUpdateEntity
import random
import string
import re
from email_service import EmailService
from flask import current_app



# ============================================================
# MAPPERS
# ============================================================
def map_detail(emp):
    return {
        "id": emp.id,
        "identification": emp.identification,
        "name": emp.name,
        "date_of_birth": emp.date_of_birth,
        "email": emp.email,
        "phone": emp.phone,
        "address": emp.address,
        "city": emp.city.name if emp.city else None,
        "position": emp.position.name if emp.position else None,
        "area": emp.area.name if emp.area else None,
        "role": emp.role.name if emp.role else None,
        "is_boss": emp.is_boss,
        "boss_id": emp.boss_id,
        "contract_type": emp.contract_type.name if emp.contract_type else None,
        "bank": emp.bank.name if emp.bank else None,
        "account_number": emp.account_number,
        "salary": emp.salary,
        "entry_date": emp.entry_date,
        "project": emp.project.name if emp.project else None,
        "state": "activo" if emp.is_active else "inactivo",
        "gender": emp.gender.name if emp.gender else None,
        "shirt_size": emp.shirt_size.name if emp.shirt_size else None,
        "pants_size": emp.pants_size,
        "shoes_size": emp.shoes_size,
        "coat_size": emp.coat_size.name if emp.coat_size else None,
        "eps": emp.eps.name if emp.eps else None,
        "arl": emp.arl.name if emp.arl else None,
        "studies": emp.studies,
        "marital_status": emp.marital_status.name if emp.marital_status else None,
        "children": emp.children,
        "username": emp.username,
        "is_active": emp.is_active,
        "created_at": emp.created_at,
        "updated_at": emp.updated_at,

    }
def map_create(emp):
    return {
        "identification": emp.identification,
        "name": emp.name,
        "date_of_birth": emp.date_of_birth,
        "email": emp.email,
        "phone": emp.phone,
        "address": emp.address,
        "city_id": emp.city_id,
        "position_id": emp.position_id,
        "area_id": emp.area_id,
        "role_id": emp.role_id,
        "is_boss": emp.is_boss,
        "boss_id": emp.boss_id,
        "contract_type_id": emp.contract_type_id,
        "bank_id": emp.bank_id,
        "account_number": emp.account_number,
        "salary": emp.salary,
        "entry_date": emp.entry_date,
        "project_id": emp.project_id,
        "gender_id": emp.gender_id,
        "shirt_size_id": emp.shirt_size_id,
        "pants_size": emp.pants_size,
        "shoes_size": emp.shoes_size,
        "coat_size_id": emp.coat_size_id,
        "eps_id": emp.eps_id,
        "arl_id": emp.arl_id,
        "studies": emp.studies,
        "marital_status_id": emp.marital_status_id,
        "children": emp.children,
        "username": emp.username,
        "temp_pass": emp.temp_pass
    }
def map_brief(emp):
    # Get boss name by querying the employee with boss_id
    boss_name = None
    if emp.boss_id:
        boss = EmployeeRepository.get_by_id(emp.boss_id)
        boss_name = boss.name if boss else None
    
    return {
        "id": emp.id,
        "name": emp.name,
        "identification": emp.identification,
        "boss_name": boss_name,
        "is_active": "activo" if emp.is_active else "inactivo",
        "position": emp.position.name if emp.position else None, 
        "project": emp.project.name if emp.project else None
    }
def map_jefes(emp):
    return {
        "id": emp.id,
        "name": emp.name,
    }


# ============================================================
# SERVICE
# ============================================================
class passwordGenerator:
    @staticmethod
    def generar_password_temporal(longitud=8):
        if longitud < 8:
            longitud = 8

        # Caracteres permitidos
        all_chars = string.ascii_letters + string.digits + string.punctuation

        # Asegurar al menos un carácter de cada tipo
        password_chars = [
            random.choice(string.ascii_uppercase),
            random.choice(string.ascii_lowercase),
            random.choice(string.digits),
            random.choice(string.punctuation),
        ]

        # Rellenar el resto
        remaining = longitud - len(password_chars)
        password_chars += [random.choice(all_chars) for _ in range(remaining)]

        # Mezclar y devolver
        random.shuffle(password_chars)
        return ''.join(password_chars)

class EmployeeService:

    @staticmethod
    def list_brief(params=None):

        filters = {}

        if params:
           
            if params.get("boss_id"):
                filters["boss_id"] = int(params.get("boss_id"))
     
            if params.get("project_id"):
                filters["project_id"] = int(params.get("project_id"))
     
            if params.get("gender_id"):
                filters["gender_id"] = int(params.get("gender_id"))

            if params.get("is_active"):
                filters["is_active"] = int(params.get("is_active"))

        if filters:
            emps = EmployeeRepository.get_filtered(filters)
        else:
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
        return EmployeeCreateEntity().dump(map_create(emp))

    @staticmethod
    def get_by_identification(identification):
        emp = EmployeeRepository.get_by_identification(identification)
        if not emp:
            return None
        return EmployeeDetailEntity().dump(map_detail(emp))
   
   
    @staticmethod
    def get_total_employees():
        count = EmployeeRepository.get_count()
        return count

    #validar si el numero que le pasas al momento de crear un cliente en el jefe inmediato tiene un 1 en el jefe o si existe 
    @staticmethod
    def validate_jefe_inmediato(jefe_id):
        jefe = EmployeeRepository.get_by_id(jefe_id)
        if not jefe or jefe.is_boss != 1:
            return False
        return True
    
    
    @staticmethod
    def create(data):

        valid = EmployeeCreateEntity().load(data)
        password_temp = passwordGenerator.generar_password_temporal(6)
        valid["temp_pass"] = 1
        boss = EmployeeService.validate_jefe_inmediato(valid.get("boss_id"))
        if not boss:
            raise ValueError("El jefe inmediato no es válido o no está autorizado para delegar.")
              
        emp = EmployeeRepository.create(valid)
        emp.set_password(password_temp)
        EmployeeRepository.update(emp)

        # Enviar correo con credenciales
        EmailService.send_credentials_email(
            email_destinatario=emp.email,
            username=emp.username,
            password_temp=password_temp,
            employee_name=emp.name
        )

        response = map_create(emp)
        response["password"] = password_temp

        return EmployeeCreateEntity().dump(response)
    


    @staticmethod
    def update_password(id, password):
        emp = EmployeeRepository.get_by_id(id)
        if not emp:
              return {"success": False, "message": "Empleado no encontrado", "status": 404}

        if len(password) < 8:
              return {"success": False, "message": "La contraseña debe tener al menos 8 caracteres", "status": 400}

        if not re.search(r"[A-Z]", password):
              return {"success": False, "message": "La contraseña debe contener al menos una letra mayúscula", "status": 400}

        if not re.search(r"[a-z]", password):
              return {"success": False, "message": "La contraseña debe contener al menos una letra minúscula", "status": 400}

        if not re.search(r"\d", password):
              return {"success": False, "message": "La contraseña debe contener al menos un número", "status": 400}

        if not re.search(r"[^A-Za-z0-9\s]", password):
              return {"success": False, "message": "La contraseña debe contener al menos un símbolo (carácter especial)", "status": 400}

        if emp.temp_pass != 1:
              return {"success": False, "message": "La contraseña no es temporal, no se puede actualizar de esta forma", "status": 400}

        emp.set_password(password)
        emp.temp_pass = 0 
        EmployeeRepository.update(emp)
        return {"success": True, "message": "Contraseña actualizada correctamente"}

    @staticmethod
    def update_state(emp_id, state_employe_id):
        emp = EmployeeRepository.get_by_id(emp_id)
        if not emp:
            return {"success": False, "message": "Empleado no encontrado", "status": 404}
        
        if not state_employe_id:
            return {"success": False, "message": "El ID del estado no puede estar vacío", "status": 400}
        
        emp.state_employe_id = state_employe_id
        EmployeeRepository.update(emp)
        return {"success": True, "message": "Estado del empleado actualizado correctamente"}

    @staticmethod
    def update(emp_id, data):
        emp = EmployeeRepository.get_by_id(emp_id)
        if not emp:
            return None
            
        valid = EmployeeCreateEntity().load(data, partial=True)

            
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

    @staticmethod
    def get_employees_with_delegar_jefe():
        """Obtiene todos los empleados que tienen permisos para delegar jefe"""
        emps = EmployeeRepository.get_employees_with_delegar_jefe()
        return EmployeeDetailEntity(many=True).dump(
            [map_jefes(e) for e in emps]
        )
