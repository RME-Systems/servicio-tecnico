from extensions import db, bcrypt
from datetime import datetime
from flask_login import UserMixin

class Rol(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(64), unique=True, nullable=False)

    usuarios = db.relationship('Usuario', backref='rol', lazy='dynamic')

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)

    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

    ordenes_asignadas = db.relationship('Orden', backref='tecnico', lazy='dynamic')

    def set_password(self, password):

        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):

        return bcrypt.check_password_hash(self.password_hash, password)

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    telefono = db.Column(db.String(20), index=True)
    email = db.Column(db.String(120))

    equipos = db.relationship('Equipo', backref='cliente', lazy='dynamic')

class Marca(db.Model):
    __tablename__ = 'marcas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)

    equipos = db.relationship('Equipo', backref='marca', lazy='dynamic')

class TipoEquipo(db.Model):
    __tablename__ = 'tipos_equipo'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)

    equipos = db.relationship('Equipo', backref='tipo_equipo', lazy='dynamic')

class Equipo(db.Model):
    __tablename__ = 'equipos'
    id = db.Column(db.Integer, primary_key=True)
    modelo = db.Column(db.String(100))
    serial = db.Column(db.String(100), unique=True, index=True)

    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    marca_id = db.Column(db.Integer, db.ForeignKey('marcas.id'), nullable=False)
    tipo_id = db.Column(db.Integer, db.ForeignKey('tipos_equipo.id'), nullable=False)

    ordenes = db.relationship('Orden', backref='equipo', lazy='dynamic')

class Estado(db.Model):
    __tablename__ = 'estados'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)

    ordenes = db.relationship('Orden', backref='estado', lazy='dynamic')

class Repuesto(db.Model):
    __tablename__ = 'repuestos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, index=True)
    stock = db.Column(db.Integer, default=0)
    precio = db.Column(db.Float, default=0.0)

class Orden(db.Model):
    __tablename__ = 'ordenes'
    id = db.Column(db.Integer, primary_key=True)
    fecha_ingreso = db.Column(db.DateTime, default=datetime.utcnow)
    problema_reportado = db.Column(db.Text, nullable=False)
    diagnostico_tecnico = db.Column(db.Text)

    equipo_id = db.Column(db.Integer, db.ForeignKey('equipos.id'), nullable=False)
    tecnico_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    estado_id = db.Column(db.Integer, db.ForeignKey('estados.id'), nullable=False)

    detalles = db.relationship('DetalleOrden', backref='orden', lazy='dynamic')

class DetalleOrden(db.Model):
    __tablename__ = 'detalles_orden'
    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer, default=1)
    precio_unitario = db.Column(db.Float)

    orden_id = db.Column(db.Integer, db.ForeignKey('ordenes.id'), nullable=False)
    repuesto_id = db.Column(db.Integer, db.ForeignKey('repuestos.id'), nullable=False)

    repuesto = db.relationship('Repuesto')