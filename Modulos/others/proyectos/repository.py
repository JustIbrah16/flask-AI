from extensions import db
from Modulos.others.proyectos.models import Project # Asegúrate de que esta importación sea correcta

class ProjectRepository:
    @staticmethod
    def get_all():
        """Obtiene todos los proyectos."""
        return Project.query.all()
    
    @staticmethod
    def get_by_id(project_id):
        """Obtiene un proyecto por ID."""
        return Project.query.get(project_id)

    @staticmethod
    def create(name):
        """Crea un nuevo proyecto."""
        new_project = Project(name=name)
        db.session.add(new_project)
        db.session.commit()
        return new_project

    @staticmethod
    def update(project, new_name):
        """Actualiza el nombre de un proyecto."""
        project.name = new_name
        db.session.commit()
        return project

    @staticmethod
    def delete(project):
        """Elimina un proyecto de la base de datos."""
        db.session.delete(project)
        db.session.commit()