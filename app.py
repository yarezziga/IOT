from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_expects_json import expects_json
from datetime import datetime, timezone
import os

app = Flask(__name__)
#Configura el SQLALCHEMY con Flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:SuperPWD@localhost/iot'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Crea objeto SQLALCHEMY
db = SQLAlchemy(app)
schema_parametros = {
    'type': 'object',
    'properties': {
        'unidades': {'type': 'string'},
        'alertaAlto': {'type': 'number'},
        'alertaBajo': {'type': 'number'},
        'valorMaximo': {'type': 'number'},
        'valorMinimo': {'type': 'number'},
        'nombre': {'type': 'string'}
    },
    'required': ['unidades', 'alertaAlto', 'alertaBajo', 'valorMaximo', 'valorMinimo', 'nombre']
}
schema_dispositivos = {
    'type': 'object',
    'properties': {
        'numSerie': {'type': 'string'},
        'dirMac': {'type': 'string'},
        'modelo': {'type': 'string'},
        'marcaDispositivo': {'type': 'string'},
        'marcaSensor': {'type': 'string'},
        'nivel': {'type': 'number'},
        'edificio': {'type': 'string'},
        'precision': {'type': 'number'},
        'oficina': {'type': 'string'},
    },
    'required': ['numSerie', 'dirMac', 'modelo', 'marcaDispositivo', 'marcaSensor', 'nivel', 'edificio', 'precision', 'oficina']
}


schema_mediciones = {
    'type': 'object',
    'properties': {
        'valor': {'type': 'number'},
        'idParametro': {'type': 'number'},
        'idDispositivo': {'type': 'number'},
    },
    'required': ['valor', 'idParametro', 'idDispositivo']
}


class Parametros(db.Model):
    idParametro = db.Column('idParametro', db.Integer, primary_key=True) # Id de Parametro
    unidades = db.Column('unidades', db.String(255), nullable=False)  
    alertaAlto = db.Column('alertaAlto', db.Float, nullable=False)
    alertaBajo = db.Column('alertaBajo', db.Float, nullable=False)
    valorMaximo = db.Column('valorMaximo', db.Float, nullable=False)
    valorMinimo = db.Column('valorMinimo', db.Float, nullable=False)
    nombre = db.Column('nombre', db.String(255), nullable=False)
    
    # Constructor.
    def init(self, unidades, alertaAlto, alertaBajo, valorMaximo, valorMinimo, nombre):
        self.unidades = unidades
        self.alertaAlto = alertaAlto
        self.alertaBajo = alertaBajo
        self.valorMaximo = valorMaximo
        self.valorMinimo = valorMinimo
        self.nombre = nombre


class Mediciones(db.Model):
    idMedicion = db.Column('idMedicion', db.Integer, primary_key=True) # Id de Medicion
    valor = db.Column('valor', db.Float, nullable=False) # Valor medidiod
    tsMedicion = db.Column('tsMedicion', db.DateTime(timezone=True),  default=datetime.utcnow)
    idParametro = db.Column('idParametro', db.Integer, nullable=False)
    idDispositivo = db.Column('idDispositivo', db.Integer, nullable=False)

    # Constructor.
    def init(self, valor, idMedicion, idParametro):
        self.idMedicion = idMedicion
        self.valor = valor
        self.idParametro = idParametro



class Dispositivo(db.Model):
    idDispositivo = db.Column('idDispositivo', db.Integer, primary_key = True)
    numSerie = db.Column('numSerie', db.String(255), nullable=False)
    dirMac = db.Column('dirMac', db.String(255), nullable=False)
    modelo = db.Column('modelo', db.String(255), nullable=False)
    marcaDispositivo = db.Column('marcaDispositivo', db.String(255), nullable=False)
    marcaSensor = db.Column('marcaSensor', db.String(255), nullable=False)
    nivel = db.Column('nivel', db.Integer, nullable=False)
    modelo = db.Column('modelo', db.String(255), nullable=False)
    edificio = db.Column('edificio', db.String(255), nullable=False)
    precision = db.Column('precision', db.Float, nullable=False)
    oficina = db.Column('oficina', db.String(255), nullable=False)

#Constructor
    def init(self, numSerie, dirMac, modelo, marcaDispositivo, marcaSensor, nivel, edificio, precision, oficina):
        self.numSerie = numSerie
        self.dirMac = dirMac
        self.marcaDispositivo = marcaDispositivo
        self.marcaSensor = marcaSensor
        self.nivel = nivel
        self.modelo = modelo
        self.edificio = edificio
        self.precision = precision
        self.oficina = oficina


db.create_all()


@app.route("/mediciones/agregar", methods=["POST"])
@expects_json(schema_mediciones)
def agregar_datos():
    content = request.json
    # Revisar idLocal 
    if (Parametros.query.get(content["idParametro"]) == None ):
        response = jsonify({"message": "idParametro no existe."})
        response.status_code = 401
        return response

    if (Dispositivo.query.get(content["idDispositivo"]) == None ):
        response = jsonify({"message": "idDispositivo no existe."})
        response.status_code = 401
        return response

    # Agregar nuevos datos.
     
    db.session.add(Mediciones( valor = content['valor'],
                               idParametro = content['idParametro'],
                               idDispositivo = content['idDispositivo']))
    db.session.commit()

    # Construir respuesta
    respuesta = jsonify({'message': 'Success Dispositivos Updated'})
    respuesta.status_code = 201
    return respuesta



@app.route("/parametros/agregar", methods=["POST"])
@expects_json(schema_parametros)
def parametros_agregar():
    content = request.json

    # Agregar nuevos datos. 
    db.session.add(Parametros( unidades = content['unidades'], 
                               alertaAlto = content['alertaAlto'], 
                               alertaBajo = content['alertaBajo'], 
                               valorMaximo = content['valorMaximo'], 
                               valorMinimo = content['valorMinimo'], 
                               nombre = content['nombre']))
    db.session.commit()

    # Construir respuesta
    respuesta = jsonify({'message': 'Success Parametros Updated'})
    respuesta.status_code = 201
    return respuesta




@app.route("/dispositivos/agregar", methods=["POST"])
@expects_json(schema_dispositivos)
def agregar_dispositivo():
    content = request.json

    # Agregar nuevos datos
    db.session.add(Dispositivo(
        numSerie = content['numSerie'],
        dirMac = content['dirMac'],
        marcaDispositivo = content['marcaDispositivo'],
        marcaSensor = content['marcaSensor'],
        nivel = content['nivel'],
        modelo = content['modelo'],
        edificio = content['edificio'],
        precision = content['precision'],
        oficina = content['oficina']))
    db.session.commit()

    # Construit respuesta
    respuesta = jsonify({'message': 'Success'})
    respuesta.status_code = 201
    return respuesta