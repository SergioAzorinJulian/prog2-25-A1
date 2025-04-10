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

def to_tuple():
    """
    Obtiene coordenadas del usuario a través de input y las convierte en una tupla.
    Maneja errores de formato y rango, y se mantiene en un bucle hasta que se ingrese un valor válido.

    Returns:
        tuple[int, int]: Una tupla con las coordenadas ingresadas por el usuario.
    """
    while True:
        try:
            entrada = input("Introduce las coordenadas (fila, columna): ")
            # Eliminar espacios en blanco al principio y al final y luego dividir la cadena por la coma
            entrada = entrada.strip()
            coordenadas_str = entrada.split(',')

            # Verificar que haya exactamente dos coordenadas
            if len(coordenadas_str) != 2:
                print("Error: Debes introducir dos coordenadas separadas por una coma.")
                continue  # Volver al inicio del bucle

            # Eliminar espacios en blanco alrededor de cada coordenada y convertir a entero
            fila = int(coordenadas_str[0].strip())
            columna = int(coordenadas_str[1].strip())

            return (fila, columna)

        except ValueError:
            print("Error: Las coordenadas deben ser números enteros.")
            continue  # Volver al inicio del bucle

@app.route('/data/<id>', methods=['POST'])
@jwt_required()
def add_data(id):
    global data
    global diccionario
    if id not in data:
        key = request.args.get('value', '')
        data[id] = diccionario[key](id, crear_mapa())

        return f'Dato {id} añadido', 200
    else:
        return f'Dato {id} ya existe', 409

@app.route('/data/ver_zona/<id>', methods=['GET'])
def ver_zona(id):
    global data
    jugador = data[id]
    posicion = request.args.get('value', '')
    x, y = map(int, posicion.split(','))
    cordenada = (x, y)
    return jugador.ver_zona(cordenada), 200


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


@app.route('/signin', methods=['GET'])
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
    