from Modulos.others.cargos.repository import PositionRepository
from sqlalchemy.exc import IntegrityError

class PositionService:
    @staticmethod
    def list_positions():
        """Lista todos los cargos."""
        return PositionRepository.get_all()
    
    @staticmethod
    def get_position(position_id):
        """Obtiene un cargo por ID, lanza error si no existe."""
        position = PositionRepository.get_by_id(position_id)
        if not position:
            # Lanzamos ValueError para que el Resource lo convierta en 404
            raise ValueError(f"Cargo con ID {position_id} no encontrado.")
        return position

    @staticmethod
    def create_position(name):
        """Crea un nuevo cargo con validación de nombre."""
        if not name:
            raise ValueError("El nombre del cargo no puede estar vacío.")
        try:
            return PositionRepository.create(name=name)
        except IntegrityError:
            # Maneja el caso de que el 'name' sea UNIQUE y ya exista
            raise ValueError(f"Ya existe un cargo con el nombre '{name}'.")

    @staticmethod
    def update_position(position_id, new_name):
        """Actualiza el nombre de un cargo."""
        position = PositionService.get_position(position_id) # Valida existencia primero
        
        if not new_name:
            raise ValueError("El nuevo nombre del cargo no puede estar vacío.")
            
        try:
            return PositionRepository.update(position, new_name=new_name)
        except IntegrityError:
            raise ValueError(f"Ya existe un cargo con el nombre '{new_name}'.")

    @staticmethod
    def delete_position(position_id):
        """Elimina un cargo por ID."""
        position = PositionService.get_position(position_id) # Valida existencia primero
        PositionRepository.delete(position)