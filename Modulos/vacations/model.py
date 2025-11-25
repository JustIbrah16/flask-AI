from extensions import db
from datetime import date


class VacationRequest(db.Model):
    __tablename__ = "vacation_requests"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    reason = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), default="pending")  # pending | approved | rejected
    created_at = db.Column(db.Date, default=date.today)

    # relación opcional (si manejas modelo Employee)
    employee = db.relationship("Employee", backref="vacation_requests")

    def to_dict(self):
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "start_date": str(self.start_date),
            "end_date": str(self.end_date),
            "reason": self.reason,
            "status": self.status,
            "created_at": str(self.created_at),
        }
