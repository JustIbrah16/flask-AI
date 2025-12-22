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
        try:
            data = request.get_json() or {}
            
            if not data.get('username') or not data.get('password'):
                return {
                    'message': 'Usuario y contraseña son requeridos',
                    'error': 'MISSING_FIELDS'
                }, 400
            
            user = AuthService.login(data.get('username'), data.get('password'))
            if not user:
                return {
                    'message': 'Credenciales inválidas',
                    'error': 'INVALID_CREDENTIALS'
                }, 401
            
            access_token = create_access_token(identity=user.id)
            if isinstance(access_token, bytes):
                access_token = access_token.decode('utf-8')
            temp_pass = user.temp_pass
            
            rol =  user.role_id
            if rol == 1:
                rol = 'admin'
            elif rol == 2:
                rol = 'agent'
            else:
                rol = 'employee'
            return {
                'message': 'Inicio de sesión exitoso',
                'access_token': access_token,
                'user_id': user.id,
                'username': user.username,
                'role': rol,
                'temp_pass': temp_pass
               
            }, 200
        except Exception as e:
            return {
                'message': 'Error en el inicio de sesión',
                'error': str(e)
            }, 500


@auth_ns.route('/verify')
class VerifyResource(Resource):
    @jwt_required()
    def get(self):
        """Verify token - returns user identity"""
        try:
            user_id = get_jwt_identity()
            return {
                'message': 'Token válido',
                'user_id': user_id
            }, 200
        except Exception as e:
            return {
                'message': 'Error al verificar el token',
                'error': str(e)
            }, 400


@auth_ns.route('/logout')
class LogoutResource(Resource):
    @jwt_required()
    def post(self):
        """Logout endpoint - invalidates token on client side"""
        try:
            return {
                'message': 'Sesión cerrada exitosamente'
            }, 200
        except Exception as e:
            return {
                'message': 'Error al cerrar sesión',
                'error': str(e)
            }, 400


@auth_ns.route('/forget-password')
class ForgetPasswordResource(Resource):
    @auth_ns.expect(auth_ns.model('ForgetPassword', {
        'email': fields.String(required=True, description='User email')
    }))
    def post(self):
        """Forget password endpoint - sends temporary password via email"""
        try:
            data = request.get_json() or {}
            email = data.get('email')
            if not email:
                return {
                    'message': 'El correo electrónico es requerido',
                    'error': 'MISSING_EMAIL'
                }, 400
            
            user = AuthService.forget_password(email)
            if not user:
                return {
                    'message': 'Usuario no encontrado o ya tiene una contraseña temporal activa',
                    'error': 'USER_NOT_FOUND_OR_TEMP_PASS_ACTIVE'
                }, 400
            
            return {
                'message': 'Se ha enviado una contraseña temporal a tu correo electrónico'
            }, 200
        except Exception as e:
            return {
                'message': 'Error al procesar la solicitud de recuperación de contraseña',
                'error': str(e)
            }, 500
