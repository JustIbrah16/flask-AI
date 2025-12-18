from Modulos.employees.repository import EmployeeRepository
from Modulos.employees.service import passwordGenerator
from werkzeug.security import check_password_hash
from extensions import mail
from flask_mail import Message
from flask import current_app


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

        try:
            email_destinatario = user.correo
            msg = Message(
                subject="Recuperación de Contraseña",
                recipients=[email_destinatario],
                sender='lfdelahozfontalvo@gmail.com'
            )

            msg.body = f"""
            Hola {user.nombre},
            
            Se ha generado una nueva contraseña temporal para tu cuenta:
            
            Contraseña temporal: {password_temp}
            
            Por seguridad, te recomendamos cambiar tu contraseña al ingresar.
            """
            mail.send(msg)

        except Exception as e:
            print(f"Error enviando correo: {str(e)}")

        return user