from Modulos.employees.repository import EmployeeRepository
from werkzeug.security import check_password_hash


class AuthService:
    @staticmethod
    def login(username, password):
        user = EmployeeRepository.get_employee_by_username(username)
        if not user:
            return None
        if not check_password_hash(user.password, password):
            return None
        return user

    def forget_password(self, gmail):
        user = EmployeeRepository.get_employee_by_email(gmail)
        if not user:
            return None
        if user.temp_pass == 1:
            return None
        return user