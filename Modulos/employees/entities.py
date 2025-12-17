from marshmallow import Schema, fields,validates, ValidationError


# ============================================================
# BASE
# ============================================================
class EmployeeBaseEntity(Schema):
    id = fields.Int()
    nombre = fields.Str()
    identificacion = fields.Int()
    is_active = fields.Int()


# ============================================================
# RESUMEN
# ============================================================
class EmployeeBriefEntity(Schema):
    nombre = fields.Str()
    identificacion = fields.Int()
    jefe_inmediato = fields.Str()
    proyecto = fields.Str()


# ============================================================
# DETALLE
# ============================================================
class EmployeeDetailEntity(Schema):
    id = fields.Int()
    identificacion = fields.Int()
    nombre = fields.Str()
    fecha_nacimiento = fields.Date(allow_none=True)
    correo = fields.Str()
    contacto = fields.Int(allow_none=True)

    direccion = fields.Str(allow_none=True)
    ciudad = fields.Str(allow_none=True)

    cargo = fields.Str(allow_none=True)
    area = fields.Str(allow_none=True)
    role = fields.Str(allow_none=True)

    jefe_inmediato = fields.Str(allow_none=True)
    tipo_contrato = fields.Str(allow_none=True)

    banco = fields.Str(allow_none=True)
    numero_cuenta_bancaria = fields.Int(allow_none=True)
    salario = fields.Float(allow_none=True)

    fecha_ingreso = fields.Date(allow_none=True)
    proyecto = fields.Str(allow_none=True)
    estado = fields.Str()

    genero = fields.Str(allow_none=True)
    camisa = fields.Str(allow_none=True)
    pantalon = fields.Int(allow_none=True)
    zapatos = fields.Int(allow_none=True)
    abrigo = fields.Str(allow_none=True)

    eps = fields.Str(allow_none=True)
    arl = fields.Str(allow_none=True)
    estudios = fields.Str(allow_none=True)

    estado_civil = fields.Str(allow_none=True)
    hijos = fields.Int(allow_none=True)

    username = fields.Str()
    is_active = fields.Int()

    created_at = fields.DateTime()
    updated_at = fields.DateTime()


# ============================================================
# CREATE
# ============================================================
class EmployeeCreateEntity(Schema):
    nombre = fields.Str(required=True)
    identificacion = fields.Int(required=True)
    correo = fields.Email(required=True)

    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

    contacto = fields.Int()
    direccion = fields.Str()

    ciudad_id = fields.Int()
    cargo_id = fields.Int()
    area_id = fields.Int()
    role_id = fields.Int()
    proyecto_id = fields.Int()

    jefe_inmediato = fields.Str()
    salario = fields.Float()

    numero_cuenta_bancaria = fields.Int()
    banco_id = fields.Int()

    genero_id = fields.Int()
    camisa_id = fields.Int()
    abrigo_id = fields.Int()
    zapatos = fields.Int()
    estudios = fields.Str()
    pantalon = fields.Int()
    fecha_ingreso = fields.Date()
    fecha_nacimiento = fields.Date()

    eps_id = fields.Int()
    arl_id = fields.Int()

    estado_civil_id = fields.Int()
    hijos = fields.Int()

    tipo_contrato_id = fields.Int()

    is_active = fields.Int(load_default=1)


# ============================================================
# UPDATE
# ============================================================
class EmployeeUpdateEntity(Schema):
    nombre = fields.Str(allow_none=True)
    correo = fields.Str(allow_none=True)  # cambiamos de Email a Str
    contacto = fields.Int(allow_none=True)
    direccion = fields.Str(allow_none=True)
    salario = fields.Float(allow_none=True)
    jefe_inmediato = fields.Str(allow_none=True)
    proyecto_id = fields.Int(allow_none=True)

    @validates("correo")
    def validate_correo(self, value):
        if not value:  # None o ""
            return
        if "@" not in value or "." not in value:
            raise ValidationError("Correo inválido")



    
