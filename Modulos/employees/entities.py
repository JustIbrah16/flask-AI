from marshmallow import Schema, fields,validates, ValidationError


# ============================================================
# BASE
# ============================================================
class EmployeeBaseEntity(Schema):
    id = fields.Int()
    name = fields.Str()
    identification = fields.Int()
    is_active = fields.Int()


# ============================================================
# RESUMEN
# ============================================================
class EmployeeBriefEntity(Schema):
    id = fields.Int()
    name = fields.Str()
    identification = fields.Int()
    boss_id = fields.Int()
    project = fields.Str()
    position = fields.Str()
    is_active = fields.Str()



# ============================================================
# DETALLE
# ============================================================
class EmployeeDetailEntity(Schema):
    id = fields.Int()
    identification = fields.Int()
    name = fields.Str()
    date_of_birth = fields.Date(allow_none=True)
    email = fields.Str()
    phone = fields.Int(allow_none=True)

    address = fields.Str(allow_none=True)
    city = fields.Str(allow_none=True)

    position = fields.Str(allow_none=True)
    area = fields.Str(allow_none=True)
    role = fields.Str(allow_none=True)

    boss_id = fields.Str(allow_none=True)
    contract_type = fields.Str(allow_none=True)

    bank = fields.Str(allow_none=True)
    account_number = fields.Int(allow_none=True)
    salary = fields.Float(allow_none=True)

    entry_date = fields.Date(allow_none=True)
    project = fields.Str(allow_none=True)
    state = fields.Str()

    gender = fields.Str(allow_none=True)
    shirt_size = fields.Str(allow_none=True)
    pants_size = fields.Int(allow_none=True)
    shoes_size = fields.Int(allow_none=True)
    coat_size = fields.Str(allow_none=True)

    eps = fields.Str(allow_none=True)
    arl = fields.Str(allow_none=True)
    studies = fields.Str(allow_none=True)

    marital_status = fields.Str(allow_none=True)
    children = fields.Int(allow_none=True)

    username = fields.Str()
    is_active = fields.Int()

    created_at = fields.DateTime()
    updated_at = fields.DateTime()
 


# ============================================================
# CREATE
# ============================================================
class EmployeeCreateEntity(Schema):
    name = fields.Str(required=True)
    identification = fields.Int(required=True)
    email = fields.Email(required=True)

    username = fields.Str(required=True)

    phone = fields.Int()
    address = fields.Str()

    city_id = fields.Int()
    position_id = fields.Int()
    area_id = fields.Int()
    role_id = fields.Int()
    project_id = fields.Int()


    is_boss = fields.Int()
    boss_id = fields.Int()
    salary = fields.Float()

    account_number = fields.Int()
    bank_id = fields.Int()

    gender_id = fields.Int()
    shirt_size_id = fields.Int()
    coat_size_id = fields.Int()
    shoes_size = fields.Int()
    studies = fields.Str()
    pants_size = fields.Int()
    entry_date = fields.Date()
    date_of_birth = fields.Date()

    eps_id = fields.Int()
    arl_id = fields.Int()

    marital_status_id = fields.Int()
    children = fields.Int()

    contract_type_id = fields.Int()

    is_active = fields.Int(load_default=1)
    temp_pass = fields.Int()
    password = fields.Str() 


# ============================================================
# UPDATE
# ============================================================
class EmployeeUpdateEntity(Schema):
    name = fields.Str(allow_none=True)
    email = fields.Str(allow_none=True)  # cambiamos de Email a Str
    phone = fields.Int(allow_none=True)
    address = fields.Str(allow_none=True)
    salary = fields.Float(allow_none=True)
    boss_id = fields.Str(allow_none=True)
    project_id = fields.Int(allow_none=True)

    @validates("email")
    def validate_email(self, value):
        if not value:  # None o ""
            return
        if "@" not in value or "." not in value:
            raise ValidationError("Correo inválido")



    
