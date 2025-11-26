from extensions import db
from datetime import datetime
from Modulos.roles.models import Role


# Tablas maestras (plurales)
class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)

class Position(db.Model):
    __tablename__ = 'positions'  # cargos
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)

class ContractType(db.Model):
    __tablename__ = 'contract_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)

class Bank(db.Model):
    __tablename__ = 'banks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)

class Gender(db.Model):
    __tablename__ = 'genders'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

class Size(db.Model):
    __tablename__ = 'sizes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)

class Area(db.Model):
    __tablename__ = 'areas'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

class EPS(db.Model):
    __tablename__ = 'eps_providers'  # EPS = Empresa Promotora de Salud
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)

class MaritalStatus(db.Model):
    __tablename__ = 'marital_statuses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)


class Employee(db.Model):
    __tablename__ = 'employees'

    # Identificación
    id = db.Column(db.Integer, primary_key=True)
    identificacion = db.Column(db.BigInteger, unique=True)  # Identificación / número de empleado

    # Información Personal
    nombre = db.Column(db.String(120), nullable=False)
    fecha_nacimiento = db.Column(db.Date)
    correo = db.Column(db.String(120), unique=True)
    contacto = db.Column(db.BigInteger)  # Teléfono

    # Dirección
    direccion = db.Column(db.String(255))
    ciudad_id = db.Column(db.Integer, db.ForeignKey('cities.id'))
    ciudad = db.relationship('City', backref='employees')

    # Información Laboral
    cargo_id = db.Column(db.Integer, db.ForeignKey('positions.id'))
    cargo = db.relationship('Position', backref='employees')
    area_id = db.Column(db.Integer, db.ForeignKey('areas.id'))
    area = db.relationship('Area', backref='employees')
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role = db.relationship('Role', backref='employees')

    # Contrato
    jefe_inmediato = db.Column(db.String(120))
    tipo_contrato_id = db.Column(db.Integer, db.ForeignKey('contract_types.id'))
    tipo_contrato = db.relationship('ContractType', backref='employees')
    banco_id = db.Column(db.Integer, db.ForeignKey('banks.id'))
    banco = db.relationship('Bank', backref='employees')
    numero_cuenta_bancaria = db.Column(db.BigInteger, unique=True)
    salario = db.Column(db.Float)

    # Información Adicional
    fecha_ingreso = db.Column(db.Date)
    proyecto_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    proyecto = db.relationship('Project', backref='employees')
    estado = db.Column(db.String(20), default='activo')  # activo, inactivo, licencia
    genero_id = db.Column(db.Integer, db.ForeignKey('genders.id'))
    genero = db.relationship('Gender', backref='employees')
    camisa_id = db.Column(db.Integer, db.ForeignKey('sizes.id'))
    camisa = db.relationship('Size', foreign_keys=[camisa_id], backref='employees_camisa')
    pantalon = db.Column(db.Integer)
    zapatos = db.Column(db.Integer)
    abrigo_id = db.Column(db.Integer, db.ForeignKey('sizes.id'))
    abrigo = db.relationship('Size', foreign_keys=[abrigo_id], backref='employees_abrigo')
    eps_id = db.Column(db.Integer, db.ForeignKey('eps_providers.id'))
    eps = db.relationship('EPS', backref='employees')

    # Estudios
    estudios = db.Column(db.Text)  # Información de estudios
    estado_civil_id = db.Column(db.Integer, db.ForeignKey('marital_statuses.id'))
    estado_civil = db.relationship('MaritalStatus', backref='employees')
    hijos = db.Column(db.Integer, default=0)

    # Sistema
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200))
    is_active = db.Column(db.Integer, default=1)  # 0: inactivo, 1: activo, 2: licencia
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'identificacion': self.identificacion,
            'nombre': self.nombre,
            'fecha_nacimiento': self.fecha_nacimiento.isoformat() if self.fecha_nacimiento else None,
            'correo': self.correo,
            'contacto': self.contacto,
            'direccion': self.direccion,
            'ciudad_id': self.ciudad_id,
            'ciudad': self.ciudad.name if self.ciudad else None,
            'cargo_id': self.cargo_id,
            'cargo': self.cargo.name if self.cargo else None,
            'area_id': self.area_id,
            'area': self.area.name if self.area else None,
            'role_id': self.role_id,
            'jefe_inmediato': self.jefe_inmediato,
            'tipo_contrato_id': self.tipo_contrato_id,
            'tipo_contrato': self.tipo_contrato.name if self.tipo_contrato else None,
            'banco_id': self.banco_id,
            'banco': self.banco.name if self.banco else None,
            'numero_cuenta_bancaria': self.numero_cuenta_bancaria,
            'salario': self.salario,
            'fecha_ingreso': self.fecha_ingreso.isoformat() if self.fecha_ingreso else None,
            'proyecto_id': self.proyecto_id,
            'proyecto': self.proyecto.name if self.proyecto else None,
            'estado': self.estado,
            'genero_id': self.genero_id,
            'genero': self.genero.name if self.genero else None,
            'camisa_id': self.camisa_id,
            'camisa': self.camisa.name if self.camisa else None,
            'pantalon': self.pantalon,
            'zapatos': self.zapatos,
            'abrigo_id': self.abrigo_id,
            'abrigo': self.abrigo.name if self.abrigo else None,
            'eps_id': self.eps_id,
            'eps': self.eps.name if self.eps else None,
            'estudios': self.estudios,
            'estado_civil_id': self.estado_civil_id,
            'estado_civil': self.estado_civil.name if self.estado_civil else None,
            'hijos': self.hijos,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

