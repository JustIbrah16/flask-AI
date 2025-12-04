from Modulos.others.areas.repository import AreaRepository
from sqlalchemy.exc import IntegrityError

class AreaService:
    @staticmethod
    def list_areas():
        return AreaRepository.get_all()

    @staticmethod
    def get_area(area_id):
        area = AreaRepository.get_by_id(area_id)
        if not area:
            raise ValueError(f"Área con ID {area_id} no encontrada.")
        return area

    @staticmethod
    def create_area(name):
        if not name:
            raise ValueError("El nombre del área no puede estar vacío.")
        try:
            return AreaRepository.create(name=name)
        except IntegrityError:
            # Esto maneja el caso de que el 'name' sea UNIQUE y ya exista
            raise ValueError(f"Ya existe un área con el nombre '{name}'.")


    @staticmethod
    def update_area(area_id, new_name):
        area = AreaService.get_area(area_id) # Reutiliza la validación de existencia
        if not new_name:
            raise ValueError("El nuevo nombre del área no puede estar vacío.")
        try:
            return AreaRepository.update(area, new_name=new_name)
        except IntegrityError:
            raise ValueError(f"Ya existe un área con el nombre '{new_name}'.")

    @staticmethod
    def delete_area(area_id):
        area = AreaService.get_area(area_id) # Reutiliza la validación de existencia
        AreaRepository.delete(area)
        # No retorna nada, solo confirma la operación.