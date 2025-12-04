from flask_restx import Namespace, Resource, fields
from flask import request
from Modulos.others.tallas.service import SizeService


sizes_ns = Namespace('sizes', description='Size operations')

# Definición del modelo (schema) para las entradas y salidas de datos
size_model = sizes_ns.model('Size', {
    'id': fields.Integer(readOnly=True, description='Identificador único de la talla'),
    'name': fields.String(required=True, description='Nombre de la talla', example='M')
})


# --- Resource para LISTAR (GET) y CREAR (POST) ---
@sizes_ns.route('/') # Usar solo '/' si 'sizes' ya está en el Namespace
class SizeList(Resource):
    
    @sizes_ns.doc('list_sizes')
    @sizes_ns.marshal_list_with(size_model, envelope='data')
    def get(self):
        """Lista todas las tallas"""
        try:
            data = SizeService.list_sizes()
            return data, 200
        except Exception as e:
            sizes_ns.abort(500, message=f'Error al obtener tallas: {str(e)}')
            
    @sizes_ns.doc('create_size')
    @sizes_ns.expect(size_model)
    @sizes_ns.marshal_with(size_model, code=201)
    def post(self):
        """Crea una nueva talla"""
        try:
            data = request.json
            if not data or 'name' not in data:
                 sizes_ns.abort(400, message='Falta el campo "name" en el cuerpo de la solicitud.')

            new_size = SizeService.create_size(name=data['name'])
            return new_size, 201
        except ValueError as e:
            # Errores de validación del servicio (ej. nombre duplicado o vacío)
            sizes_ns.abort(409, message=str(e)) # 409 Conflict
        except Exception as e:
            sizes_ns.abort(500, message=f'Error al crear talla: {str(e)}')


# --- Resource para OBTENER, EDITAR y ELIMINAR un ítem específico ---
@sizes_ns.route('/<int:size_id>')
@sizes_ns.param('size_id', 'El identificador de la talla')
class SizeItem(Resource):
    
    @sizes_ns.doc('get_size')
    @sizes_ns.marshal_with(size_model)
    def get(self, size_id):
        """Obtiene detalles de una talla específica"""
        try:
            size = SizeService.get_size(size_id)
            return size, 200
        except ValueError as e:
            sizes_ns.abort(404, message=str(e)) # 404 Not Found
        except Exception as e:
            sizes_ns.abort(500, message=f'Error al obtener talla: {str(e)}')
            
    @sizes_ns.doc('update_size')
    @sizes_ns.expect(size_model)
    @sizes_ns.marshal_with(size_model)
    def put(self, size_id):
        """Actualiza una talla existente"""
        try:
            data = request.json
            if not data or 'name' not in data:
                 sizes_ns.abort(400, message='Falta el campo "name" en el cuerpo de la solicitud.')

            updated_size = SizeService.update_size(size_id, new_name=data['name'])
            return updated_size, 200
        except ValueError as e:
            # Errores de validación (ej. no encontrado o nombre duplicado)
            status_code = 404 if 'no encontrada' in str(e) else 409
            sizes_ns.abort(status_code, message=str(e))
        except Exception as e:
            sizes_ns.abort(500, message=f'Error al actualizar talla: {str(e)}')

    @sizes_ns.doc('delete_size')
    @sizes_ns.response(204, 'Talla eliminada exitosamente')
    def delete(self, size_id):
        """Elimina una talla específica"""
        try:
            SizeService.delete_size(size_id)
            return '', 204
        except ValueError as e:
            sizes_ns.abort(404, message=str(e)) # 404 Not Found
        except Exception as e:
            sizes_ns.abort(500, message=f'Error al eliminar talla: {str(e)}')