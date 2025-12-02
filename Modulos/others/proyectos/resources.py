from flask_restx import Namespace, Resource, fields
from flask import request
from Modulos.others.proyectos.service import ProjectService


proyectos_ns = Namespace('projects', description='Project operations')

# Definición del modelo (schema) para las entradas y salidas de datos
project_model = proyectos_ns.model('Project', {
    'id': fields.Integer(readOnly=True, description='Identificador único del proyecto'),
    'name': fields.String(required=True, description='Nombre del proyecto', example='Proyecto Alpha')
})


# --- Resource para LISTAR (GET) y CREAR (POST) ---
@proyectos_ns.route('/') 
class ProjectList(Resource):
    
    @proyectos_ns.doc('list_projects')
    @proyectos_ns.marshal_list_with(project_model, envelope='data')
    def get(self):
        """Lista todos los proyectos"""
        try:
            data = ProjectService.list_projects()
            return data, 200
        except Exception as e:
            proyectos_ns.abort(500, message=f'Error al obtener proyectos: {str(e)}')
            
    @proyectos_ns.doc('create_project')
    @proyectos_ns.expect(project_model)
    @proyectos_ns.marshal_with(project_model, code=201)
    def post(self):
        """Crea un nuevo proyecto"""
        try:
            data = request.json
            if not data or 'name' not in data:
                 proyectos_ns.abort(400, message='Falta el campo "name" en el cuerpo de la solicitud.')

            new_project = ProjectService.create_project(name=data['name'])
            return new_project, 201
        except ValueError as e:
            # Errores de validación del servicio (ej. nombre duplicado o vacío)
            proyectos_ns.abort(409, message=str(e)) # 409 Conflict
        except Exception as e:
            proyectos_ns.abort(500, message=f'Error al crear proyecto: {str(e)}')


# --- Resource para OBTENER, EDITAR y ELIMINAR un ítem específico ---
@proyectos_ns.route('/<int:project_id>')
@proyectos_ns.param('project_id', 'El identificador del proyecto')
class ProjectItem(Resource):
    
    @proyectos_ns.doc('get_project')
    @proyectos_ns.marshal_with(project_model)
    def get(self, project_id):
        """Obtiene detalles de un proyecto específico"""
        try:
            project = ProjectService.get_project(project_id)
            return project, 200
        except ValueError as e:
            proyectos_ns.abort(404, message=str(e)) # 404 Not Found
        except Exception as e:
            proyectos_ns.abort(500, message=f'Error al obtener proyecto: {str(e)}')
            
    @proyectos_ns.doc('update_project')
    @proyectos_ns.expect(project_model)
    @proyectos_ns.marshal_with(project_model)
    def put(self, project_id):
        """Actualiza un proyecto existente"""
        try:
            data = request.json
            if not data or 'name' not in data:
                 proyectos_ns.abort(400, message='Falta el campo "name" en el cuerpo de la solicitud.')

            updated_project = ProjectService.update_project(project_id, new_name=data['name'])
            return updated_project, 200
        except ValueError as e:
            # Errores de validación (ej. no encontrado o nombre duplicado)
            status_code = 404 if 'no encontrado' in str(e) else 409
            proyectos_ns.abort(status_code, message=str(e))
        except Exception as e:
            proyectos_ns.abort(500, message=f'Error al actualizar proyecto: {str(e)}')

    @proyectos_ns.doc('delete_project')
    @proyectos_ns.response(204, 'Proyecto eliminado exitosamente')
    def delete(self, project_id):
        """Elimina un proyecto específico"""
        try:
            ProjectService.delete_project(project_id)
            return '', 204
        except ValueError as e:
            proyectos_ns.abort(404, message=str(e)) # 404 Not Found
        except Exception as e:
            proyectos_ns.abort(500, message=f'Error al eliminar proyecto: {str(e)}')