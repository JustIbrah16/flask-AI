from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from Modulos.vacations.model import VacationRequest

class VacationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = VacationRequest
        load_instance = True
        include_fk = True
