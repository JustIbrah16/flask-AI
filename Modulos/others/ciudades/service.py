from Modulos.others.ciudades.repository import CityRepository
from sqlalchemy.exc import IntegrityError

class CityService:
    @staticmethod
    def list_cities():
        """Lista todas las ciudades."""
        return CityRepository.get_all()
    
    @staticmethod
    def get_city(city_id):
        """Obtiene una ciudad por ID, lanza error si no existe."""
        city = CityRepository.get_by_id(city_id)
        if not city:
            # Lanzamos ValueError para que el Resource lo convierta en 404
            raise ValueError(f"Ciudad con ID {city_id} no encontrada.")
        return city

    @staticmethod
    def create_city(name):
        """Crea una nueva ciudad con validación de nombre."""
        if not name:
            raise ValueError("El nombre de la ciudad no puede estar vacío.")
        try:
            return CityRepository.create(name=name)
        except IntegrityError:
            # Maneja el caso de que el 'name' sea UNIQUE y ya exista
            raise ValueError(f"Ya existe una ciudad con el nombre '{name}'.")

    @staticmethod
    def update_city(city_id, new_name):
        """Actualiza el nombre de una ciudad."""
        city = CityService.get_city(city_id) # Valida existencia primero
        
        if not new_name:
            raise ValueError("El nuevo nombre de la ciudad no puede estar vacío.")
            
        try:
            return CityRepository.update(city, new_name=new_name)
        except IntegrityError:
            raise ValueError(f"Ya existe una ciudad con el nombre '{new_name}'.")

    @staticmethod
    def delete_city(city_id):
        """Elimina una ciudad por ID."""
        city = CityService.get_city(city_id) # Valida existencia primero
        CityRepository.delete(city)