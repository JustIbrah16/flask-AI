from Modulos.employees.repository import EmployeeRepository
from Modulos.employees.service import passwordGenerator
from werkzeug.security import check_password_hash
from email_service import EmailService


class AuthService:
    @staticmethod
    def login(username, password):
        user = EmployeeRepository.get_employee_by_username(username)
        if not user:
            return None
        if not check_password_hash(user.password, password):
            return None
        return user

    @staticmethod
    def forget_password(email):
        user = EmployeeRepository.get_employee_by_email(email)
        if not user:
            return None
        if user.temp_pass == 1:
            return None
        password_temp = passwordGenerator.generar_password_temporal()
        user.set_password(password_temp)
        user.temp_pass = 1
        EmployeeRepository.update(user)

        # Enviar correo de recuperación de contraseña
        EmailService.send_password_recovery_email(
            email_destinatario=user.email,
            password_temp=password_temp,
            employee_name=user.name
        )

        return user