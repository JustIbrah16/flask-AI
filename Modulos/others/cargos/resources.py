from flask_restx import Namespace, Resource, fields
from flask import request
from Modulos.others.cargos.service import PositionService


cargos_ns = Namespace('cargos', description='Cargo operations')

# Definición del modelo (schema) para las entradas y salidas de datos
position_model = cargos_ns.model('Position', {
    'id': fields.Integer(readOnly=True, description='Identificador único del cargo'),
    'name': fields.String(required=True, description='Nombre del cargo', example='Gerente de Proyecto')
})


# --- Resource para LISTAR (GET) y CREAR (POST) ---
@cargos_ns.route('/') # Usar solo '/' si 'cargos' ya está en el Namespace
class PositionList(Resource):
    
    @cargos_ns.doc('list_positions')
    @cargos_ns.marshal_list_with(position_model, envelope='data')
    def get(self):
        """Lista todos los cargos"""
        try:
            data = PositionService.list_positions()
            return data, 200
        except Exception as e:
            cargos_ns.abort(500, message=f'Error al obtener cargos: {str(e)}')
            
    @cargos_ns.doc('create_position')
    @cargos_ns.expect(position_model)
    @cargos_ns.marshal_with(position_model, code=201)
    def post(self):
        """Crea un nuevo cargo"""
        try:
            data = request.json
            if not data or 'name' not in data:
                 cargos_ns.abort(400, message='Falta el campo "name" en el cuerpo de la solicitud.')

            new_position = PositionService.create_position(name=data['name'])
            return new_position, 201
        except ValueError as e:
            # Errores de validación del servicio (ej. nombre duplicado o vacío)
            cargos_ns.abort(409, message=str(e)) # 409 Conflict
        except Exception as e:
            cargos_ns.abort(500, message=f'Error al crear cargo: {str(e)}')


# --- Resource para OBTENER, EDITAR y ELIMINAR un ítem específico ---
@cargos_ns.route('/<int:position_id>')
@cargos_ns.param('position_id', 'El identificador del cargo')
class PositionItem(Resource):
    
    @cargos_ns.doc('get_position')
    @cargos_ns.marshal_with(position_model)
    def get(self, position_id):
        """Obtiene detalles de un cargo específico"""
        try:
            position = PositionService.get_position(position_id)
            return position, 200
        except ValueError as e:
            cargos_ns.abort(404, message=str(e)) # 404 Not Found
        except Exception as e:
            cargos_ns.abort(500, message=f'Error al obtener cargo: {str(e)}')
            
    @cargos_ns.doc('update_position')
    @cargos_ns.expect(position_model)
    @cargos_ns.marshal_with(position_model)
    def put(self, position_id):
        """Actualiza un cargo existente"""
        try:
            data = request.json
            if not data or 'name' not in data:
                 cargos_ns.abort(400, message='Falta el campo "name" en el cuerpo de la solicitud.')

            updated_position = PositionService.update_position(position_id, new_name=data['name'])
            return updated_position, 200
        except ValueError as e:
            # Errores de validación (ej. no encontrado o nombre duplicado)
            status_code = 404 if 'no encontrado' in str(e) else 409
            cargos_ns.abort(status_code, message=str(e))
        except Exception as e:
            cargos_ns.abort(500, message=f'Error al actualizar cargo: {str(e)}')

    @cargos_ns.doc('delete_position')
    @cargos_ns.response(204, 'Cargo eliminado exitosamente')
    def delete(self, position_id):
        """Elimina un cargo específico"""
        try:
            PositionService.delete_position(position_id)
            return '', 204
        except ValueError as e:
            cargos_ns.abort(404, message=str(e)) # 404 Not Found
        except Exception as e:
            cargos_ns.abort(500, message=f'Error al eliminar cargo: {str(e)}')