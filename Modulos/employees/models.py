from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from Modulos.roles.models import Role
from Modulos.others.areas.models import Area
from Modulos.others.arl.models import ARL
from Modulos.others.bancos.models import Bank
from Modulos.others.cargos.models import Position
from Modulos.others.ciudades.models import City
from Modulos.others.contratos.models import ContractType
from Modulos.others.eps.models import EPS
from Modulos.others.estado_civil.models import MaritalStatus
from Modulos.others.generos.models import Gender
from Modulos.others.proyectos.models import Project
from Modulos.others.tallas.models import Size
from Modulos.others.state_employe.models import StateEmploye



class Employee(db.Model):
    __tablename__ = 'employees'

    # Identificación
    id = db.Column(db.Integer, primary_key=True)
    identification = db.Column(db.BigInteger, unique=True)  # Identificación / número de empleado

    # Información Personal
    name = db.Column(db.String(120), nullable=False)
    date_of_birth = db.Column(db.Date)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.BigInteger)  # Teléfono

    # Dirección
    address = db.Column(db.String(255))
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'))
    city = db.relationship('City', backref='employees')

    # Información Laboral
    position_id = db.Column(db.Integer, db.ForeignKey('positions.id'))
    position = db.relationship('Position', backref='employees')
    area_id = db.Column(db.Integer, db.ForeignKey('areas.id'))
    area = db.relationship('Area', backref='employees')
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role = db.relationship('Role', backref='employees')

    # Contrato
    is_boss = db.Column(db.Integer, default=0)  
    boss_id = db.Column(db.Integer)
    contract_type_id = db.Column(db.Integer, db.ForeignKey('contract_types.id'))
    contract_type = db.relationship('ContractType', backref='employees')
    bank_id = db.Column(db.Integer, db.ForeignKey('banks.id'))
    bank = db.relationship('Bank', backref='employees')
    account_number = db.Column(db.BigInteger, unique=True)
    salary = db.Column(db.Float)

    # Información Adicional
    entry_date = db.Column(db.Date)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    project = db.relationship('Project', backref='employees')
    state_employe_id = db.Column(db.Integer, db.ForeignKey('state_employe.id'), default=1)
    state_employe = db.relationship('StateEmploye', backref='employees')
    gender_id = db.Column(db.Integer, db.ForeignKey('genders.id'))
    gender = db.relationship('Gender', backref='employees')
    shirt_size_id = db.Column(db.Integer, db.ForeignKey('sizes.id'))
    shirt_size = db.relationship('Size', foreign_keys=[shirt_size_id], backref='employees_size')
    pants_size = db.Column(db.Integer)
    shoes_size = db.Column(db.Integer)
    coat_size_id = db.Column(db.Integer, db.ForeignKey('sizes.id'))
    coat_size = db.relationship('Size', foreign_keys=[coat_size_id], backref='employees_coat')
    eps_id = db.Column(db.Integer, db.ForeignKey('eps_providers.id'))
    eps = db.relationship('EPS', backref='employees')
    arl_id = db.Column(db.Integer, db.ForeignKey('arl_providers.id'))
    arl = db.relationship('ARL', backref='employees')

    # Estudios
    studies = db.Column(db.Text)  # Información de estudios
    marital_status_id = db.Column(db.Integer, db.ForeignKey('marital_statuses.id'))
    marital_status = db.relationship('MaritalStatus', backref='employees')
    children = db.Column(db.Integer, default=0)

    # Sistema
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200))
    is_active = db.Column(db.Integer, default=1)  # 0: inactivo, 1: activo, 2: licencia
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    temp_pass = db.Column(db.Integer, default=1)  # Indica si la contraseña es temporal

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


    def to_dict(self):
        return {
            'id': self.id,
            'identification': self.identification,
            'name': self.name,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'city_id': self.city_id,
            'city': self.city.name if self.city else None,
            'position_id': self.position_id,
            'position': self.position.name if self.position else None,
            'area_id': self.area_id,
            'area': self.area.name if self.area else None,
            'role_id': self.role_id,
            'boss_id': self.boss_id,
            'contract_type_id': self.contract_type_id,
            'contract_type': self.contract_type.name if self.contract_type else None,
            'bank_id': self.bank_id,
            'bank': self.bank.name if self.bank else None,
            'account_number': self.account_number,
            'salary': self.salary,
            'entry_date': self.entry_date.isoformat() if self.entry_date else None,
            'project_id': self.project_id,
            'project': self.project.name if self.project else None,
            'state_employe_id': self.state_employe_id,
            'state_employe': self.state_employe.name if self.state_employe else None,
            'gender_id': self.gender_id,
            'gender': self.gender.name if self.gender else None,
            'shirt_size_id': self.shirt_size_id,
            'shirt_size': self.shirt_size.name if self.shirt_size else None,
            'pants_size': self.pants_size,
            'shoes_size': self.shoes_size,
            'coat_size_id': self.coat_size_id,
            'coat_size': self.coat_size.name if self.coat_size else None,
            'eps_id': self.eps_id,
            'eps': self.eps.name if self.eps else None,
            'arl_id': self.arl_id,
            'arl': self.arl.name if self.arl else None,
            'studies': self.studies,
            'marital_status_id': self.marital_status_id,
            'marital_status': self.marital_status.name if self.marital_status else None,
            'children': self.children,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'temp_pass': self.temp_pass
        }

