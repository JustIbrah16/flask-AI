from flask_restx import Namespace, Resource, fields
from flask import request
from Modulos.others.eps.service import EPSProviderService


eps_ns = Namespace('eps', description='EPS operations')

# Definición del modelo (schema) para las entradas y salidas de datos
eps_model = eps_ns.model('EPSProvider', {
    'id': fields.Integer(readOnly=True, description='Identificador único del proveedor EPS'),
    'name': fields.String(required=True, description='Nombre del proveedor EPS', example='Nueva EPS')
})


# --- Resource para LISTAR (GET) y CREAR (POST) ---
@eps_ns.route('/') # Usar solo '/' si 'eps' ya está en el Namespace
class EPSProviderList(Resource):
    
    @eps_ns.doc('list_eps_providers')
    @eps_ns.marshal_list_with(eps_model, envelope='data')
    def get(self):
        """Lista todos los proveedores EPS"""
        try:
            data = EPSProviderService.list_eps_providers()
            return data, 200
        except Exception as e:
            eps_ns.abort(500, message=f'Error al obtener EPS: {str(e)}')
            
    @eps_ns.doc('create_eps_provider')
    @eps_ns.expect(eps_model)
    @eps_ns.marshal_with(eps_model, code=201)
    def post(self):
        """Crea un nuevo proveedor EPS"""
        try:
            data = request.json
            if not data or 'name' not in data:
                 eps_ns.abort(400, message='Falta el campo "name" en el cuerpo de la solicitud.')

            new_eps = EPSProviderService.create_eps_provider(name=data['name'])
            return new_eps, 201
        except ValueError as e:
            # Errores de validación del servicio (ej. nombre duplicado o vacío)
            eps_ns.abort(409, message=str(e)) # 409 Conflict
        except Exception as e:
            eps_ns.abort(500, message=f'Error al crear EPS: {str(e)}')


# --- Resource para OBTENER, EDITAR y ELIMINAR un ítem específico ---
@eps_ns.route('/<int:eps_id>')
@eps_ns.param('eps_id', 'El identificador del proveedor EPS')
class EPSProviderItem(Resource):
    
    @eps_ns.doc('get_eps_provider')
    @eps_ns.marshal_with(eps_model)
    def get(self, eps_id):
        """Obtiene detalles de un proveedor EPS específico"""
        try:
            eps = EPSProviderService.get_eps_provider(eps_id)
            return eps, 200
        except ValueError as e:
            eps_ns.abort(404, message=str(e)) # 404 Not Found
        except Exception as e:
            eps_ns.abort(500, message=f'Error al obtener EPS: {str(e)}')
            
    @eps_ns.doc('update_eps_provider')
    @eps_ns.expect(eps_model)
    @eps_ns.marshal_with(eps_model)
    def put(self, eps_id):
        """Actualiza un proveedor EPS existente"""
        try:
            data = request.json
            if not data or 'name' not in data:
                 eps_ns.abort(400, message='Falta el campo "name" en el cuerpo de la solicitud.')

            updated_eps = EPSProviderService.update_eps_provider(eps_id, new_name=data['name'])
            return updated_eps, 200
        except ValueError as e:
            # Errores de validación (ej. no encontrado o nombre duplicado)
            status_code = 404 if 'no encontrado' in str(e) else 409
            eps_ns.abort(status_code, message=str(e))
        except Exception as e:
            eps_ns.abort(500, message=f'Error al actualizar EPS: {str(e)}')

    @eps_ns.doc('delete_eps_provider')
    @eps_ns.response(204, 'Proveedor EPS eliminado exitosamente')
    def delete(self, eps_id):
        """Elimina un proveedor EPS específico"""
        try:
            EPSProviderService.delete_eps_provider(eps_id)
            return '', 204
        except ValueError as e:
            eps_ns.abort(404, message=str(e)) # 404 Not Found
        except Exception as e:
            eps_ns.abort(500, message=f'Error al eliminar EPS: {str(e)}')