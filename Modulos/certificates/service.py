from Modulos.certificates.repository import CertificateTypeRepository, CertificateRepository
from Modulos.employees.repository import EmployeeRepository
from werkzeug.exceptions import NotFound
from datetime import datetime
from Modulos.certificates.utils import PDFGenerator

class CertificateService:
    # Certificate Types
    @staticmethod
    def list_types():
        return CertificateTypeRepository.get_all()

    @staticmethod
    def get_type(type_id):
        return CertificateTypeRepository.get_by_id(type_id)

    @staticmethod
    def create_type(data):
        return CertificateTypeRepository.create(data)

    @staticmethod
    def update_type(type_id, data):
        obj = CertificateTypeRepository.get_by_id(type_id)
        if not obj:
            return None
        for k, v in data.items():
            if hasattr(obj, k) and k != 'id':
                setattr(obj, k, v)
        return CertificateTypeRepository.update(obj)

    @staticmethod
    def delete_type(type_id):
        obj = CertificateTypeRepository.get_by_id(type_id)
        if not obj:
            return None
        return CertificateTypeRepository.delete(obj)

    # Certificates
    @staticmethod
    def list_certificates():
        return CertificateRepository.get_all()

    @staticmethod
    def get_certificate(cert_id):
        return CertificateRepository.get_by_id(cert_id)

    @staticmethod
    def create_certificate(data):
        # 1. Validar datos de entrada
        if 'certificate_type_id' not in data or 'subject_identificacion' not in data:
            raise ValueError("El ID del tipo de certificado y la identificación del empleado son requeridos.")

        cert_type_id = data['certificate_type_id']
        subject_id = data['subject_identificacion']

        # 2. Obtener la plantilla del certificado
        cert_type = CertificateTypeRepository.get_by_id(cert_type_id)
        if not cert_type or not cert_type.template:
            raise NotFound("El tipo de certificado no existe o no tiene una plantilla asociada.")
        
        template = cert_type.template

        # 3. Obtener los datos del empleado
        employee = EmployeeRepository.get_by_identificacion(subject_id)
        if not employee:
            raise NotFound("No se encontró un empleado con la identificación proporcionada.")


        agent = EmployeeRepository.get_by_id(data.get('created_by'))
        if not agent:
            raise NotFound("No se encontró un agente con la identificación proporcionada.")
        
        # 4. Reemplazar las variables en la plantilla
        content = template.replace('{{ nombre_empleado }}', employee.nombre or '')
        content = content.replace('{{ identificacion_empleado }}', str(employee.identificacion) or '')
        content = content.replace('{{ fecha_inicio_trabajo }}', str(employee.fecha_ingreso) or '')
        content = content.replace('{{ cargo_empleado }}', employee.cargo.name if employee.cargo else '')
        content = content.replace('{{ fecha_emision }}', datetime.now().strftime('%d de %B de %Y'))
        content = content.replace('{{ nombre_firmante }}', agent.nombre or '')
        # 5. Generar PDF a partir del HTML
        pdf_path = PDFGenerator.html_to_pdf(content)

        # 6. Guardar en la BD
        new_cert_data = {
            'certificate_type_id': cert_type_id,
            'created_by': data.get('created_by'),
            'subject_name': employee.nombre,
            'subject_identificacion': employee.identificacion,
            'subject_email': employee.correo,
            'certificate_content': content,       # HTML original
            'pdf_path': pdf_path                  # << NUEVO
        }

        return CertificateRepository.create(new_cert_data)

    @staticmethod
    def update_certificate(cert_id, data):
        obj = CertificateRepository.get_by_id(cert_id)
        if not obj:
            return None
        for k, v in data.items():
            if hasattr(obj, k) and k != 'id':
                setattr(obj, k, v)
        return CertificateRepository.update(obj)

    @staticmethod
    def delete_certificate(cert_id):
        obj = CertificateRepository.get_by_id(cert_id)
        if not obj:
            return None
        return CertificateRepository.delete(obj)

    @staticmethod
    def list_by_type(type_id):
        return CertificateRepository.get_by_type(type_id)

    @staticmethod
    def get_by_subject_id(subject_id):
        return CertificateRepository.get_by_subject_id(subject_id)
