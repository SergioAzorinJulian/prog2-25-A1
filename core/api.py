from flask import Flask, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import hashlib
import copy

from jugador import Jugador
from mapa import Mapa
from region import Region
from region_manager import RegionManager
from recursos import Recurso
from tropas import Tropa
from edificios import Edificio
from tropas import TropaAtaque, TropaDefensa, TropaAlcance, TropaEstructura

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "contraseña"
jwt = JWTManager(app)

users = {}
data = {}


diccionario = {
                key.lower(): value
                for key, value in globals().items()
                if isinstance(value, type) }


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/data', methods=['GET'])
@jwt_required()
def get_data():
    return list(data.keys()), 200


@app.route('/data/<id>', methods=['GET'])
def get_data_id(id):
    try:
        return data[id], 200
    except KeyError:
        return f'Dato {id} No encontrado', 404

def crear_mapa():
    """Crea el mapa por defecto y lo devuelve."""

    # Inicializar el mapa con 5 filas y 5 columnas
    map = Mapa(5, 5)

    # Crear nodos y conexiones
    nodos = map.crear_nodos()
    conexiones = map.crear_aristas(nodos)

    # Asignar terrenos a los nodos
    map.anyadir_terreno(conexiones)

    # Asignar zonas y generar recursos
    map.asigna_zonas()

    return map


@app.route('/data/<id>', methods=['POST'])
@jwt_required()
def add_data(id):
    global data
    global diccionario
    if id not in data:
        key = request.args.get('value', '')
        data[id] = diccionario[key](id, crear_mapa())

        return f'Sesión creada', 200
    else:
        return f' Ya existe la sesión', 409

@app.route('/data/ver_zona/<id>', methods=['GET'])
def ver_zona(id):
    global data
    jugador = data[id]
    posicion = request.args.get('value', '')
    x, y = map(int, posicion.split(','))
    cordenada = (x, y)
    regionstr = jugador.ver_zona(cordenada)
    return regionstr,200

@app.route('/data/ver_zona/add_tropa/<id>', methods=['POST'])
def add_tropas(id):
    global data
    jugador = data[id]
    tropa= request.args.get('tropa', '')
    cantidad= request.args.get('cantidad', '')
    resultado = jugador.add_tropa(tropa,cantidad)
    return resultado,200
@app.route('/data/ver_zona/catalogo/<id>', methods=['GET'])
def catalogo_tropas(id):
    global data
    jugador = data[id]
    catalogo = jugador.mostrar_catalogo()[1]
    return catalogo,200
@app.route('/data/<id>', methods=['PUT'])
@jwt_required()
def update_data(id):
    if id in data:
        data[id] = request.args.get('value', '')
        return f'Dato {id} actualizado', 200
    else:
        return f'Dato {id} No encontrado', 404


@app.route('/data/<id>', methods=['DELETE'])
@jwt_required()
def delete_data(id):
    if id in data:
        del data[id]
        return f'Dato {id} eliminado', 200
    else:
        return f'Dato {id} No encontrado', 404


@app.route('/signup', methods=['POST'])
def signup():
    user = request.args.get('user', '')
    if user in users:
        return f'Usuario {user} ya existe', 409
    else:
        password = request.args.get('password', '')
        hashed = hashlib.sha256(password.encode()).hexdigest()
        users[user] = hashed
        return f'Usuario {user} registrado', 200


@app.route('/login', methods=['GET'])
def login():
    user = request.args.get('user', '')
    password = request.args.get('password', '')
    hashed = hashlib.sha256(password.encode()).hexdigest()

    if user in users and users[user] == hashed:
        return create_access_token(identity=user), 200
    else:
        return f'Usuario o contraseña incorrectos', 401


if __name__ == '__main__':
    app.run(debug=True)
    