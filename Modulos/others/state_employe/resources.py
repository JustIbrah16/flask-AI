from flask_restx import Namespace, Resource, fields
from flask import request
from Modulos.others.state_employe.service import StateEmployeService

state_employes_ns = Namespace('state_employes', description='State Employee operations')

state_model = state_employes_ns.model('StateEmploye', {
    'id': fields.Integer(readOnly=True, description='Identificador único del estado'),
    'name': fields.String(required=True, description='Nombre del estado', example='Activo')
})


@state_employes_ns.route('/')
class StateList(Resource):
    @state_employes_ns.doc('list_states')
    @state_employes_ns.marshal_list_with(state_model, envelope='data')
    def get(self):
        try:
            data = StateEmployeService.list_items()
            return data, 200
        except Exception as e:
            state_employes_ns.abort(500, message=f'Error al obtener estados: {str(e)}')

    @state_employes_ns.doc('create_state')
    @state_employes_ns.expect(state_model)
    @state_employes_ns.marshal_with(state_model, code=201)
    def post(self):
        try:
            data = request.json
            if not data or 'name' not in data:
                state_employes_ns.abort(400, message='Falta el campo "name" en el cuerpo de la solicitud.')

            new_item = StateEmployeService.create_item(name=data['name'])
            return new_item, 201
        except ValueError as e:
            state_employes_ns.abort(409, message=str(e))
        except Exception as e:
            state_employes_ns.abort(500, message=f'Error al crear estado: {str(e)}')


@state_employes_ns.route('/<int:item_id>')
@state_employes_ns.param('item_id', 'El identificador del estado')
class StateItem(Resource):
    @state_employes_ns.doc('get_state')
    @state_employes_ns.marshal_with(state_model)
    def get(self, item_id):
        try:
            item = StateEmployeService.get_item(item_id)
            return item, 200
        except ValueError as e:
            state_employes_ns.abort(404, message=str(e))
        except Exception as e:
            state_employes_ns.abort(500, message=f'Error al obtener estado: {str(e)}')

    @state_employes_ns.doc('update_state')
    @state_employes_ns.expect(state_model)
    @state_employes_ns.marshal_with(state_model)
    def put(self, item_id):
        try:
            data = request.json
            if not data or 'name' not in data:
                state_employes_ns.abort(400, message='Falta el campo "name" en el cuerpo de la solicitud.')

            updated_item = StateEmployeService.update_item(item_id, new_name=data['name'])
            return updated_item, 200
        except ValueError as e:
            status_code = 404 if 'no encontrado' in str(e) or 'no encontrado' in str(e).lower() else 409
            state_employes_ns.abort(status_code, message=str(e))
        except Exception as e:
            state_employes_ns.abort(500, message=f'Error al actualizar estado: {str(e)}')

    @state_employes_ns.doc('delete_state')
    @state_employes_ns.response(204, 'Estado eliminado exitosamente')
    def delete(self, item_id):
        try:
            StateEmployeService.delete_item(item_id)
            return '', 204
        except ValueError as e:
            state_employes_ns.abort(404, message=str(e))
        except Exception as e:
            state_employes_ns.abort(500, message=f'Error al eliminar estado: {str(e)}')
