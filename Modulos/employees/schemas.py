from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validate, post_load
from Modulos.employees.models import Employee

class EmployeeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Employee
        load_instance = True
        include_fk = True
        # Excluir las relaciones del auto-schema para evitar problemas de serialización
        exclude = ('ciudad', 'cargo', 'area', 'tipo_contrato', 'banco', 'proyecto', 'genero', 'camisa', 'abrigo', 'eps', 'estado_civil', 'role')
    
    # ========================================================================
    # Orden según tabla employees en database_schema.sql
    # ========================================================================
    
    # Sistema
    id = fields.Integer(dump_only=True)
    
    # Información Personal
    identificacion = fields.Integer(required=True)
    nombre = fields.Str(required=True)
    fecha_nacimiento = fields.Date(allow_none=True)
    correo = fields.Email(required=True)
    contacto = fields.Integer(allow_none=True)
    
    # Dirección
    direccion = fields.Str(allow_none=True)
    ciudad_id = fields.Integer(allow_none=True)
    ciudad = fields.Function(lambda obj: obj.ciudad.name if obj.ciudad else None, dump_only=True)
    
    # Información Laboral
    cargo_id = fields.Integer(allow_none=True)
    cargo = fields.Function(lambda obj: obj.cargo.name if obj.cargo else None, dump_only=True)
    area_id = fields.Integer(allow_none=True)
    area = fields.Function(lambda obj: obj.area.name if obj.area else None, dump_only=True)
    role_id = fields.Integer(allow_none=True)
    
    # Contrato
    jefe_inmediato = fields.Str(allow_none=True)
    tipo_contrato_id = fields.Integer(allow_none=True)
    tipo_contrato = fields.Function(lambda obj: obj.tipo_contrato.name if obj.tipo_contrato else None, dump_only=True)
    banco_id = fields.Integer(allow_none=True)
    banco = fields.Function(lambda obj: obj.banco.name if obj.banco else None, dump_only=True)
    numero_cuenta_bancaria = fields.Integer(allow_none=True)
    salario = fields.Float(allow_none=True)
    
    # Información Adicional
    fecha_ingreso = fields.Date(allow_none=True)
    proyecto_id = fields.Integer(allow_none=True)
    proyecto = fields.Function(lambda obj: obj.proyecto.name if obj.proyecto else None, dump_only=True)
    estado = fields.Str(allow_none=True)
    genero_id = fields.Integer(allow_none=True)
    genero = fields.Function(lambda obj: obj.genero.name if obj.genero else None, dump_only=True)
    
    # Tallas
    camisa_id = fields.Integer(allow_none=True)
    camisa = fields.Function(lambda obj: obj.camisa.name if obj.camisa else None, dump_only=True)
    pantalon = fields.Integer(allow_none=True)
    zapatos = fields.Integer(allow_none=True)
    abrigo_id = fields.Integer(allow_none=True)
    abrigo = fields.Function(lambda obj: obj.abrigo.name if obj.abrigo else None, dump_only=True)
    
    # Salud y Estudios
    eps_id = fields.Integer(allow_none=True)
    eps = fields.Function(lambda obj: obj.eps.name if obj.eps else None, dump_only=True)
    arl_id = fields.Integer(allow_none=True)
    arl = fields.Function(lambda obj: obj.arl.name if obj.arl else None, dump_only=True)
    estudios = fields.Str(allow_none=True)
    
    # Estado Civil
    estado_civil_id = fields.Integer(allow_none=True)
    estado_civil = fields.Function(lambda obj: obj.estado_civil.name if obj.estado_civil else None, dump_only=True)
    hijos = fields.Integer(allow_none=True)
    
    # Sistema
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    is_active = fields.Integer(allow_none=True)  # 0: inactivo, 1: activo, 2: licencia
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

