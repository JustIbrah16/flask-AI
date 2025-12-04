from Modulos.others.arl.repository import ARLProviderRepository
from sqlalchemy.exc import IntegrityError

class ARLProviderService:
    @staticmethod
    def list_arl_providers():
        """Lista todos los proveedores ARL."""
        return ARLProviderRepository.get_all()

    @staticmethod
    def get_arl_provider(arl_id):
        """Obtiene un proveedor ARL por ID, lanza error si no existe."""
        arl = ARLProviderRepository.get_by_id(arl_id)
        if not arl:
            # Lanzamos ValueError para que el Resource lo convierta en 404
            raise ValueError(f"Proveedor ARL con ID {arl_id} no encontrado.")
        return arl

    @staticmethod
    def create_arl_provider(name):
        """Crea un nuevo proveedor ARL con validación de nombre."""
        if not name:
            raise ValueError("El nombre del proveedor ARL no puede estar vacío.")
        try:
            return ARLProviderRepository.create(name=name)
        except IntegrityError:
            # Maneja el caso de que el 'name' sea UNIQUE y ya exista
            raise ValueError(f"Ya existe un proveedor ARL con el nombre '{name}'.")

    @staticmethod
    def update_arl_provider(arl_id, new_name):
        """Actualiza el nombre de un proveedor ARL."""
        arl = ARLProviderService.get_arl_provider(arl_id) # Valida existencia primero
        
        if not new_name:
            raise ValueError("El nuevo nombre del proveedor ARL no puede estar vacío.")
            
        try:
            return ARLProviderRepository.update(arl, new_name=new_name)
        except IntegrityError:
            raise ValueError(f"Ya existe un proveedor ARL con el nombre '{new_name}'.")

    @staticmethod
    def delete_arl_provider(arl_id):
        """Elimina un proveedor ARL por ID."""
        arl = ARLProviderService.get_arl_provider(arl_id) # Valida existencia primero
        ARLProviderRepository.delete(arl)