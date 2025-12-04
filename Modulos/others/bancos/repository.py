from extensions import db
from Modulos.others.bancos.models import Bank # Asegúrate de que esta importación sea correcta

class BankRepository:
    @staticmethod
    def get_all():
        """Obtiene todos los bancos."""
        return Bank.query.all()
    
    @staticmethod
    def get_by_id(bank_id):
        """Obtiene un banco por ID."""
        return Bank.query.get(bank_id)

    @staticmethod
    def create(name):
        """Crea un nuevo banco."""
        new_bank = Bank(name=name)
        db.session.add(new_bank)
        db.session.commit()
        return new_bank

    @staticmethod
    def update(bank, new_name):
        """Actualiza el nombre de un banco."""
        bank.name = new_name
        db.session.commit()
        return bank

    @staticmethod
    def delete(bank):
        """Elimina un banco de la base de datos."""
        db.session.delete(bank)
        db.session.commit()