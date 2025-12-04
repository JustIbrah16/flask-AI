from flask_restx import Namespace, Resource, fields
from flask import request
from Modulos.others.ciudades.service import CityService

cities_ns = Namespace('cities', description='City operations')

# Definición del modelo (schema) para las entradas y salidas de datos
city_model = cities_ns.model('City', {
    'id': fields.Integer(readOnly=True, description='Identificador único de la ciudad'),
    'name': fields.String(required=True, description='Nombre de la ciudad', example='Medellín')
})


# --- Resource para LISTAR (GET) y CREAR (POST) ---
@cities_ns.route('/') # Usar solo '/' si 'cities' ya está en el Namespace
class CityList(Resource):
    
    @cities_ns.doc('list_cities')
    @cities_ns.marshal_list_with(city_model, envelope='data')
    def get(self):
        """Lista todas las ciudades"""
        try:
            data = CityService.list_cities()
            return data, 200
        except Exception as e:
            cities_ns.abort(500, message=f'Error al obtener ciudades: {str(e)}')
            
    @cities_ns.doc('create_city')
    @cities_ns.expect(city_model)
    @cities_ns.marshal_with(city_model, code=201)
    def post(self):
        """Crea una nueva ciudad"""
        try:
            data = request.json
            if not data or 'name' not in data:
                 cities_ns.abort(400, message='Falta el campo "name" en el cuerpo de la solicitud.')

            new_city = CityService.create_city(name=data['name'])
            return new_city, 201
        except ValueError as e:
            # Errores de validación del servicio (ej. nombre duplicado o vacío)
            cities_ns.abort(409, message=str(e)) # 409 Conflict
        except Exception as e:
            cities_ns.abort(500, message=f'Error al crear ciudad: {str(e)}')


# --- Resource para OBTENER, EDITAR y ELIMINAR un ítem específico ---
@cities_ns.route('/<int:city_id>')
@cities_ns.param('city_id', 'El identificador de la ciudad')
class CityItem(Resource):
    
    @cities_ns.doc('get_city')
    @cities_ns.marshal_with(city_model)
    def get(self, city_id):
        """Obtiene detalles de una ciudad específica"""
        try:
            city = CityService.get_city(city_id)
            return city, 200
        except ValueError as e:
            cities_ns.abort(404, message=str(e)) # 404 Not Found
        except Exception as e:
            cities_ns.abort(500, message=f'Error al obtener ciudad: {str(e)}')
            
    @cities_ns.doc('update_city')
    @cities_ns.expect(city_model)
    @cities_ns.marshal_with(city_model)
    def put(self, city_id):
        """Actualiza una ciudad existente"""
        try:
            data = request.json
            if not data or 'name' not in data:
                 cities_ns.abort(400, message='Falta el campo "name" en el cuerpo de la solicitud.')

            updated_city = CityService.update_city(city_id, new_name=data['name'])
            return updated_city, 200
        except ValueError as e:
            # Errores de validación (ej. no encontrado o nombre duplicado)
            status_code = 404 if 'no encontrada' in str(e) else 409
            cities_ns.abort(status_code, message=str(e))
        except Exception as e:
            cities_ns.abort(500, message=f'Error al actualizar ciudad: {str(e)}')

    @cities_ns.doc('delete_city')
    @cities_ns.response(204, 'Ciudad eliminada exitosamente')
    def delete(self, city_id):
        """Elimina una ciudad específica"""
        try:
            CityService.delete_city(city_id)
            return '', 204
        except ValueError as e:
            cities_ns.abort(404, message=str(e)) # 404 Not Found
        except Exception as e:
            cities_ns.abort(500, message=f'Error al eliminar ciudad: {str(e)}')