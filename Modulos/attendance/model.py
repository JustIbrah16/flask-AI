from extensions import db
from datetime import datetime


class Attendance(db.Model):
    __tablename__ = 'attendance'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    check_in = db.Column(db.DateTime)  # Hora de entrada
    check_out = db.Column(db.DateTime)  # Hora de salida
    worked_hours = db.Column(db.Float, default=0)  # Horas trabajadas calculadas
    attendance_date = db.Column(db.Date, default=datetime.utcnow)  # Fecha del registro
    status = db.Column(db.String(20), default='present')  # present, absent, late, half-day
    notes = db.Column(db.Text)  # Notas adicionales
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    employee = db.relationship('Employee', backref='attendance_records')

    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'check_in': self.check_in.isoformat() if self.check_in else None,
            'check_out': self.check_out.isoformat() if self.check_out else None,
            'worked_hours': self.worked_hours,
            'attendance_date': self.attendance_date.isoformat() if self.attendance_date else None,
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
