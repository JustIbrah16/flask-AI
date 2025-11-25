from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from Modulos.reports.model import Report


class ReportSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Report
        load_instance = True
        include_fk = True
