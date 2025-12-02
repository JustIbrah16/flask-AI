from Modulos.employees.repository import EmployeeRepository
from werkzeug.security import generate_password_hash

class EmployeeService:
    @staticmethod
    def list_employees():
        return EmployeeRepository.get_all()

    @staticmethod
    def list_employees_brief():
        """Return a list of employees with only the brief fields requested by the UI.

        Fields: nombre, identificacion, jefe_inmediato, proyecto
        Ordered alphabetically by nombre.
        """
        emps = EmployeeRepository.get_all_ordered_by_name()
        result = []
        for e in emps:
            result.append({
                'nombre': e.nombre,
                'identificacion': e.identificacion,
                'jefe_inmediato': e.jefe_inmediato,
                'proyecto': e.proyecto.name if e.proyecto else None,
            })
        return result

    @staticmethod
    def get_employee(emp_id):
        return EmployeeRepository.get_by_id(emp_id)

    @staticmethod
    def create_employee(data):
        # hash password if provided
        if 'password' in data and data['password']:
            data['password'] = generate_password_hash(data['password'])
        return EmployeeRepository.create(data)

    @staticmethod
    def update_employee(emp_id, data):
        emp = EmployeeRepository.get_by_id(emp_id)
        if not emp:
            return None
        
        # hash password if being updated
        if 'password' in data and data['password']:
            data['password'] = generate_password_hash(data['password'])
        
        for key, value in data.items():
            if hasattr(emp, key) and key != 'id':
                setattr(emp, key, value)
        
        return EmployeeRepository.update(emp)

    @staticmethod
    def toggle_employee_status(emp_id):
        emp = EmployeeRepository.get_by_id(emp_id)
        if not emp:
            return None
        
        # Alternar entre 0 (inactivo) y 1 (activo)
        emp.is_active = 0 if emp.is_active == 1 else 1
        # keep `estado` field in sync with is_active
        emp.estado = 'activo' if emp.is_active == 1 else 'inactivo'
        return EmployeeRepository.update(emp)

    @staticmethod
    def delete_employee(emp_id):
        # No elimina, solo inactiva
        emp = EmployeeRepository.get_by_id(emp_id)
        if not emp:
            return None
        emp.is_active = 0  # 0: inactivo
        emp.estado = 'inactivo'
        return EmployeeRepository.update(emp)
