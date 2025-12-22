from Modulos.employees.repository import EmployeeRepository
from Modulos.employees.models import Employee
from Modulos.employees.entities import  EmployeeBriefEntity, EmployeeDetailEntity, EmployeeCreateEntity, EmployeeUpdateEntity
import random
import string
from extensions import mail
from flask_mail import Message
from flask import current_app



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
        "delegar_jefe": emp.delegar_jefe,
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
def map_create(emp):
    return {
        "identificacion": emp.identificacion,
        "nombre": emp.nombre,
        "fecha_nacimiento": emp.fecha_nacimiento,
        "correo": emp.correo,
        "contacto": emp.contacto,
        "direccion": emp.direccion,
        "ciudad_id": emp.ciudad_id,
        "cargo_id": emp.cargo_id,
        "area_id": emp.area_id,
        "role_id": emp.role_id,
        "delegar_jefe": emp.delegar_jefe,
        "jefe_inmediato": emp.jefe_inmediato,
        "tipo_contrato_id": emp.tipo_contrato_id,
        "banco_id": emp.banco_id,
        "numero_cuenta_bancaria": emp.numero_cuenta_bancaria,
        "salario": emp.salario,
        "fecha_ingreso": emp.fecha_ingreso,
        "proyecto_id": emp.proyecto_id,
        "genero_id": emp.genero_id,
        "camisa_id": emp.camisa_id,
        "pantalon": emp.pantalon,
        "zapatos": emp.zapatos,
        "abrigo_id": emp.abrigo_id,
        "eps_id": emp.eps_id,
        "arl_id": emp.arl_id,
        "estudios": emp.estudios,
        "estado_civil_id": emp.estado_civil_id,
        "hijos": emp.hijos,
        "username": emp.username,
        "temp_pass": emp.temp_pass
    }
def map_brief(emp):
    return {
        "nombre": emp.nombre,
        "identificacion": emp.identificacion,
        "jefe_inmediato": emp.jefe_inmediato,
        "is_active": "activo" if emp.is_active else "inactivo",
        "cargo": emp.cargo.name if emp.cargo else None, 
        "proyecto": emp.proyecto.name if emp.proyecto else None
    }
def map_jefes(emp):
    return {
        "id": emp.id,
        "name": emp.nombre,}


# ============================================================
# SERVICE
# ============================================================
class passwordGenerator:
    @staticmethod
    def generar_password_temporal(longitud=6):
        caracteres = string.ascii_letters + string.digits
        return ''.join(random.choice(caracteres) for _ in range(longitud))

class EmployeeService:

    @staticmethod
    def list_brief(params=None):

        filters = {}

        if params:
           
            if params.get("jefe_id"):
                filters["jefe_id"] = int(params.get("jefe_id"))
     
            if params.get("proyecto_id"):
                filters["proyecto_id"] = int(params.get("proyecto_id"))
     
            if params.get("genero_id"):
                filters["genero_id"] = int(params.get("genero_id"))

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
        return EmployeeDetailEntity().dump(map_detail(emp))

    @staticmethod
    def get_by_identificacion(identificacion):
        emp = EmployeeRepository.get_by_identificacion(identificacion)
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
        if not jefe or jefe.delegar_jefe != 1:
            return False
        return True
    
    
    @staticmethod
    def create(data):

        valid = EmployeeCreateEntity().load(data)
        password_temp = passwordGenerator.generar_password_temporal(6)
        valid["temp_pass"] = 1
        boss = EmployeeService.validate_jefe_inmediato(valid["jefe_inmediato"])
        if not boss:
            raise ValueError("El jefe inmediato no es válido o no está autorizado para delegar.")
              
        emp = EmployeeRepository.create(valid)
        emp.set_password(password_temp)
        EmployeeRepository.update(emp)


        try:
         
            email_destinatario = emp.correo
            username = emp.username 

            msg = Message(
                subject="Bienvenido a la Plataforma - Tus Credenciales",
                recipients=[email_destinatario],
                sender='lfdelahozfontalvo@gmail.com'
            )
            
            msg.body = f"""
            Hola {emp.nombre},
            
            Se ha creado tu cuenta en la plataforma. Estas son tus credenciales de acceso:
            
            Usuario: {username}
            Contraseña: {password_temp}
            
            Por seguridad, te recomendamos cambiar tu contraseña al ingresar.
            """
            mail.send(msg)
            
        except Exception as e:
            print(f"Error enviando correo: {str(e)}")

        response = map_create(emp)
        response["password"] = password_temp

        return EmployeeCreateEntity().dump(response)
    


    @staticmethod
    def update_password(id, password):
        emp = EmployeeRepository.get_by_id(id)
        if not emp:
            return None

        if len(password) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")

        if emp.temp_pass != 1:
            raise ValueError("La contraseña no es temporal, no se puede actualizar de esta forma")

        emp.set_password(password)
        emp.temp_pass = 0 
        EmployeeRepository.update(emp)
        return True

        


    @staticmethod
    def update(emp_id, data):
        emp = EmployeeRepository.get_by_id(emp_id)
        if not emp:
            return None
            
        valid = EmployeeUpdateEntity().load(data, partial=True)

            
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
