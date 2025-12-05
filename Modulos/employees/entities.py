from marshmallow import Schema, fields


# ============================================================
#  ENTIDAD BASE (estructura mínima)
# ============================================================
class EmployeeBaseEntity(Schema):
    id = fields.Int()
    nombre = fields.Str()
    identificacion = fields.Int()
    is_active = fields.Int()


# ============================================================
#  ENTIDAD PARA LISTAR (resumen)
# ============================================================
class EmployeeBriefEntity(Schema):
    nombre = fields.Str()
    identificacion = fields.Int()
    jefe_inmediato = fields.Str()
    proyecto = fields.Str()


# ============================================================
#  ENTIDAD DETALLADA (perfil completo)
# ============================================================
class EmployeeDetailEntity(Schema):
    id = fields.Int()
    identificacion = fields.Int()
    nombre = fields.Str()
    fecha_nacimiento = fields.Date()
    correo = fields.Str()
    contacto = fields.Int()

    direccion = fields.Str()
    ciudad = fields.Str()

    cargo = fields.Str()
    area = fields.Str()
    role = fields.Str()

    jefe_inmediato = fields.Str()
    tipo_contrato = fields.Str()

    banco = fields.Str()
    numero_cuenta_bancaria = fields.Int()
    salario = fields.Float()

    fecha_ingreso = fields.Date()
    proyecto = fields.Str()
    estado = fields.Str()

    genero = fields.Str()
    camisa = fields.Str()
    pantalon = fields.Int()
    zapatos = fields.Int()
    abrigo = fields.Str()

    eps = fields.Str()
    arl = fields.Str()
    estudios = fields.Str()

    estado_civil = fields.Str()
    hijos = fields.Int()

    username = fields.Str()
    is_active = fields.Int()

    created_at = fields.DateTime()
    updated_at = fields.DateTime()


# ============================================================
#  ENTIDAD PARA CREAR EMPLEADOS
# ============================================================
class EmployeeCreateEntity(Schema):
    nombre = fields.Str(required=True)
    identificacion = fields.Int(required=True)
    correo = fields.Email(required=True)
    contacto = fields.Int()
    direccion = fields.Str()
    fecha_nacimiento = fields.Date()
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
    eps_id = fields.Int()
    arl_id = fields.Int()
    estado_civil_id = fields.Int()
    hijos = fields.Int()
    tipo_contrato_id = fields.Int()


# ============================================================
#  ENTIDAD PARA ACTUALIZAR EMPLEADOS (parcial)
# ============================================================
class EmployeeUpdateEntity(Schema):
    nombre = fields.Str()
    correo = fields.Email()
    contacto = fields.Int()
    direccion = fields.Str()
    salario = fields.Float()
    jefe_inmediato = fields.Str()
    proyecto_id = fields.Int()
    is_active = fields.Int()


# ============================================================
#  ENTIDAD DINÁMICA (si quieres elegir campos)
#  Ejemplo: EmployeeDynamicEntity(only=["id", "nombre"])
# ============================================================
class EmployeeDynamicEntity(Schema):
    class Meta:
        fields = ()  # Se setea dinámicamente

    def __init__(self, only=None, **kwargs):
        super().__init__(only=only, **kwargs)
