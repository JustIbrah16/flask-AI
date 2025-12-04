from flask_restx import Namespace, Resource, fields
from flask import request
from Modulos.others.bancos.service import BankService

# NOTA: Corregida la variable del namespace a 'bank_ns' para consistencia
bank_ns = Namespace('banks', description='Bank operations') 

# Definición del modelo (schema) para las entradas y salidas de datos
bank_model = bank_ns.model('Bank', {
    'id': fields.Integer(readOnly=True, description='Identificador único del banco'),
    'name': fields.String(required=True, description='Nombre del banco', example='Banco de Colombia')
})

# --- Resource para LISTAR (GET) y CREAR (POST) ---
@bank_ns.route('/') # Usar solo '/' para la colección
class BankList(Resource):
    
    @bank_ns.doc('list_banks')
    @bank_ns.marshal_list_with(bank_model, envelope='data')
    def get(self):
        """Lista todos los bancos"""
        try:
            data = BankService.list_banks()
            return data, 200
        except Exception as e:
            bank_ns.abort(500, message=f'Error al obtener bancos: {str(e)}')
            
    @bank_ns.doc('create_bank')
    @bank_ns.expect(bank_model)
    @bank_ns.marshal_with(bank_model, code=201)
    def post(self):
        """Crea un nuevo banco"""
        try:
            data = request.json
            if not data or 'name' not in data:
                 bank_ns.abort(400, message='Falta el campo "name" en el cuerpo de la solicitud.')

            new_bank = BankService.create_bank(name=data['name'])
            return new_bank, 201
        except ValueError as e:
            # Errores de validación del servicio (ej. nombre duplicado o vacío)
            bank_ns.abort(409, message=str(e)) # 409 Conflict
        except Exception as e:
            bank_ns.abort(500, message=f'Error al crear banco: {str(e)}')


# --- Resource para OBTENER, EDITAR y ELIMINAR un ítem específico ---
@bank_ns.route('/<int:bank_id>')
@bank_ns.param('bank_id', 'El identificador del banco')
class BankItem(Resource):
    
    @bank_ns.doc('get_bank')
    @bank_ns.marshal_with(bank_model)
    def get(self, bank_id):
        """Obtiene detalles de un banco específico"""
        try:
            bank = BankService.get_bank(bank_id)
            return bank, 200
        except ValueError as e:
            bank_ns.abort(404, message=str(e)) # 404 Not Found
        except Exception as e:
            bank_ns.abort(500, message=f'Error al obtener banco: {str(e)}')
            
    @bank_ns.doc('update_bank')
    @bank_ns.expect(bank_model)
    @bank_ns.marshal_with(bank_model)
    def put(self, bank_id):
        """Actualiza un banco existente"""
        try:
            data = request.json
            if not data or 'name' not in data:
                 bank_ns.abort(400, message='Falta el campo "name" en el cuerpo de la solicitud.')

            updated_bank = BankService.update_bank(bank_id, new_name=data['name'])
            return updated_bank, 200
        except ValueError as e:
            # Errores de validación (ej. no encontrado o nombre duplicado)
            status_code = 404 if 'no encontrado' in str(e) else 409
            bank_ns.abort(status_code, message=str(e))
        except Exception as e:
            bank_ns.abort(500, message=f'Error al actualizar banco: {str(e)}')

    @bank_ns.doc('delete_bank')
    @bank_ns.response(204, 'Banco eliminado exitosamente')
    def delete(self, bank_id):
        """Elimina un banco específico"""
        try:
            BankService.delete_bank(bank_id)
            return '', 204
        except ValueError as e:
            bank_ns.abort(404, message=str(e)) # 404 Not Found
        except Exception as e:
            bank_ns.abort(500, message=f'Error al eliminar banco: {str(e)}')