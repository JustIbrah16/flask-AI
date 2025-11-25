from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from Modulos.auth.service import AuthService

auth_ns = Namespace('auth', description='Auth operations')

# Models
login_model = auth_ns.model('Login', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password'),
})

register_model = auth_ns.model('Register', {
    'username': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'phone': fields.String(required=False),
})

# Response models
login_response = auth_ns.model('LoginResponse', {
    'access_token': fields.String(description='JWT access token'),
    'user_id': fields.Integer(description='User ID'),
    'username': fields.String(description='Username'),
})

error_response = auth_ns.model('ErrorResponse', {
    'msg': fields.String(description='Error message'),
    'code': fields.String(description='Error code'),
})


@auth_ns.route('/login')
class LoginResource(Resource):
    @auth_ns.expect(login_model)
    @auth_ns.response(200, 'Success', login_response)
    @auth_ns.response(401, 'Unauthorized', error_response)
    @auth_ns.response(400, 'Bad Request', error_response)
    def post(self):
        """Login endpoint - returns JWT token"""
        data = request.get_json() or {}
        
        if not data.get('username') or not data.get('password'):
            return {'msg': 'Username and password are required', 'code': 'MISSING_FIELDS'}, 400
        
        user = AuthService.login(data.get('username'), data.get('password'))
        if not user:
            return {'msg': 'Invalid credentials', 'code': 'INVALID_CREDENTIALS'}, 401
        
        access_token = create_access_token(identity=user.id)
        return {
            'access_token': access_token,
            'user_id': user.id,
            'username': user.username
        }, 200


@auth_ns.route('/verify')
class VerifyResource(Resource):
    @jwt_required()
    def get(self):
        """Verify token - returns user identity"""
        user_id = get_jwt_identity()
        return {'user_id': user_id, 'msg': 'Token is valid'}, 200


@auth_ns.route('/logout')
class LogoutResource(Resource):
    @jwt_required()
    def post(self):
        """Logout endpoint - invalidates token on client side"""
        return {'msg': 'Successfully logged out'}, 200
