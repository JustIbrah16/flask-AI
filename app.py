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
from Modulos.certificates.resources import certificates_ns


def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)

    # extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={
        r"/auth/*": {"origins": app.config['CORS_ORIGINS']},
        r"/employees/*": {"origins": app.config['CORS_ORIGINS']},
        r"/attendance/*": {"origins": app.config['CORS_ORIGINS']},
        r"/vacations/*": {"origins": app.config['CORS_ORIGINS']},
        r"/reports/*": {"origins": app.config['CORS_ORIGINS']},
    })

    # Flask-RESTX API
    api = Api(app, title="GH360 API", version="1.0", description="API Gestión Humana 360")

    # Registrar namespaces
    api.add_namespace(auth_ns, path="/auth")
    api.add_namespace(employees_ns, path="/employees")
    api.add_namespace(attendance_ns, path="/attendance")
    api.add_namespace(vacations_ns, path="/vacations")
    api.add_namespace(reports_ns, path="/reports")
    api.add_namespace(certificates_ns, path="/certificates")

    # CORS extra headers (global)
    @app.after_request
    def apply_cors(response):
        response.headers["Access-Control-Allow-Origin"] = "http://localhost:4200"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        return response

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
