from extensions import db
from Modulos.others.eps.models import EPS # Asegúrate de que esta importación sea correcta

class EPSProviderRepository:
    @staticmethod
    def get_all():
        """Obtiene todos los proveedores EPS."""
        return EPS.query.all()
    
    @staticmethod
    def get_by_id(eps_id):
        """Obtiene un proveedor EPS por ID."""
        return EPS.query.get(eps_id)

    @staticmethod
    def create(name):
        """Crea un nuevo proveedor EPS."""
        new_eps = EPS(name=name)
        db.session.add(new_eps)
        db.session.commit()
        return new_eps

    @staticmethod
    def update(eps, new_name):
        """Actualiza el nombre de un proveedor EPS."""
        eps.name = new_name
        db.session.commit()
        return eps

    @staticmethod
    def delete(eps):
        """Elimina un proveedor EPS de la base de datos."""
        db.session.delete(eps)
        db.session.commit()