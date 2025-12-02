from flask_restx import Namespace, Resource, fields
from flask import request
from Modulos.others.areas.service import AreaService

areas_ns = Namespace('areas', description='Area operations')

# Definición del modelo (schema) para las entradas y salidas de datos
area_model = areas_ns.model('Area', {
    'id': fields.Integer(readOnly=True, description='Identificador único del área'),
    'name': fields.String(required=True, description='Nombre del área', example='Recursos Humanos')
})

# --- Resource para LISTAR (GET) y CREAR (POST) ---
@areas_ns.route('/') # Usar solo '/' para la colección si 'areas' ya está en el Namespace
class AreaList(Resource):
    @areas_ns.doc('list_areas')
    @areas_ns.marshal_list_with(area_model, envelope='data')
    def get(self):
        """Lista todas las áreas"""
        try:
            data = AreaService.list_areas()
            return data, 200
        except Exception as e:
            areas_ns.abort(500, message=f'Error al obtener áreas: {str(e)}')

    @areas_ns.doc('create_area')
    @areas_ns.expect(area_model)
    @areas_ns.marshal_with(area_model, code=201)
    def post(self):
        """Crea una nueva área"""
        try:
            data = request.json
            if not data or 'name' not in data:
                 areas_ns.abort(400, message='Falta el campo "name" en el cuerpo de la solicitud.')

            new_area = AreaService.create_area(name=data['name'])
            return new_area, 201
        except ValueError as e:
            # Errores de validación del servicio (ej. nombre duplicado o vacío)
            areas_ns.abort(409, message=str(e)) # 409 Conflict o 400 Bad Request
        except Exception as e:
            areas_ns.abort(500, message=f'Error al crear área: {str(e)}')


# --- Resource para OBTENER, EDITAR y ELIMINAR un ítem específico ---
@areas_ns.route('/<int:area_id>')
@areas_ns.param('area_id', 'El identificador del área')
class AreaItem(Resource):
    @areas_ns.doc('get_area')
    @areas_ns.marshal_with(area_model)
    def get(self, area_id):
        """Obtiene detalles de un área específica"""
        try:
            area = AreaService.get_area(area_id)
            return area, 200
        except ValueError as e:
            areas_ns.abort(404, message=str(e)) # 404 Not Found
        except Exception as e:
            areas_ns.abort(500, message=f'Error al obtener área: {str(e)}')
            
    @areas_ns.doc('update_area')
    @areas_ns.expect(area_model)
    @areas_ns.marshal_with(area_model)
    def put(self, area_id):
        """Actualiza un área existente"""
        try:
            data = request.json
            if not data or 'name' not in data:
                 areas_ns.abort(400, message='Falta el campo "name" en el cuerpo de la solicitud.')

            updated_area = AreaService.update_area(area_id, new_name=data['name'])
            return updated_area, 200
        except ValueError as e:
            # Errores de validación (ej. no encontrado, nombre duplicado o vacío)
            status_code = 404 if 'no encontrada' in str(e) else 409
            areas_ns.abort(status_code, message=str(e))
        except Exception as e:
            areas_ns.abort(500, message=f'Error al actualizar área: {str(e)}')

    @areas_ns.doc('delete_area')
    @areas_ns.response(204, 'Área eliminada exitosamente')
    def delete(self, area_id):
        """Elimina un área específica"""
        try:
            AreaService.delete_area(area_id)
            return '', 204
        except ValueError as e:
            areas_ns.abort(404, message=str(e)) # 404 Not Found
        except Exception as e:
            areas_ns.abort(500, message=f'Error al eliminar área: {str(e)}')