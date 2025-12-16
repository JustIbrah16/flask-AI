from extensions import db
from Modulos.roles.models import Role

class RoleRepository:
    @staticmethod
    def get_all():
        return Role.query.all()
    
    @staticmethod
    def get_by_id(role_id):
        return Role.query.get(role_id)
    @staticmethod
    def create(name):
        new_role = Role(name=name)
        db.session.add(new_role)
        db.session.commit()
        return new_role

    @staticmethod
    def update(role, new_name):
        role.name = new_name
        db.session.commit()
        return role

    @staticmethod
    def delete(role):
        db.session.delete(role)
        db.session.commit()
