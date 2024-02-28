from flask_sqlalchemy import SQLAlchemy

import datetime

db=SQLAlchemy()

# class Alumnos(db.Model):
#     __Tablename__='alumnos'
#     id=db.Column(db.Integer, primary_key=True)
#     nombre=db.Column(db.String(50))
#     apaterno=db.Column(db.String(50))
#     email=db.Column(db.String(50))
#     create_date=db.Column(db.DateTime, default=datetime.datetime.now)

class Empleados(db.Model):
    __Tablename__='empleados'
    id=db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(50))
    email=db.Column(db.String(50))
    telefono=db.Column(db.String(50))
    direccion=db.Column(db.String(200))
    sueldo=db.Column(db.Float(10))
    create_date=db.Column(db.DateTime, default=datetime.datetime.now)