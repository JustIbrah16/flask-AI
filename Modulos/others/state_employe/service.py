from Modulos.others.state_employe.repository import StateEmployeRepository
from sqlalchemy.exc import IntegrityError


class StateEmployeService:
    @staticmethod
    def list_items():
        return StateEmployeRepository.get_all()

    @staticmethod
    def get_item(item_id):
        item = StateEmployeRepository.get_by_id(item_id)
        if not item:
            raise ValueError(f"Estado con ID {item_id} no encontrado.")
        return item

    @staticmethod
    def create_item(name):
        if not name:
            raise ValueError("El nombre no puede estar vacío.")
        try:
            return StateEmployeRepository.create(name=name)
        except IntegrityError:
            raise ValueError(f"Ya existe un estado con el nombre '{name}'.")

    @staticmethod
    def update_item(item_id, new_name):
        item = StateEmployeService.get_item(item_id)
        if not new_name:
            raise ValueError("El nuevo nombre no puede estar vacío.")
        try:
            return StateEmployeRepository.update(item, new_name=new_name)
        except IntegrityError:
            raise ValueError(f"Ya existe un estado con el nombre '{new_name}'.")

    @staticmethod
    def delete_item(item_id):
        item = StateEmployeService.get_item(item_id)
        StateEmployeRepository.delete(item)
