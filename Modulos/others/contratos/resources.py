from flask_restx import Namespace, Resource, fields
from flask import request
from Modulos.others.contratos.service import ContractTypeService


contract_types_ns = Namespace('contract_types', description='Contract Type operations')

# Definición del modelo (schema) para las entradas y salidas de datos
contract_type_model = contract_types_ns.model('ContractType', {
    'id': fields.Integer(readOnly=True, description='Identificador único del tipo de contrato'),
    'name': fields.String(required=True, description='Nombre del tipo de contrato', example='Término Indefinido')
})


# --- Resource para LISTAR (GET) y CREAR (POST) ---
@contract_types_ns.route('/') # Usar solo '/' si 'contract_types' ya está en el Namespace
class ContractTypeList(Resource):
    
    @contract_types_ns.doc('list_contract_types')
    @contract_types_ns.marshal_list_with(contract_type_model, envelope='data')
    def get(self):
        """Lista todos los tipos de contrato"""
        try:
            data = ContractTypeService.list_contract_types()
            return data, 200
        except Exception as e:
            contract_types_ns.abort(500, message=f'Error al obtener tipos de contrato: {str(e)}')
            
    @contract_types_ns.doc('create_contract_type')
    @contract_types_ns.expect(contract_type_model)
    @contract_types_ns.marshal_with(contract_type_model, code=201)
    def post(self):
        """Crea un nuevo tipo de contrato"""
        try:
            data = request.json
            if not data or 'name' not in data:
                 contract_types_ns.abort(400, message='Falta el campo "name" en el cuerpo de la solicitud.')

            new_type = ContractTypeService.create_contract_type(name=data['name'])
            return new_type, 201
        except ValueError as e:
            # Errores de validación del servicio (ej. nombre duplicado o vacío)
            contract_types_ns.abort(409, message=str(e)) # 409 Conflict
        except Exception as e:
            contract_types_ns.abort(500, message=f'Error al crear tipo de contrato: {str(e)}')


# --- Resource para OBTENER, EDITAR y ELIMINAR un ítem específico ---
@contract_types_ns.route('/<int:contract_type_id>')
@contract_types_ns.param('contract_type_id', 'El identificador del tipo de contrato')
class ContractTypeItem(Resource):
    
    @contract_types_ns.doc('get_contract_type')
    @contract_types_ns.marshal_with(contract_type_model)
    def get(self, contract_type_id):
        """Obtiene detalles de un tipo de contrato específico"""
        try:
            contract_type = ContractTypeService.get_contract_type(contract_type_id)
            return contract_type, 200
        except ValueError as e:
            contract_types_ns.abort(404, message=str(e)) # 404 Not Found
        except Exception as e:
            contract_types_ns.abort(500, message=f'Error al obtener tipo de contrato: {str(e)}')
            
    @contract_types_ns.doc('update_contract_type')
    @contract_types_ns.expect(contract_type_model)
    @contract_types_ns.marshal_with(contract_type_model)
    def put(self, contract_type_id):
        """Actualiza un tipo de contrato existente"""
        try:
            data = request.json
            if not data or 'name' not in data:
                 contract_types_ns.abort(400, message='Falta el campo "name" en el cuerpo de la solicitud.')

            updated_type = ContractTypeService.update_contract_type(contract_type_id, new_name=data['name'])
            return updated_type, 200
        except ValueError as e:
            # Errores de validación (ej. no encontrado o nombre duplicado)
            status_code = 404 if 'no encontrado' in str(e) else 409
            contract_types_ns.abort(status_code, message=str(e))
        except Exception as e:
            contract_types_ns.abort(500, message=f'Error al actualizar tipo de contrato: {str(e)}')

    @contract_types_ns.doc('delete_contract_type')
    @contract_types_ns.response(204, 'Tipo de contrato eliminado exitosamente')
    def delete(self, contract_type_id):
        """Elimina un tipo de contrato específico"""
        try:
            ContractTypeService.delete_contract_type(contract_type_id)
            return '', 204
        except ValueError as e:
            contract_types_ns.abort(404, message=str(e)) # 404 Not Found
        except Exception as e:
            contract_types_ns.abort(500, message=f'Error al eliminar tipo de contrato: {str(e)}')