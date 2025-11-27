from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from Modulos.certificates.models import CertificateType, Certificate


class CertificateTypeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CertificateType
        load_instance = True
        include_fk = True

    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    template = fields.Str(allow_none=True)
    created_at = fields.DateTime(dump_only=True)


class CertificateSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Certificate
        load_instance = True
        include_fk = True

    id = fields.Integer(dump_only=True)
    certificate_type_id = fields.Integer(required=True)
    certificate_type = fields.Function(lambda obj: obj.certificate_type.name if obj.certificate_type else None, dump_only=True)
    created_by = fields.Integer(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    subject_name = fields.Str(required=True)
    subject_identificacion = fields.Integer(allow_none=True)
    subject_email = fields.Email(allow_none=True)
    certificate_content = fields.Str(dump_only=True)
