from Modulos.roles.repository import RoleRepository
from sqlalchemy.exc import IntegrityError

class RoleService:
    @staticmethod
    def list_roles():
        return RoleRepository.get_all()

    @staticmethod
    def get_role(role_id):
        role = RoleRepository.get_by_id(role_id)
        if not role:
            raise ValueError(f"Rol con ID {role_id} no encontrado.")
        return role

    @staticmethod
    def create_role(name):
        return RoleRepository.create(name=name  )

    @staticmethod
    def get_role(role_id):
        role = RoleRepository.get_by_id(role_id)
        if not role:
            raise ValueError(f"Rol con ID {role_id} no encontrado.")
        return role

    @staticmethod
    def create_role(name):
        if not name:
            raise ValueError("El nombre del rol no puede estar vacío.")
        try:
            return RoleRepository.create(name=name)
        except IntegrityError:
            # Esto maneja el caso de que el 'name' sea UNIQUE y ya exista
            raise ValueError(f"Ya existe un rol con el nombre '{name}'.")


    @staticmethod
    def update_role(role_id, new_name):
        role = RoleService.get_role(role_id) # Reutiliza la validación de existencia
        if not new_name:
            raise ValueError("El nuevo nombre del rol no puede estar vacío.")
        try:
            return RoleRepository.update(role, new_name=new_name)
        except IntegrityError:
            raise ValueError(f"Ya existe un rol con el nombre '{new_name}'.")

    @staticmethod
    def delete_role(role_id):
        role = RoleService.get_role(role_id) # Reutiliza la validación de existencia
        RoleRepository.delete(role)
        # No retorna nada, solo confirma la operación.