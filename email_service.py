from extensions import mail
from flask_mail import Message
from email_templates import EmailTemplates


class EmailService:
    @staticmethod
    def send_credentials_email(email_destinatario, username, password_temp, employee_name):
      
        try:
            # Obtener la plantilla HTML
            html_body = EmailTemplates.credentials_template(
                employee_name=employee_name,
                username=username,
                password_temp=password_temp
            )
            
            msg = Message(
                subject="Bienvenido a la Plataforma - Tus Credenciales",
                recipients=[email_destinatario],
                sender='lfdelahozfontalvo@gmail.com',
                html=html_body
            )
            
            mail.send(msg)
            return True
            
        except Exception as e:
            print(f"Error enviando correo a {email_destinatario}: {str(e)}")
            return False

    @staticmethod
    def send_password_recovery_email(email_destinatario, password_temp, employee_name):
     
        try:
            # Obtener la plantilla HTML
            html_body = EmailTemplates.password_recovery_template(
                employee_name=employee_name,
                password_temp=password_temp
            )
            
            msg = Message(
                subject="Recuperación de Contraseña",
                recipients=[email_destinatario],
                sender='lfdelahozfontalvo@gmail.com',
                html=html_body
            )
            
            mail.send(msg)
            return True
            
        except Exception as e:
            print(f"Error enviando correo a {email_destinatario}: {str(e)}")
            return False
