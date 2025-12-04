from Modulos.others.contratos.repository import ContractTypeRepository
from sqlalchemy.exc import IntegrityError

class ContractTypeService:
    @staticmethod
    def list_contract_types():
        """Lista todos los tipos de contrato."""
        return ContractTypeRepository.get_all()
    
    @staticmethod
    def get_contract_type(contract_type_id):
        """Obtiene un tipo de contrato por ID, lanza error si no existe."""
        contract_type = ContractTypeRepository.get_by_id(contract_type_id)
        if not contract_type:
            # Lanzamos ValueError para que el Resource lo convierta en 404
            raise ValueError(f"Tipo de contrato con ID {contract_type_id} no encontrado.")
        return contract_type

    @staticmethod
    def create_contract_type(name):
        """Crea un nuevo tipo de contrato con validación de nombre."""
        if not name:
            raise ValueError("El nombre del tipo de contrato no puede estar vacío.")
        try:
            return ContractTypeRepository.create(name=name)
        except IntegrityError:
            # Maneja el caso de que el 'name' sea UNIQUE y ya exista
            raise ValueError(f"Ya existe un tipo de contrato con el nombre '{name}'.")

    @staticmethod
    def update_contract_type(contract_type_id, new_name):
        """Actualiza el nombre de un tipo de contrato."""
        contract_type = ContractTypeService.get_contract_type(contract_type_id) # Valida existencia primero
        
        if not new_name:
            raise ValueError("El nuevo nombre del tipo de contrato no puede estar vacío.")
            
        try:
            return ContractTypeRepository.update(contract_type, new_name=new_name)
        except IntegrityError:
            raise ValueError(f"Ya existe un tipo de contrato con el nombre '{new_name}'.")

    @staticmethod
    def delete_contract_type(contract_type_id):
        """Elimina un tipo de contrato por ID."""
        contract_type = ContractTypeService.get_contract_type(contract_type_id) # Valida existencia primero
        ContractTypeRepository.delete(contract_type)