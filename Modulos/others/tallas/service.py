from Modulos.others.tallas.repository import SizeRepository
from sqlalchemy.exc import IntegrityError

class SizeService:
    @staticmethod
    def list_sizes():
        """Lista todas las tallas."""
        return SizeRepository.get_all()
    
    @staticmethod
    def get_size(size_id):
        """Obtiene una talla por ID, lanza error si no existe."""
        size = SizeRepository.get_by_id(size_id)
        if not size:
            # Lanzamos ValueError para que el Resource lo convierta en 404
            raise ValueError(f"Talla con ID {size_id} no encontrada.")
        return size

    @staticmethod
    def create_size(name):
        """Crea una nueva talla con validación de nombre."""
        if not name:
            raise ValueError("El nombre de la talla no puede estar vacío.")
        try:
            return SizeRepository.create(name=name)
        except IntegrityError:
            # Maneja el caso de que el 'name' sea UNIQUE y ya exista
            raise ValueError(f"Ya existe una talla con el nombre '{name}'.")

    @staticmethod
    def update_size(size_id, new_name):
        """Actualiza el nombre de una talla."""
        size = SizeService.get_size(size_id) # Valida existencia primero
        
        if not new_name:
            raise ValueError("El nuevo nombre de la talla no puede estar vacío.")
            
        try:
            return SizeRepository.update(size, new_name=new_name)
        except IntegrityError:
            raise ValueError(f"Ya existe una talla con el nombre '{new_name}'.")

    @staticmethod
    def delete_size(size_id):
        """Elimina una talla por ID."""
        size = SizeService.get_size(size_id) # Valida existencia primero
        SizeRepository.delete(size)