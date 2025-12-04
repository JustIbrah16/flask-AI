from extensions import db
from Modulos.others.contratos.models import ContractType # Asegúrate de que esta importación sea correcta

class ContractTypeRepository:
    @staticmethod
    def get_all():
        """Obtiene todos los tipos de contrato."""
        return ContractType.query.all()
    
    @staticmethod
    def get_by_id(contract_type_id):
        """Obtiene un tipo de contrato por ID."""
        return ContractType.query.get(contract_type_id)

    @staticmethod
    def create(name):
        """Crea un nuevo tipo de contrato."""
        new_contract_type = ContractType(name=name)
        db.session.add(new_contract_type)
        db.session.commit()
        return new_contract_type

    @staticmethod
    def update(contract_type, new_name):
        """Actualiza el nombre de un tipo de contrato."""
        contract_type.name = new_name
        db.session.commit()
        return contract_type

    @staticmethod
    def delete(contract_type):
        """Elimina un tipo de contrato de la base de datos."""
        db.session.delete(contract_type)
        db.session.commit()