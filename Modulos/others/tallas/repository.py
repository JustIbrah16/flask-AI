from extensions import db
from Modulos.others.tallas.models import Size # Asegúrate de que esta importación sea correcta

class SizeRepository:
    @staticmethod
    def get_all():
        """Obtiene todas las tallas."""
        return Size.query.all()
    
    @staticmethod
    def get_by_id(size_id):
        """Obtiene una talla por ID."""
        return Size.query.get(size_id)

    @staticmethod
    def create(name):
        """Crea una nueva talla."""
        new_size = Size(name=name)
        db.session.add(new_size)
        db.session.commit()
        return new_size

    @staticmethod
    def update(size, new_name):
        """Actualiza el nombre de una talla."""
        size.name = new_name
        db.session.commit()
        return size

    @staticmethod
    def delete(size):
        """Elimina una talla de la base de datos."""
        db.session.delete(size)
        db.session.commit()