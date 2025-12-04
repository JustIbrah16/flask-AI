from extensions import db
from Modulos.others.generos.models import Gender # Asegúrate de que esta importación sea correcta

class GenderRepository:
    @staticmethod
    def get_all():
        """Obtiene todos los géneros."""
        return Gender.query.all()
    
    @staticmethod
    def get_by_id(gender_id):
        """Obtiene un género por ID."""
        return Gender.query.get(gender_id)

    @staticmethod
    def create(name):
        """Crea un nuevo género."""
        new_gender = Gender(name=name)
        db.session.add(new_gender)
        db.session.commit()
        return new_gender

    @staticmethod
    def update(gender, new_name):
        """Actualiza el nombre de un género."""
        gender.name = new_name
        db.session.commit()
        return gender

    @staticmethod
    def delete(gender):
        """Elimina un género de la base de datos."""
        db.session.delete(gender)
        db.session.commit()