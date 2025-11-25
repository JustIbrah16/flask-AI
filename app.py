from flask import Flask
from flask_restx import Api
from config import Config
from extensions import db, migrate, jwt, cors

# import namespaces
from Modulos.auth.routes import auth_ns
from Modulos.employees.resources import employees_ns
from Modulos.attendance.resources import attendance_ns
from Modulos.vacations.resources import vacations_ns
from Modulos.reports.resources import reports_ns


def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)

    # extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}})

    # API (Swagger)
    api = Api(app, version='1.0', title='HR Platform API', doc='/docs')

    # register namespaces
    api.add_namespace(auth_ns, path='/auth')
    api.add_namespace(employees_ns, path='/employees')
    api.add_namespace(attendance_ns, path='/attendance')
    api.add_namespace(vacations_ns, path='/vacations')
    api.add_namespace(reports_ns, path='/reports')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)