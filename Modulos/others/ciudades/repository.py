from extensions import db
from Modulos.others.ciudades.models import City # Asegúrate de que esta importación sea correcta

class CityRepository:
    @staticmethod
    def get_all():
        """Obtiene todas las ciudades."""
        return City.query.all()
    
    @staticmethod
    def get_by_id(city_id):
        """Obtiene una ciudad por ID."""
        return City.query.get(city_id)

    @staticmethod
    def create(name):
        """Crea una nueva ciudad."""
        new_city = City(name=name)
        db.session.add(new_city)
        db.session.commit()
        return new_city

    @staticmethod
    def update(city, new_name):
        """Actualiza el nombre de una ciudad."""
        city.name = new_name
        db.session.commit()
        return city

    @staticmethod
    def delete(city):
        """Elimina una ciudad de la base de datos."""
        db.session.delete(city)
        db.session.commit()