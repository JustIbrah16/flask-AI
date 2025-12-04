from extensions import db
from Modulos.others.estado_civil.models import MaritalStatus # Asegúrate de que esta importación sea correcta

class MaritalStatusRepository:
    @staticmethod
    def get_all():
        """Obtiene todos los estados civiles."""
        return MaritalStatus.query.all()
    
    @staticmethod
    def get_by_id(status_id):
        """Obtiene un estado civil por ID."""
        return MaritalStatus.query.get(status_id)

    @staticmethod
    def create(name):
        """Crea un nuevo estado civil."""
        new_status = MaritalStatus(name=name)
        db.session.add(new_status)
        db.session.commit()
        return new_status

    @staticmethod
    def update(status, new_name):
        """Actualiza el nombre de un estado civil."""
        status.name = new_name
        db.session.commit()
        return status

    @staticmethod
    def delete(status):
        """Elimina un estado civil de la base de datos."""
        db.session.delete(status)
        db.session.commit()