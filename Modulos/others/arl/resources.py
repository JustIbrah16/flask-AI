from flask_restx import Namespace, Resource, fields
from flask import request
from Modulos.others.arl.service import ARLProviderService

# NOTA: El Namespace está en 'employees', quizás deberías cambiarlo a 'others' o 'arl'
arl_ns = Namespace('arl', description='ARL Provider operations') 

# Definición del modelo (schema) para las entradas y salidas de datos
arl_model = arl_ns.model('ARLProvider', {
    'id': fields.Integer(readOnly=True, description='Identificador único del proveedor ARL'),
    'name': fields.String(required=True, description='Nombre del proveedor ARL', example='Positiva')
})

# --- Resource para LISTAR (GET) y CREAR (POST) ---
@arl_ns.route('/') # Usar solo '/' para la colección
class ARLProviderList(Resource):
    
    @arl_ns.doc('list_arl_providers')
    @arl_ns.marshal_list_with(arl_model, envelope='data')
    def get(self):
        """Lista todos los proveedores ARL"""
        try:
            data = ARLProviderService.list_arl_providers()
            return data, 200
        except Exception as e:
            arl_ns.abort(500, message=f'Error al obtener ARLs: {str(e)}')
            
    @arl_ns.doc('create_arl_provider')
    @arl_ns.expect(arl_model)
    @arl_ns.marshal_with(arl_model, code=201)
    def post(self):
        """Crea un nuevo proveedor ARL"""
        try:
            data = request.json
            if not data or 'name' not in data:
                 arl_ns.abort(400, message='Falta el campo "name" en el cuerpo de la solicitud.')

            new_arl = ARLProviderService.create_arl_provider(name=data['name'])
            return new_arl, 201
        except ValueError as e:
            # Errores de validación del servicio (ej. nombre duplicado o vacío)
            arl_ns.abort(409, message=str(e)) # 409 Conflict
        except Exception as e:
            arl_ns.abort(500, message=f'Error al crear ARL: {str(e)}')


# --- Resource para OBTENER, EDITAR y ELIMINAR un ítem específico ---
@arl_ns.route('/<int:arl_id>')
@arl_ns.param('arl_id', 'El identificador del proveedor ARL')
class ARLProviderItem(Resource):
    
    @arl_ns.doc('get_arl_provider')
    @arl_ns.marshal_with(arl_model)
    def get(self, arl_id):
        """Obtiene detalles de un proveedor ARL específico"""
        try:
            arl = ARLProviderService.get_arl_provider(arl_id)
            return arl, 200
        except ValueError as e:
            arl_ns.abort(404, message=str(e)) # 404 Not Found
        except Exception as e:
            arl_ns.abort(500, message=f'Error al obtener ARL: {str(e)}')
            
    @arl_ns.doc('update_arl_provider')
    @arl_ns.expect(arl_model)
    @arl_ns.marshal_with(arl_model)
    def put(self, arl_id):
        """Actualiza un proveedor ARL existente"""
        try:
            data = request.json
            if not data or 'name' not in data:
                 arl_ns.abort(400, message='Falta el campo "name" en el cuerpo de la solicitud.')

            updated_arl = ARLProviderService.update_arl_provider(arl_id, new_name=data['name'])
            return updated_arl, 200
        except ValueError as e:
            # Errores de validación (ej. no encontrado o nombre duplicado)
            status_code = 404 if 'no encontrado' in str(e) else 409
            arl_ns.abort(status_code, message=str(e))
        except Exception as e:
            arl_ns.abort(500, message=f'Error al actualizar ARL: {str(e)}')

    @arl_ns.doc('delete_arl_provider')
    @arl_ns.response(204, 'Proveedor ARL eliminado exitosamente')
    def delete(self, arl_id):
        """Elimina un proveedor ARL específico"""
        try:
            ARLProviderService.delete_arl_provider(arl_id)
            return '', 204
        except ValueError as e:
            arl_ns.abort(404, message=str(e)) # 404 Not Found
        except Exception as e:
            arl_ns.abort(500, message=f'Error al eliminar ARL: {str(e)}')