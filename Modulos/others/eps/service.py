from Modulos.others.eps.repository import EPSProviderRepository
from sqlalchemy.exc import IntegrityError

class EPSProviderService:
    @staticmethod
    def list_eps_providers():
        """Lista todos los proveedores EPS."""
        return EPSProviderRepository.get_all()
    
    @staticmethod
    def get_eps_provider(eps_id):
        """Obtiene un proveedor EPS por ID, lanza error si no existe."""
        eps = EPSProviderRepository.get_by_id(eps_id)
        if not eps:
            # Lanzamos ValueError para que el Resource lo convierta en 404
            raise ValueError(f"Proveedor EPS con ID {eps_id} no encontrado.")
        return eps

    @staticmethod
    def create_eps_provider(name):
        """Crea un nuevo proveedor EPS con validación de nombre."""
        if not name:
            raise ValueError("El nombre del proveedor EPS no puede estar vacío.")
        try:
            return EPSProviderRepository.create(name=name)
        except IntegrityError:
            # Maneja el caso de que el 'name' sea UNIQUE y ya exista
            raise ValueError(f"Ya existe un proveedor EPS con el nombre '{name}'.")

    @staticmethod
    def update_eps_provider(eps_id, new_name):
        """Actualiza el nombre de un proveedor EPS."""
        eps = EPSProviderService.get_eps_provider(eps_id) # Valida existencia primero
        
        if not new_name:
            raise ValueError("El nuevo nombre del proveedor EPS no puede estar vacío.")
            
        try:
            return EPSProviderRepository.update(eps, new_name=new_name)
        except IntegrityError:
            raise ValueError(f"Ya existe un proveedor EPS con el nombre '{new_name}'.")

    @staticmethod
    def delete_eps_provider(eps_id):
        """Elimina un proveedor EPS por ID."""
        eps = EPSProviderService.get_eps_provider(eps_id) # Valida existencia primero
        EPSProviderRepository.delete(eps)