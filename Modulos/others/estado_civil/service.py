from Modulos.others.estado_civil.repository import MaritalStatusRepository
from sqlalchemy.exc import IntegrityError

class MaritalStatusService:
    @staticmethod
    def list_marital_statuses():
        """Lista todos los estados civiles."""
        return MaritalStatusRepository.get_all()
    
    @staticmethod
    def get_marital_status(status_id):
        """Obtiene un estado civil por ID, lanza error si no existe."""
        status = MaritalStatusRepository.get_by_id(status_id)
        if not status:
            # Lanzamos ValueError para que el Resource lo convierta en 404
            raise ValueError(f"Estado civil con ID {status_id} no encontrado.")
        return status

    @staticmethod
    def create_marital_status(name):
        """Crea un nuevo estado civil con validación de nombre."""
        if not name:
            raise ValueError("El nombre del estado civil no puede estar vacío.")
        try:
            return MaritalStatusRepository.create(name=name)
        except IntegrityError:
            # Maneja el caso de que el 'name' sea UNIQUE y ya exista
            raise ValueError(f"Ya existe un estado civil con el nombre '{name}'.")

    @staticmethod
    def update_marital_status(status_id, new_name):
        """Actualiza el nombre de un estado civil."""
        status = MaritalStatusService.get_marital_status(status_id) # Valida existencia primero
        
        if not new_name:
            raise ValueError("El nuevo nombre del estado civil no puede estar vacío.")
            
        try:
            return MaritalStatusRepository.update(status, new_name=new_name)
        except IntegrityError:
            raise ValueError(f"Ya existe un estado civil con el nombre '{new_name}'.")

    @staticmethod
    def delete_marital_status(status_id):
        """Elimina un estado civil por ID."""
        status = MaritalStatusService.get_marital_status(status_id) # Valida existencia primero
        MaritalStatusRepository.delete(status)