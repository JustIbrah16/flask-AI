from Modulos.others.generos.repository import GenderRepository
from sqlalchemy.exc import IntegrityError

class GenderService:
    @staticmethod
    def list_genders():
        """Lista todos los géneros."""
        return GenderRepository.get_all()
    
    @staticmethod
    def get_gender(gender_id):
        """Obtiene un género por ID, lanza error si no existe."""
        gender = GenderRepository.get_by_id(gender_id)
        if not gender:
            # Lanzamos ValueError para que el Resource lo convierta en 404
            raise ValueError(f"Género con ID {gender_id} no encontrado.")
        return gender

    @staticmethod
    def create_gender(name):
        """Crea un nuevo género con validación de nombre."""
        if not name:
            raise ValueError("El nombre del género no puede estar vacío.")
        try:
            return GenderRepository.create(name=name)
        except IntegrityError:
            # Maneja el caso de que el 'name' sea UNIQUE y ya exista
            raise ValueError(f"Ya existe un género con el nombre '{name}'.")

    @staticmethod
    def update_gender(gender_id, new_name):
        """Actualiza el nombre de un género."""
        gender = GenderService.get_gender(gender_id) # Valida existencia primero
        
        if not new_name:
            raise ValueError("El nuevo nombre del género no puede estar vacío.")
            
        try:
            return GenderRepository.update(gender, new_name=new_name)
        except IntegrityError:
            raise ValueError(f"Ya existe un género con el nombre '{new_name}'.")

    @staticmethod
    def delete_gender(gender_id):
        """Elimina un género por ID."""
        gender = GenderService.get_gender(gender_id) # Valida existencia primero
        GenderRepository.delete(gender)