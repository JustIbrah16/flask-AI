from extensions import db
from Modulos.others.cargos.models import Position # Asegúrate de que esta importación sea correcta

class PositionRepository:
    @staticmethod
    def get_all():
        """Obtiene todos los cargos."""
        return Position.query.all()
    
    @staticmethod
    def get_by_id(position_id):
        """Obtiene un cargo por ID."""
        return Position.query.get(position_id)

    @staticmethod
    def create(name):
        """Crea un nuevo cargo."""
        new_position = Position(name=name)
        db.session.add(new_position)
        db.session.commit()
        return new_position

    @staticmethod
    def update(position, new_name):
        """Actualiza el nombre de un cargo."""
        position.name = new_name
        db.session.commit()
        return position

    @staticmethod
    def delete(position):
        """Elimina un cargo de la base de datos."""
        db.session.delete(position)
        db.session.commit()