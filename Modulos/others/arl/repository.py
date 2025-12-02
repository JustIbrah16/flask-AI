from extensions import db
from Modulos.others.arl.models import ARL # Asegúrate de que esta importación sea correcta

class ARLProviderRepository:
    @staticmethod
    def get_all():
        """Obtiene todos los proveedores ARL."""
        return ARL.query.all()
    
    @staticmethod
    def get_by_id(arl_id):
        """Obtiene un proveedor ARL por ID."""
        return ARL.query.get(arl_id)

    @staticmethod
    def create(name):
        """Crea un nuevo proveedor ARL."""
        new_arl = ARL(name=name)
        db.session.add(new_arl)
        db.session.commit()
        return new_arl

    @staticmethod
    def update(arl, new_name):
        """Actualiza el nombre de un proveedor ARL."""
        arl.name = new_name
        db.session.commit()
        return arl

    @staticmethod
    def delete(arl):
        """Elimina un proveedor ARL de la base de datos."""
        db.session.delete(arl)
        db.session.commit()