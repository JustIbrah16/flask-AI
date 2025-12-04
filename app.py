from flask import Flask
from flask_restx import Api
from config import Config
from extensions import db, migrate, jwt
from flask_cors import CORS

from Modulos.auth.routes import auth_ns
from Modulos.employees.resources import employees_ns
from Modulos.attendance.resources import attendance_ns
from Modulos.vacations.resources import vacations_ns
from Modulos.reports.resources import reports_ns
from Modulos.certificates.resources import certificates_ns
from Modulos.others.areas.resources import areas_ns         
from Modulos.others.arl.resources import arl_ns              
from Modulos.others.bancos.resources import bank_ns          
from Modulos.others.cargos.resources import cargos_ns        
from Modulos.others.ciudades.resources import cities_ns      
from Modulos.others.contratos.resources import contract_types_ns 
from Modulos.others.eps.resources import eps_ns              
from Modulos.others.estado_civil.resources import marital_status_ns 
from Modulos.others.generos.resources import genero_ns       
from Modulos.others.proyectos.resources import proyectos_ns  
from Modulos.others.tallas.resources import sizes_ns       


def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)

    # EXTENSIONS
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # CORS CONFIG
    CORS(app,
         resources={r"/*": {"origins": Config.CORS_ORIGINS}},
         supports_credentials=True)

    # CREAR LA API
    api = Api(app)

    # NAMESPACES
    api.add_namespace(auth_ns, path='/auth')
    api.add_namespace(employees_ns, path='/employees')
    api.add_namespace(attendance_ns, path='/attendance')
    api.add_namespace(vacations_ns, path='/vacations')
    api.add_namespace(reports_ns, path='/reports')
    api.add_namespace(certificates_ns, path='/certificates')
    api.add_namespace(areas_ns, path='/areas')
    api.add_namespace(arl_ns, path='/arl')
    api.add_namespace(bank_ns, path='/banks')
    api.add_namespace(cargos_ns, path='/positions') 
    api.add_namespace(cities_ns, path='/cities')
    api.add_namespace(contract_types_ns, path='/contract-types')
    api.add_namespace(eps_ns, path='/eps')
    api.add_namespace(marital_status_ns, path='/marital-statuses')
    api.add_namespace(genero_ns, path='/genders') 
    api.add_namespace(proyectos_ns, path='/projects')
    api.add_namespace(sizes_ns, path='/sizes')

    return app
