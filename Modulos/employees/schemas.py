from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validate, post_load
from Modulos.employees.models import Employee

class EmployeeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Employee
        load_instance = True
        include_fk = True
        # Excluir las relaciones del auto-schema para evitar problemas de serialización
        exclude = ('city', 'position', 'area', 'contract_type', 'bank', 'project', 'gender', 'shirt_size', 'coat_size', 'eps', 'marital_status', 'role')
    
    # ========================================================================
    # Orden según tabla employees en database_schema.sql
    # ========================================================================
    
    # Sistema
    id = fields.Integer(dump_only=True)
    
    # Información Personal
    identification = fields.Integer(required=True)
    name = fields.Str(required=True)
    date_of_birth = fields.Date(allow_none=True)
    email = fields.Email(required=True)
    phone = fields.Integer(allow_none=True)
    
    # Dirección
    address = fields.Str(allow_none=True)
    city_id = fields.Integer(allow_none=True)
    city = fields.Function(lambda obj: obj.city.name if obj.city else None, dump_only=True)
    
    # Información Laboral
    position_id = fields.Integer(allow_none=True)
    position = fields.Function(lambda obj: obj.position.name if obj.position else None, dump_only=True)
    area_id = fields.Integer(allow_none=True)
    area = fields.Function(lambda obj: obj.area.name if obj.area else None, dump_only=True)
    role_id = fields.Integer(allow_none=True)
    
    # Contrato
    boss_id = fields.Int(allow_none=True)
    contract_type_id = fields.Integer(allow_none=True)
    contract_type = fields.Function(lambda obj: obj.contract_type.name if obj.contract_type else None, dump_only=True)
    bank_id = fields.Integer(allow_none=True)
    bank = fields.Function(lambda obj: obj.bank.name if obj.bank else None, dump_only=True)
    account_number = fields.Integer(allow_none=True)
    salary = fields.Float(allow_none=True)
    
    # Información Adicional
    entry_date = fields.Date(allow_none=True)
    project_id = fields.Integer(allow_none=True)
    project = fields.Function(lambda obj: obj.project.name if obj.project else None, dump_only=True)
    state = fields.Str(allow_none=True)
    gender_id = fields.Integer(allow_none=True)
    gender = fields.Function(lambda obj: obj.gender.name if obj.gender else None, dump_only=True)
    
    # Tallas
    shirt_size_id = fields.Integer(allow_none=True)
    shirt_size = fields.Function(lambda obj: obj.shirt_size.name if obj.shirt_size else None, dump_only=True)
    pants_size = fields.Integer(allow_none=True)
    shoes_size = fields.Integer(allow_none=True)
    coat_size_id = fields.Integer(allow_none=True)
    coat_size = fields.Function(lambda obj: obj.coat_size.name if obj.coat_size else None, dump_only=True)
    
    # Salud y Estudios
    eps_id = fields.Integer(allow_none=True)
    eps = fields.Function(lambda obj: obj.eps.name if obj.eps else None, dump_only=True)
    arl_id = fields.Integer(allow_none=True)
    arl = fields.Function(lambda obj: obj.arl.name if obj.arl else None, dump_only=True)
    studies = fields.Str(allow_none=True)
    
    # Estado Civil
    marital_status_id = fields.Integer(allow_none=True)
    marital_status = fields.Function(lambda obj: obj.marital_status.name if obj.marital_status else None, dump_only=True)
    children = fields.Integer(allow_none=True)
    
    # Sistema
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    is_active = fields.Integer(allow_none=True)  # 0: inactivo, 1: activo, 2: licencia
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

