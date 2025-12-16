from flask_restx import Namespace, Resource, fields
from flask import request
from Modulos.roles.service import RoleService

roles_ns = Namespace('roles', description='roles related operations')

# Definición del modelo (schema) para las entradas y salidas de datos
role_model = roles_ns.model('Role', {
    'id': fields.Integer(readOnly=True, description='Identificador único del rol'),
    'name': fields.String(required=True, description='Nombre del rol', example='Administrador')
})

# --- Resource para LISTAR (GET) y CREAR (POST) ---
@roles_ns.route('/') # Usar solo '/' para la colección si 'roles' ya está en el Namespace
class RoleList(Resource):
    @roles_ns.doc('list_roles')
    @roles_ns.marshal_list_with(role_model, envelope='data')
    def get(self):
        """Lista todos los roles"""
        try:
            data = RoleService.list_roles()
            return data, 200
        except Exception as e:
            roles_ns.abort(500, message=f'Error al obtener roles: {str(e)}')

    @roles_ns.doc('create_role')
    @roles_ns.expect(role_model)
    @roles_ns.marshal_with(role_model, code=201)
    def post(self):
        """Crea un nuevo rol"""
        try:
            data = request.json
            if not data or 'name' not in data:
                 roles_ns.abort(400, message='Falta el campo "name" en el cuerpo de la solicitud.')
            new_role = RoleService.create_role(name=data['name'])
            return new_role, 201
        except ValueError as e:
            # Errores de validación del servicio (ej. nombre duplicado o vacío)
            roles_ns.abort(409, message=str(e)) # 409 Conflict o 400 Bad Request
        except Exception as e:
            roles_ns.abort(500, message=f'Error al crear rol: {str(e)}')


# --- Resource para OBTENER, EDITAR y ELIMINAR un ítem específico ---
@roles_ns.route('/<int:role_id>')
@roles_ns.param('role_id', 'El identificador del rol')
class RoleItem(Resource):
    @roles_ns.doc('get_role')
    @roles_ns.marshal_with(role_model)
    def get(self, role_id):
        """Obtiene detalles de un rol específico"""
        try:
            role = RoleService.get_role(role_id)
            return role, 200
        except ValueError as e:
            roles_ns.abort(404, message=str(e)) # 404 Not Found
        except Exception as e:
            roles_ns.abort(500, message=f'Error al obtener rol: {str(e)}')

    @roles_ns.doc('update_role')
    @roles_ns.expect(role_model)
    @roles_ns.marshal_with(role_model)
    def put(self, role_id):
        """Actualiza un rol existente"""
        try:
            data = request.json
            if not data or 'name' not in data:
                 roles_ns.abort(400, message='Falta el campo "name" en el cuerpo de la solicitud.')
            updated_role = RoleService.update_role(role_id, new_name=data['name'])
            return updated_role, 200
        except ValueError as e:
            # Errores de validación (ej. no encontrado, nombre duplicado o vacío)
            status_code = 404 if 'no encontrado' in str(e) else 409
            roles_ns.abort(status_code, message=str(e))
        except Exception as e:
            roles_ns.abort(500, message=f'Error al actualizar rol   : {str(e)}')

    @roles_ns.doc('delete_role')
    @roles_ns.response(204, 'Rol eliminado exitosamente')
    def delete(self, role_id):
        """Elimina un rol específico"""
        try:
            RoleService.delete_role(role_id)
            return '', 204
        except ValueError as e:
            roles_ns.abort(404, message=str(e)) # 404 Not Found
        except Exception as e:
            roles_ns.abort(500, message=f'Error al eliminar rol: {str(e)}')