from extensions import db
from datetime import datetime


class Report(db.Model):
    __tablename__ = 'reports'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    report_type = db.Column(db.String(50))  # 'daily', 'weekly', 'monthly', 'incident'
    status = db.Column(db.String(20), default='pending')  # pending | reviewed | closed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    employee = db.relationship('Employee', backref='reports')

    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'title': self.title,
            'description': self.description,
            'report_type': self.report_type,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
