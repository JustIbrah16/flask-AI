from Modulos.attendance.repository import AttendanceRepository
from datetime import datetime, timedelta

class AttendanceService:
    @staticmethod
    def get_all():
        return AttendanceRepository.get_all()

    @staticmethod
    def get_by_employee(employee_id, from_date=None, to_date=None):
        records = AttendanceRepository.get_by_employee(employee_id, from_date, to_date)
        return [r.to_dict() for r in records]

    @staticmethod
    def get_today_attendance(employee_id):
        from datetime import date
        today = date.today()
        record = AttendanceRepository.get_by_date(employee_id, today)
        if not record:
            return None
        return record.to_dict()

    @staticmethod
    def check_in(employee_id):
        """Registrar entrada del empleado"""
        from datetime import date
        today = date.today()
        
        # Buscar si ya existe registro para hoy
        existing = AttendanceRepository.get_by_date(employee_id, today)
        
        if existing and existing.check_in:
            return None  # Ya hizo check-in hoy
        
        if existing:
            # Actualizar check_in si no existe
            existing.check_in = datetime.now()
            return AttendanceRepository.update(existing)
        else:
            # Crear nuevo registro
            data = {
                'employee_id': employee_id,
                'check_in': datetime.now(),
                'attendance_date': today,
                'status': 'present'
            }
            return AttendanceRepository.create(data)

    @staticmethod
    def check_out(employee_id):
        """Registrar salida del empleado y calcular horas trabajadas"""
        from datetime import date
        today = date.today()
        
        record = AttendanceRepository.get_by_date(employee_id, today)
        
        if not record or not record.check_in:
            return None  # No hay check-in para hoy
        
        record.check_out = datetime.now()
        
        # Calcular horas trabajadas
        if record.check_in and record.check_out:
            time_diff = record.check_out - record.check_in
            hours_worked = time_diff.total_seconds() / 3600
            record.worked_hours = round(hours_worked, 2)
        
        return AttendanceRepository.update(record)

    @staticmethod
    def record(data):
        """Crear registro manual de asistencia"""
        record = AttendanceRepository.create(data)
        
        # Calcular horas si se proporcionan check_in y check_out
        if record.check_in and record.check_out:
            time_diff = record.check_out - record.check_in
            hours_worked = time_diff.total_seconds() / 3600
            record.worked_hours = round(hours_worked, 2)
            AttendanceRepository.update(record)
        
        return record

    @staticmethod
    def get_employee_summary(employee_id, from_date, to_date):
        """Obtener resumen de asistencia y horas trabajadas"""
        records = AttendanceRepository.get_by_employee(employee_id, from_date, to_date)
        
        total_days = len(records)
        total_hours = sum(r.worked_hours for r in records if r.worked_hours)
        present_days = len([r for r in records if r.status == 'present'])
        absent_days = len([r for r in records if r.status == 'absent'])
        late_days = len([r for r in records if r.status == 'late'])
        
        return {
            'employee_id': employee_id,
            'total_days': total_days,
            'total_hours': round(total_hours, 2),
            'present_days': present_days,
            'absent_days': absent_days,
            'late_days': late_days,
            'average_hours_per_day': round(total_hours / total_days, 2) if total_days > 0 else 0,
            'from_date': from_date.isoformat() if from_date else None,
            'to_date': to_date.isoformat() if to_date else None,
        }
