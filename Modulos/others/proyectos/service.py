from Modulos.others.proyectos.repository import ProjectRepository
from sqlalchemy.exc import IntegrityError

class ProjectService:
    @staticmethod
    def list_projects():
        """Lista todos los proyectos."""
        return ProjectRepository.get_all()
    
    @staticmethod
    def get_project(project_id):
        """Obtiene un proyecto por ID, lanza error si no existe."""
        project = ProjectRepository.get_by_id(project_id)
        if not project:
            # Lanzamos ValueError para que el Resource lo convierta en 404
            raise ValueError(f"Proyecto con ID {project_id} no encontrado.")
        return project

    @staticmethod
    def create_project(name):
        """Crea un nuevo proyecto con validación de nombre."""
        if not name:
            raise ValueError("El nombre del proyecto no puede estar vacío.")
        try:
            return ProjectRepository.create(name=name)
        except IntegrityError:
            # Maneja el caso de que el 'name' sea UNIQUE y ya exista
            raise ValueError(f"Ya existe un proyecto con el nombre '{name}'.")

    @staticmethod
    def update_project(project_id, new_name):
        """Actualiza el nombre de un proyecto."""
        project = ProjectService.get_project(project_id) # Valida existencia primero
        
        if not new_name:
            raise ValueError("El nuevo nombre del proyecto no puede estar vacío.")
            
        try:
            return ProjectRepository.update(project, new_name=new_name)
        except IntegrityError:
            raise ValueError(f"Ya existe un proyecto con el nombre '{new_name}'.")

    @staticmethod
    def delete_project(project_id):
        """Elimina un proyecto por ID."""
        project = ProjectService.get_project(project_id) # Valida existencia primero
        ProjectRepository.delete(project)