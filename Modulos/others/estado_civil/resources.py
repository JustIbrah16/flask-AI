from flask_restx import Namespace, Resource, fields
from flask import request
from Modulos.others.estado_civil.service import MaritalStatusService


marital_status_ns = Namespace('marital_statuses', description='Marital Status operations')

# Definición del modelo (schema) para las entradas y salidas de datos
marital_status_model = marital_status_ns.model('MaritalStatus', {
    'id': fields.Integer(readOnly=True, description='Identificador único del estado civil'),
    'name': fields.String(required=True, description='Nombre del estado civil', example='Casado/a')
})


# --- Resource para LISTAR (GET) y CREAR (POST) ---
@marital_status_ns.route('/') # Usar solo '/' si 'marital_statuses' ya está en el Namespace
class MaritalStatusList(Resource):
    
    @marital_status_ns.doc('list_marital_statuses')
    @marital_status_ns.marshal_list_with(marital_status_model, envelope='data')
    def get(self):
        """Lista todos los estados civiles"""
        try:
            data = MaritalStatusService.list_marital_statuses()
            return data, 200
        except Exception as e:
            marital_status_ns.abort(500, message=f'Error al obtener estados civiles: {str(e)}')
            
    @marital_status_ns.doc('create_marital_status')
    @marital_status_ns.expect(marital_status_model)
    @marital_status_ns.marshal_with(marital_status_model, code=201)
    def post(self):
        """Crea un nuevo estado civil"""
        try:
            data = request.json
            if not data or 'name' not in data:
                 marital_status_ns.abort(400, message='Falta el campo "name" en el cuerpo de la solicitud.')

            new_status = MaritalStatusService.create_marital_status(name=data['name'])
            return new_status, 201
        except ValueError as e:
            # Errores de validación del servicio (ej. nombre duplicado o vacío)
            marital_status_ns.abort(409, message=str(e)) # 409 Conflict
        except Exception as e:
            marital_status_ns.abort(500, message=f'Error al crear estado civil: {str(e)}')


# --- Resource para OBTENER, EDITAR y ELIMINAR un ítem específico ---
@marital_status_ns.route('/<int:status_id>')
@marital_status_ns.param('status_id', 'El identificador del estado civil')
class MaritalStatusItem(Resource):
    
    @marital_status_ns.doc('get_marital_status')
    @marital_status_ns.marshal_with(marital_status_model)
    def get(self, status_id):
        """Obtiene detalles de un estado civil específico"""
        try:
            status = MaritalStatusService.get_marital_status(status_id)
            return status, 200
        except ValueError as e:
            marital_status_ns.abort(404, message=str(e)) # 404 Not Found
        except Exception as e:
            marital_status_ns.abort(500, message=f'Error al obtener estado civil: {str(e)}')
            
    @marital_status_ns.doc('update_marital_status')
    @marital_status_ns.expect(marital_status_model)
    @marital_status_ns.marshal_with(marital_status_model)
    def put(self, status_id):
        """Actualiza un estado civil existente"""
        try:
            data = request.json
            if not data or 'name' not in data:
                 marital_status_ns.abort(400, message='Falta el campo "name" en el cuerpo de la solicitud.')

            updated_status = MaritalStatusService.update_marital_status(status_id, new_name=data['name'])
            return updated_status, 200
        except ValueError as e:
            # Errores de validación (ej. no encontrado o nombre duplicado)
            status_code = 404 if 'no encontrado' in str(e) else 409
            marital_status_ns.abort(status_code, message=str(e))
        except Exception as e:
            marital_status_ns.abort(500, message=f'Error al actualizar estado civil: {str(e)}')

    @marital_status_ns.doc('delete_marital_status')
    @marital_status_ns.response(204, 'Estado civil eliminado exitosamente')
    def delete(self, status_id):
        """Elimina un estado civil específico"""
        try:
            MaritalStatusService.delete_marital_status(status_id)
            return '', 204
        except ValueError as e:
            marital_status_ns.abort(404, message=str(e)) # 404 Not Found
        except Exception as e:
            marital_status_ns.abort(500, message=f'Error al eliminar estado civil: {str(e)}')