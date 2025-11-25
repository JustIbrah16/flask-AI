# package marker

from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import create_access_token
from Modulos.auth.service import AuthService


auth_ns = Namespace('auth', description='Auth operations')


login_model = auth_ns.model('Login', {
'username': fields.String(required=True),
'password': fields.String(required=True),
})


@auth_ns.route('/login')
class LoginResource(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        data = request.get_json() or {}
        user = AuthService.login(data.get('username'), data.get('password'))
        if not user:
            return {'msg': 'invalid credentials'}, 401
        access = create_access_token(identity=user.id)
        return {'access_token': access}, 200


@auth_ns.route('/profile')
class Profile(Resource):
    def get(self):
        return {'msg': 'profile endpoint (todo: protect with jwt_required)'}