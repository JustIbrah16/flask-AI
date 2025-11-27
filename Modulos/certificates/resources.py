from flask_restx import Namespace, Resource, fields
from flask import request
from Modulos.certificates.service import CertificateService
from Modulos.certificates.schemas import CertificateTypeSchema, CertificateSchema

certificates_ns = Namespace('certificates', description='Certificates operations')

# Models for API docs
certificate_type_model = certificates_ns.model('CertificateType', {
    'name': fields.String(required=True, description='Nombre del tipo de certificado'),
    'description': fields.String(description='Descripción'),
    'template': fields.String(description='Plantilla o contenido base del certificado'),
})

certificate_model = certificates_ns.model('CertificateCreation', {
    'certificate_type_id': fields.Integer(required=True, description='ID del tipo de certificado'),
    'created_by': fields.Integer(required=True, description='ID del empleado que crea el certificado'),
    'subject_identificacion': fields.Integer(required=True, description='Identificación del empleado a quien se le genera el certificado')
})

certificate_output_model = certificates_ns.model('CertificateOutput', {
    'id': fields.Integer,
    'certificate_type_id': fields.Integer,
    'created_by': fields.Integer,
    'subject_name': fields.String,
    'subject_identificacion': fields.Integer,
    'subject_email': fields.String,
    'certificate_content': fields.String(description='Contenido final generado'),
    'created_at': fields.DateTime,
})

# ------------------ Certificate Types ------------------
@certificates_ns.route('/types')
class CertificateTypeList(Resource):
    def get(self):
        try:
            items = CertificateService.list_types()
            schema = CertificateTypeSchema(many=True)
            return {
                'message': 'Tipos de certificado obtenidos exitosamente',
                'data': schema.dump(items)
            }, 200
        except Exception as e:
            return {'message': 'Error al obtener tipos de certificado', 'error': str(e)}, 500

    @certificates_ns.expect(certificate_type_model)
    def post(self):
        try:
            data = request.get_json() or {}
            obj = CertificateService.create_type(data)
            schema = CertificateTypeSchema()
            return {'message': 'Tipo de certificado creado', 'data': schema.dump(obj)}, 201
        except Exception as e:
            return {'message': 'Error al crear tipo de certificado', 'error': str(e)}, 400


@certificates_ns.route('/types/<int:id>')
class CertificateTypeDetail(Resource):
    def get(self, id):
        try:
            obj = CertificateService.get_type(id)
            if not obj:
                return {'message': 'Tipo de certificado no encontrado', 'type_id': id}, 404
            schema = CertificateTypeSchema()
            return {'message': 'Tipo de certificado obtenido', 'data': schema.dump(obj)}, 200
        except Exception as e:
            return {'message': 'Error al obtener tipo de certificado', 'error': str(e)}, 500

    @certificates_ns.expect(certificate_type_model)
    def put(self, id):
        try:
            data = request.get_json() or {}
            obj = CertificateService.update_type(id, data)
            if not obj:
                return {'message': 'Tipo de certificado no encontrado', 'type_id': id}, 404
            schema = CertificateTypeSchema()
            return {'message': 'Tipo de certificado actualizado', 'data': schema.dump(obj)}, 200
        except Exception as e:
            return {'message': 'Error al actualizar tipo de certificado', 'error': str(e)}, 400

    def delete(self, id):
        try:
            res = CertificateService.delete_type(id)
            if not res:
                return {'message': 'Tipo de certificado no encontrado', 'type_id': id}, 404
            return {'message': 'Tipo de certificado eliminado'}, 200
        except Exception as e:
            return {'message': 'Error al eliminar tipo de certificado', 'error': str(e)}, 400


# ------------------ Certificates ------------------
@certificates_ns.route('/')
class CertificateList(Resource):
    def get(self):
        try:
            items = CertificateService.list_certificates()
            schema = CertificateSchema(many=True)
            return {'message': 'Certificados obtenidos exitosamente', 'data': schema.dump(items)}, 200
        except Exception as e:
            return {'message': 'Error al obtener certificados', 'error': str(e)}, 500

    @certificates_ns.expect(certificate_model)
    def post(self):
        try:
            data = request.get_json() or {}
            obj = CertificateService.create_certificate(data)
            schema = CertificateSchema()
            return {'message': 'Certificado creado exitosamente', 'data': schema.dump(obj)}, 201
        except Exception as e:
            return {'message': 'Error al crear certificado', 'error': str(e)}, 400


@certificates_ns.route('/<int:id>')
class CertificateDetail(Resource):
    def get(self, id):
        try:
            obj = CertificateService.get_certificate(id)
            if not obj:
                return {'message': 'Certificado no encontrado', 'certificate_id': id}, 404
            schema = CertificateSchema()
            return {'message': 'Certificado obtenido', 'data': schema.dump(obj)}, 200
        except Exception as e:
            return {'message': 'Error al obtener certificado', 'error': str(e)}, 500

    @certificates_ns.expect(certificate_model)
    def put(self, id):
        try:
            data = request.get_json() or {}
            obj = CertificateService.update_certificate(id, data)
            if not obj:
                return {'message': 'Certificado no encontrado', 'certificate_id': id}, 404
            schema = CertificateSchema()
            return {'message': 'Certificado actualizado', 'data': schema.dump(obj)}, 200
        except Exception as e:
            return {'message': 'Error al actualizar certificado', 'error': str(e)}, 400

    def delete(self, id):
        try:
            res = CertificateService.delete_certificate(id)
            if not res:
                return {'message': 'Certificado no encontrado', 'certificate_id': id}, 404
            return {'message': 'Certificado eliminado'}, 200
        except Exception as e:
            return {'message': 'Error al eliminar certificado', 'error': str(e)}, 400


@certificates_ns.route('/type/<int:type_id>')
class CertificatesByType(Resource):
    def get(self, type_id):
        try:
            items = CertificateService.list_by_type(type_id)
            schema = CertificateSchema(many=True)
            return {'message': 'Certificados por tipo obtenidos', 'type_id': type_id, 'data': schema.dump(items)}, 200
        except Exception as e:
            return {'message': 'Error al obtener certificados por tipo', 'error': str(e)}, 500


@certificates_ns.route('/subject/<int:subject_id>')
class CertificatesBySubject(Resource):
    @certificates_ns.marshal_list_with(certificate_output_model)
    def get(self, subject_id):
        try:
            items = CertificateService.get_by_subject_id(subject_id)
            return items, 200
        except Exception as e:
            return {'message': 'Error al obtener certificados por empleado', 'error': str(e)}, 500
