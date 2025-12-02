from flask_restx import Namespace, Resource, fields
from flask import request
from Modulos.others.generos.service import GenderService


genero_ns = Namespace('genero', description='Género operations')

# Definición del modelo (schema) para las entradas y salidas de datos
gender_model = genero_ns.model('Gender', {
    'id': fields.Integer(readOnly=True, description='Identificador único del género'),
    'name': fields.String(required=True, description='Nombre del género', example='Femenino')
})


# --- Resource para LISTAR (GET) y CREAR (POST) ---
@genero_ns.route('/') # Usar solo '/' si 'genero' ya está en el Namespace
class GenderList(Resource):
    
    @genero_ns.doc('list_genders')
    @genero_ns.marshal_list_with(gender_model, envelope='data')
    def get(self):
        """Lista todos los géneros"""
        try:
            data = GenderService.list_genders()
            return data, 200
        except Exception as e:
            genero_ns.abort(500, message=f'Error al obtener géneros: {str(e)}')
            
    @genero_ns.doc('create_gender')
    @genero_ns.expect(gender_model)
    @genero_ns.marshal_with(gender_model, code=201)
    def post(self):
        """Crea un nuevo género"""
        try:
            data = request.json
            if not data or 'name' not in data:
                 genero_ns.abort(400, message='Falta el campo "name" en el cuerpo de la solicitud.')

            new_gender = GenderService.create_gender(name=data['name'])
            return new_gender, 201
        except ValueError as e:
            # Errores de validación del servicio (ej. nombre duplicado o vacío)
            genero_ns.abort(409, message=str(e)) # 409 Conflict
        except Exception as e:
            genero_ns.abort(500, message=f'Error al crear género: {str(e)}')


# --- Resource para OBTENER, EDITAR y ELIMINAR un ítem específico ---
@genero_ns.route('/<int:gender_id>')
@genero_ns.param('gender_id', 'El identificador del género')
class GenderItem(Resource):
    
    @genero_ns.doc('get_gender')
    @genero_ns.marshal_with(gender_model)
    def get(self, gender_id):
        """Obtiene detalles de un género específico"""
        try:
            gender = GenderService.get_gender(gender_id)
            return gender, 200
        except ValueError as e:
            genero_ns.abort(404, message=str(e)) # 404 Not Found
        except Exception as e:
            genero_ns.abort(500, message=f'Error al obtener género: {str(e)}')
            
    @genero_ns.doc('update_gender')
    @genero_ns.expect(gender_model)
    @genero_ns.marshal_with(gender_model)
    def put(self, gender_id):
        """Actualiza un género existente"""
        try:
            data = request.json
            if not data or 'name' not in data:
                 genero_ns.abort(400, message='Falta el campo "name" en el cuerpo de la solicitud.')

            updated_gender = GenderService.update_gender(gender_id, new_name=data['name'])
            return updated_gender, 200
        except ValueError as e:
            # Errores de validación (ej. no encontrado o nombre duplicado)
            status_code = 404 if 'no encontrado' in str(e) else 409
            genero_ns.abort(status_code, message=str(e))
        except Exception as e:
            genero_ns.abort(500, message=f'Error al actualizar género: {str(e)}')

    @genero_ns.doc('delete_gender')
    @genero_ns.response(204, 'Género eliminado exitosamente')
    def delete(self, gender_id):
        """Elimina un género específico"""
        try:
            GenderService.delete_gender(gender_id)
            return '', 204
        except ValueError as e:
            genero_ns.abort(404, message=str(e)) # 404 Not Found
        except Exception as e:
            genero_ns.abort(500, message=f'Error al eliminar género: {str(e)}')