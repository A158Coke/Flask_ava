#models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime


db1 = SQLAlchemy()

factura_producto = Table('factura_producto', db1.Model.metadata,
    db1.Column('factura_id', db1.Integer, ForeignKey('factura.id')),
    db1.Column('producto_id', db1.Integer, ForeignKey('producto.id')),
    db1.Column('cantidad',db1.Integer)
)

albaran_producto = Table('albaran_producto', db1.Model.metadata,
    db1.Column('albaran_id', db1.Integer, ForeignKey('albaran.id')),
    db1.Column('producto_id', db1.Integer, ForeignKey('producto.id')),
    db1.Column('cantidad',db1.Integer)
)

class Producto(db1.Model):
    id = db1.Column(db1.Integer, primary_key=True)
    nombre = db1.Column(db1.String(100), nullable=False, unique=True)
    cantidad = db1.Column(db1.Integer, nullable=False)
    facturas = relationship('Factura', secondary=factura_producto, back_populates='productos')
    albaranes = relationship('Albaran', secondary=albaran_producto, back_populates='productos')

class Albaran(db1.Model):
    id = db1.Column(db1.Integer, primary_key=True)
    fecha = db1.Column(db1.DateTime, default=datetime.utcnow)
    productos = relationship('Producto', secondary=albaran_producto, back_populates='albaranes')

class Factura(db1.Model):
    id = db1.Column(db1.Integer, primary_key=True)
    fecha = db1.Column(db1.DateTime, default=datetime.utcnow)
    productos = relationship('Producto', secondary=factura_producto, back_populates='facturas')
