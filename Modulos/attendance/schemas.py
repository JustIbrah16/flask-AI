from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from Modulos.attendance.model import Attendance

class AttendanceSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Attendance
        load_instance = True
        include_fk = True