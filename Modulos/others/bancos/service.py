from Modulos.others.bancos.repository import BankRepository
from sqlalchemy.exc import IntegrityError

class BankService:
    @staticmethod
    def list_banks():
        """Lista todos los bancos."""
        return BankRepository.get_all()
    
    @staticmethod
    def get_bank(bank_id):
        """Obtiene un banco por ID, lanza error si no existe."""
        bank = BankRepository.get_by_id(bank_id)
        if not bank:
            # Lanzamos ValueError para que el Resource lo convierta en 404
            raise ValueError(f"Banco con ID {bank_id} no encontrado.")
        return bank

    @staticmethod
    def create_bank(name):
        """Crea un nuevo banco con validación de nombre."""
        if not name:
            raise ValueError("El nombre del banco no puede estar vacío.")
        try:
            return BankRepository.create(name=name)
        except IntegrityError:
            # Maneja el caso de que el 'name' sea UNIQUE y ya exista
            raise ValueError(f"Ya existe un banco con el nombre '{name}'.")

    @staticmethod
    def update_bank(bank_id, new_name):
        """Actualiza el nombre de un banco."""
        bank = BankService.get_bank(bank_id) # Valida existencia primero
        
        if not new_name:
            raise ValueError("El nuevo nombre del banco no puede estar vacío.")
            
        try:
            return BankRepository.update(bank, new_name=new_name)
        except IntegrityError:
            raise ValueError(f"Ya existe un banco con el nombre '{new_name}'.")

    @staticmethod
    def delete_bank(bank_id):
        """Elimina un banco por ID."""
        bank = BankService.get_bank(bank_id) # Valida existencia primero
        BankRepository.delete(bank)