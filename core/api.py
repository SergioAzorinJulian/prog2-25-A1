from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from partida import Partida
from jugador import Jugador
from mysql_base import add_user_ranking, ver_ranking
from apscheduler.schedulers.background import BackgroundScheduler
import hashlib
import random
import pickle
import os

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "Yt7#qW9z!Kp3$VmL"
jwt = JWTManager(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PICKLE_DIR = os.path.join(BASE_DIR, 'pickle_files')
os.makedirs(PICKLE_DIR, exist_ok=True)

def pickle_path(filename: str) -> str:
    return os.path.join(PICKLE_DIR, filename)
#DATOS
users={}
buzon={}
partidas={}

### FUNCIONES ###
def id_partida() -> str:
    """
    Genera un identificador único para una nueva partida.

    Returns
    -------
    str
        Identificador único de la partida.
    """

    while True:
        n = random.randint(1,999)
        if n not in partidas.keys():
            n = str(n)
            return n
        else:
            continue

#GUARDADOS

def cargar_partidas():
    """
        Cargamos las partidas
    """
    try:
        with open(pickle_path('partidas.pkl'), 'rb') as f:
            partidas_nuevo = pickle.load(f)
        partidas.update(partidas_nuevo)
    except (EOFError, FileNotFoundError):
        with open(pickle_path('partidas.pkl'), 'wb') as f:
            pickle.dump(partidas, f)
    return 'Partidas obtenidas', 200


def cargar_jugadores():
    """
        Cargamos los jugadores

        """
    try:
        with open(pickle_path('jugadores.pkl'), 'rb') as f:
            users_nuevo = pickle.load(f)
        users.update(users_nuevo)
    except (EOFError, FileNotFoundError):
        with open(pickle_path('jugadores.pkl'), 'wb') as f:
            pickle.dump(users, f)
    return 'Jugadores obtenidos', 200


def cargar_buzones():
    """
        Cargamos los buzones (notificaciones)
        """
    try:
        with open(pickle_path('buzones.pkl'), 'rb') as f:
            buzones_nuevo = pickle.load(f)
        buzon.update(buzones_nuevo)
    except (EOFError, FileNotFoundError):
        with open(pickle_path('buzones.pkl'), 'wb') as f:
            pickle.dump(buzon, f)
    return 'Buzones obtenidos', 200

def guardar_jugadores():
    """
    Metemos en archivo pkl los jugadores
    """
    with open(pickle_path('jugadores.pkl'), 'wb') as f:
        pickle.dump(users, f)
    return 'Jugadores guardados', 200


def guardar_buzones():
    """
    Metemos en archivo pkl los buzones (notificaciones)
    """

    with open(pickle_path('buzones.pkl'), 'wb') as f:
        pickle.dump(buzon, f)
    return 'Buzones guardados', 200


#API
@app.route('/')
def kingdom_craft():
    """
    Endpoint raíz de la API.

    Returns
    -------
    str
        Mensaje de bienvenida.
    """

    return 'KINGDOM CRAFT'


#AUTENTICACIÓN
@app.route('/auth/signup', methods=['POST'])
def signup():
    """
    Registra un nuevo usuario en el sistema.

    Returns
    -------
    str
        Mensaje de éxito o error.
    int
        Código de estado HTTP.
    """

    user = request.args.get('user', '')
    if user in users:
        return f'Usuario {user} ya existe', 409
    else:
        password = request.args.get('password', '')
        hashed = hashlib.sha256(password.encode()).hexdigest()
        users[user] = {
            'hashed': hashed,
            'amigos': [],
            'solicitudes_enviadas': [],
            'solicitudes_recibidas': [],
            'partidas': [],
            'invitaciones_partida':[]
        }
        buzon[user] = []
        #Creamos un usuario en MYSQL:
        text_sql=add_user_ranking(user)
        return f'Usuario {user} registrado\n{text_sql}', 200


@app.route('/auth/login', methods=['GET'])
def login():
    """
    Autentifica a un usuario y retorna un token JWT si las credenciales son correctas.

    Returns
    -------
    str
        Token JWT o mensaje de error.
    int
        Código de estado HTTP.
    """

    print(partidas)
    user = request.args.get('user', '')

    password = request.args.get('password', '')
    hashed = hashlib.sha256(password.encode()).hexdigest()

    if user in users and users[user]['hashed'] == hashed:
        print(partidas)
        return create_access_token(identity=user), 200

    else:
        print(partidas)
        return f'Usuario o contraseña incorrectos', 401


#USUARIOS
### RANKING
@app.route('/users/ranking', methods=['GET'])
@jwt_required()
def ranking_global():
    """
    Devuelve el ranking global de usuarios.

    Returns
    -------
    list
        Lista de usuarios ordenados por ranking.
    int
        Código de estado HTTP.
    """

    ranking : list = ver_ranking()
    return jsonify(ranking), 200


### AMIGOS
@app.route('/users/friends', methods=['GET'])
@jwt_required()
def amigos():
    """
    Devuelve la lista de amigos del usuario autentificado.

    Returns
    -------
    list
        Lista de amigos.
    int
        Código de estado HTTP.
    """

    amigos = users[get_jwt_identity()]['amigos']
    return jsonify(amigos),200    


@app.route('/users/friend-requests', methods=['POST'])
@jwt_required()
def enviar_solicitud():
    """
    Envía una solicitud de amistad a otro usuario.

    Returns
    -------
    str
        Mensaje de éxito o error.
    int
        Código de estado HTTP.
    """

    id_solicitud = request.args.get('id_solicitud','')
    if id_solicitud in users:
        user = get_jwt_identity()
        if id_solicitud not in users[user]['solicitudes_recibidas']:
            users[user]['solicitudes_enviadas'].append(id_solicitud)
            users[id_solicitud]['solicitudes_recibidas'].append(user)
            buzon[id_solicitud].append({'mensaje': f'{user} quiere ser tu amigo','leido': False})
            return 'Solicitud enviada',200
        else:
            return f'{id_solicitud} ya quiere ser tu amigo'
    else:
        return 'Usuario no encontrado',404


@app.route('/users/friend-requests', methods=['GET'])
@jwt_required()
def solicitudes():
    """
    Devuelve la lista de solicitudes de amistad recibidas.

    Returns
    -------
    list
        Lista de usuarios que han enviado solicitud.
    int
        Código de estado HTTP.
    """
    solicitudes = users[get_jwt_identity()]['solicitudes_recibidas']
    return jsonify(solicitudes),200


@app.route('/users/friend-requests/<id>/accept', methods=['POST'])
@jwt_required()
def aceptar_solicitud(id):
    """
    Acepta una solicitud de amistad.

    Parameters
    ----------
    id : str
        Identificador del usuario que envió la solicitud.

    Returns
    -------
    str
        Mensaje de éxito.
    int
        Código de estado HTTP.
    """

    user = get_jwt_identity()
    users[user]['solicitudes_recibidas'].remove(id)
    users[user]['amigos'].append(id)
    users[id]['solicitudes_enviadas'].remove(user)
    users[id]['amigos'].append(user)
    buzon[id].append({'mensaje':f'{user} ahora es tu amigo','leido': False})
    return f'Ahora eres amigo de {id}',200


@app.route('/users/friend-requests/<id>/reject', methods=['POST'])
@jwt_required()
def rechazar_solicitud(id):
    """
    Rechaza una solicitud de amistad.

    Parameters
    ----------
    id : str
        Identificador del usuario que envió la solicitud.

    Returns
    -------
    str
        Mensaje de éxito.
    int
        Código de estado HTTP.
    """
    user = get_jwt_identity()
    users[user]['solicitudes_recibidas'].remove(id)
    users[id]['solicitudes_enviadas'].remove(user)
    buzon[id].append({'mensaje':f'{user} rechazo tu solicitud de amistad','leido': False})
    return 'Solicitud de amistad rechazada',200


### BUZÓN
@app.route('/users/mail/notificaciones', methods=['GET'])
@jwt_required()
def notificaciones():
    """
    Devuelve el número de notificaciones no leídas del usuario.

    Returns
    -------
    str
        Mensaje con el número de notificaciones.
    int
        Código de estado HTTP.
    """

    user = get_jwt_identity()

    notificaciones = 0

    for mensaje in buzon[user]:
        if mensaje['leido'] == False:
            notificaciones += 1
    return f'\nTienes {notificaciones} notificaciones nuevas',200


@app.route('/users/mail', methods=['PUT'])
@jwt_required()
def marcar_leido():
    """
    Marca todos los mensajes del buzón como leídos.

    Returns
    -------
    str
        Mensaje de confirmación.
    int
        Código de estado HTTP.
    """

    user = get_jwt_identity()
    for mensaje in buzon[user]:
        mensaje['leido'] = True
    return 'Mensajes marcados como leído',200



@app.route('/users/mail', methods=['GET'])
@jwt_required()
def ver_buzon():
    """
    Devuelve los mensajes no leídos del buzón del usuario.

    Returns
    -------
    list
        Lista de mensajes no leídos.
    int
        Código de estado HTTP.
    """

    user = get_jwt_identity()
    mensajes = []
    for mensaje in buzon[user]:
        if mensaje['leido'] == False:
            mensajes.append(mensaje['mensaje'])
    return jsonify(mensajes),200
#USUARIOS
#   GAMES
@app.route('/users/game_requests', methods=['GET'])
@jwt_required()
def invitaciones_privadas():
    """
    Devuelve las invitaciones a partidas privadas del usuario.

    Returns
    -------
    dict
        Diccionario de partidas privadas.
    int
        Código de estado HTTP.
    """

    user = get_jwt_identity()
    id_privadas = users[user]['invitaciones_partida']
    partidas_privadas = {key : str(value) for key,value in partidas.items() if key in id_privadas}
    return jsonify(partidas_privadas),200


@app.route('/users/my_games', methods=['GET'])
@jwt_required()
def mis_partidas():
    """
    Devuelve las partidas en las que participa el usuario.

    Returns
    -------
    dict
        Diccionario de partidas del usuario.
    int
        Código de estado HTTP.
    """

    user = get_jwt_identity()
    id_partidas_user = users[user]['partidas']
    partidas_user = {key : str(value) for key,value in partidas.items() if key in id_partidas_user}
    return jsonify(partidas_user),200


#PARTIDA
@app.route('/games',methods=['POST'])
@jwt_required()
def crear_partida():
    """
    Crea una nueva partida, pública o privada.

    Returns
    -------
    str
        Mensaje de éxito o error.
    int
        Código de estado HTTP.
    """

    user = get_jwt_identity()
    id = id_partida()
    parametros_partida = request.get_json()
    if parametros_partida['privada']:
        try:
            invitado = parametros_partida['invitado']
            buzon[invitado].append({'mensaje': f'{user} te ha invitado a una partida privada, aceptala desde tu perfil','leido':False})
            users[invitado]['invitaciones_partida'].append(id)
        except KeyError:
            return f'Usuario {invitado} no encontrado',404
        partidas[id] = Partida(id=id,privada=True,host=user)
    else:
        partidas[id] = Partida(id=id,host=user)
    partidas[id].inicializar_mapa(parametros_partida['size'],parametros_partida['terrenos'])
    partidas[id].add_jugador(user,parametros_partida['reino'])
    users[user]['partidas'].append(id)
    return f'Partida de id: {id} creada correctamente'

#GUARDADO PARTIDA
@app.route('/games/partidas.pkl',methods=['POST'])
def guardar_partidas():
    """
    Metemos en archivo pkl las partidas
    """

    with open(pickle_path('partidas.pkl'), 'wb') as f:
        pickle.dump(partidas, f)
    return 'Partidas guardadas', 200

@app.route('/games',methods=['GET'])
@jwt_required()
def partidas_publicas():
    """
    Devuelve las partidas públicas disponibles a las que el usuario puede unirse.

    Returns
    -------
    dict
        Diccionario de partidas públicas.
    int
        Código de estado HTTP.
    """

    user = get_jwt_identity()
    publicas = {key: str(value) for key, value in partidas.items() if not value.privada and value.estado == 'Esperando' and value.host != user}
    return jsonify(publicas),200


@app.route('/games/<id>/join',methods=['PUT'])
@jwt_required()
def unirse_partida(id):
    """
    Permite a un usuario unirse a una partida existente.

    Parameters
    ----------
    id : str
        Identificador de la partida.

    Returns
    -------
    str
        Mensaje de éxito o error.
    int
        Código de estado HTTP.
    """

    user = get_jwt_identity()
    reino = request.args.get('reino','')
    try:
        partidas[id].add_jugador(user,reino)
        host = partidas[id].host
        buzon[host].append({'mensaje':f'{user} se ha unido a tu partida de id: {id}','leido':False})
        if id in users[user]['invitaciones_partida']:
            users[user]['invitaciones_partida'].remove(id)
        users[user]['partidas'].append(id)
        return f'Te has unido ha partida: {id}',200
    except KeyError:
        return f'Partida {id} no encontrada',404


@app.route('/games/<id>/start',methods=['PUT'])
@jwt_required()
def iniciar_partida(id):
    """
    Inicializa una partida y notifica al jugador que comienza.

    Parameters
    ----------
    id : str
        Identificador de la partida.

    Returns
    -------
    str or None
        Mensaje de éxito o None si la partida no existe.
    int
        Código de estado HTTP.
    """

    try:
        jugador = partidas[id].inicializar_partida()
        buzon[jugador].append({'mensaje':f'Es tu turno! Partida: {id}','leido':False})
        return f'Partida {id} inicializada, comienza {jugador}',200
    except KeyError:
        return 'No se ha podido iniciar la partida',404


@app.route('/games/<id>/cancel',methods=['POST'])
@jwt_required()
def cancelar_partida(id):
    """
    Cancela una partida y notifica al host.

    Parameters
    ----------
    id : str
        Identificador de la partida.

    Returns
    -------
    str
        Mensaje de éxito o error.
    int
        Código de estado HTTP.
    """

    try:
        user = get_jwt_identity()
        partidas[id].cancelar_partida()
        users[user]['invitaciones_partida'].remove(id)
        host = partidas[id].host
        buzon[host].append({'mensaje':f'{user} ha cancelado tu invitación','leido':False})
        users[host]['partidas'].remove(id)
        del partidas[id]
        return f'Partida {id} cancelada con éxito',200
    except KeyError:
        return f'Partida {id} no encontrada',404


@app.route('/games/<id>/game_state',methods=['GET'])
@jwt_required()
def estado_partida(id):
    """
    Devuelve el estado actual de una partida.

    Parameters
    ----------
    id : str
        Identificador de la partida.

    Returns
    -------
    str
        Estado de la partida.
    int
        Código de estado HTTP.
    """

    try:
        estado = partidas[id].estado_partida()
        return estado, 200
    except KeyError:
        return 'Partida no encontrada', 404


@app.route('/games/<id>/player_state',methods=['GET'])
@jwt_required()
def estado_jugador(id):
    """
    Devuelve el estado del jugador autenticado en la partida.

    Parameters
    ----------
    id : str
        Identificador de la partida.

    Returns
    -------
    dict
        Estado del jugador.
    int
        Código de estado HTTP.
    """

    user = get_jwt_identity()
    return jsonify(partidas[id].estado_jugador(user)),200


#/games/<id>/player/
@app.route('/games/<id>/player/ver_zona',methods=['POST'])
@jwt_required()
def ver_zona(id):
    """
    Devuelve la información de una zona específica del mapa.

    Parameters
    ----------
    id : str
        Identificador de la partida.

    Returns
    -------
    dict
        Información de la zona o error.
    int
        Código de estado HTTP.
    """

    zona = request.get_json()
    zona = tuple(zona['zona'])
    if zona in partidas[id].mapa.regiones.keys():
        user = get_jwt_identity()
        jugador = partidas[id].jugadores[partidas[id].jugadores.index(user)]
        return jsonify(jugador.ver_zona(zona)),200
    else:
        return jsonify({'error': f'Zona {zona} no encontrada'}),404


@app.route('/games/<id>/player/ver_recursos',methods=['GET'])
@jwt_required()
def ver_recursos(id):
    """
    Devuelve los recursos del jugador autenticado en la partida.

    Parameters
    ----------
    id : str
        Identificador de la partida.

    Returns
    -------
    list
        Lista de recursos del jugador.
    int
        Código de estado HTTP.
    """
    user = get_jwt_identity()
    jugador = partidas[id].jugadores[partidas[id].jugadores.index(user)]

    return jsonify(jugador.ver_recursos()),200


@app.route('/games/<id>/player/ver_mapa',methods=['GET'])
@jwt_required()
def ver_mapa(id):
    """
    Devuelve la representación gráfica del mapa para el jugador autentificado.

    Parameters
    ----------
    id : str
        Identificador de la partida.

    Returns
    -------
    str
        Representación gráfica del mapa.
    int
        Código de estado HTTP.
    """
    user = get_jwt_identity()
    jugador = partidas[id].jugadores[partidas[id].jugadores.index(user)]
    mapa_grafico = jugador.mapa_grafico()
    return mapa_grafico, 200

@app.route('/games/<id>/player/cambiar_turno',methods=['PUT'])
@jwt_required()
def cambiar_turno(id):
    """
    Cambia el turno al siguiente jugador en la partida.

    Parameters
    ----------
    id : str
        Identificador de la partida.

    Returns
    -------
    str
        Mensaje de éxito.
    int
        Código de estado HTTP.
    """
    partida = partidas[id]
    partida.cambiar_turno()
    le_toca_a = partida.turno
    buzon[le_toca_a].append({'mensaje': f'Es tu turno! Partida: {id}','leido':False})
    return "Turno cambiado con éxito", 200


@app.route('/games/<id>/player/catalogos',methods=['GET'])
@jwt_required()
def catalogos(id):
    """
    Devuelve los catálogos de tropas y edificios disponibles para el jugador.

    Parameters
    ----------
    id : str
        Identificador de la partida.

    Returns
    -------
    dict
        Diccionario con catálogos y valores válidos.
    int
        Código de estado HTTP.
    """

    user = get_jwt_identity()
    jugador = partidas[id].jugadores[partidas[id].jugadores.index(user)]
    catalogos_dict = {}
    valores_validos_tropas, catalogo_tropas = jugador.mostrar_catalogo()
    valores_validos_edificios, catalogo_edificios = jugador.mostrar_catalogo_edificios()
    catalogos_dict['tropas'] = {
        'valores_validos' : valores_validos_tropas,
        'catalogo' : catalogo_tropas
    }
    catalogos_dict['edificios'] = {
        'valores_validos' : valores_validos_edificios,
        'catalogo' : catalogo_edificios
    }
    return jsonify(catalogos_dict),200


@app.route('/games/<id>/player/add_tropa',methods=['POST'])
@jwt_required()
def add_tropa(id):
    """
    Añade una tropa al jugador en la partida.

    Parameters
    ----------
    id : str
        Identificador de la partida.

    Returns
    -------
    str
        Mensaje de éxito o error.
    int
        Código de estado HTTP.
    """

    user = get_jwt_identity()
    tropa_dict = request.get_json()
    jugador : Jugador = partidas[id].jugadores[partidas[id].jugadores.index(user)]
    salida = jugador.add_tropa(tropa_dict['tropa'],tropa_dict['cantidad'])
    return salida, 200


@app.route('/games/<id>/player/mover_tropa',methods=['PUT'])
@jwt_required()
def mover_tropa(id):
    """
    Mueve una tropa a otra región del mapa.

    Parameters
    ----------
    id : str
        Identificador de la partida.

    Returns
    -------
    dict
        Mensaje de éxito o error.
    int
        Código de estado HTTP.
    """

    user = get_jwt_identity()
    tropa_dict = request.get_json()
    jugador : Jugador = partidas[id].jugadores[partidas[id].jugadores.index(user)]
    salida = jugador.mover_tropa(tuple(tropa_dict['destino']),tropa_dict['tropa'],tropa_dict['cantidad'])
    return jsonify(salida), 200


@app.route('/games/<id>/player/mover_batallon',methods=['PUT'])
@jwt_required()
def mover_batallon(id):
    """
    Mueve un batallón completo a otra región del mapa.

    Parameters
    ----------
    id : str
        Identificador de la partida.

    Returns
    -------
    dict
        Mensaje de éxito o error.
    int
        Código de estado HTTP.
    """

    user = get_jwt_identity()
    destino_dict = request.get_json()
    jugador : Jugador = partidas[id].jugadores[partidas[id].jugadores.index(user)]
    salida = jugador.mover_batallon(tuple(destino_dict['destino']))
    return jsonify(salida), 200


@app.route('/games/<id>/player/edificio',methods=['POST'])
@jwt_required()
def construir_edificio(id):
    """
    Construye un edificio en la región actual del jugador.

    Parameters
    ----------
    id : str
        Identificador de la partida.

    Returns
    -------
    str
        Mensaje de éxito o error.
    int
        Código de estado HTTP.
    """

    user = get_jwt_identity()
    edificio = request.get_json()
    jugador : Jugador = partidas[id].jugadores[partidas[id].jugadores.index(user)]
    salida = jugador.construir_edificio(edificio)
    return salida,200


@app.route('/games/<id>/player/edificio',methods=['PUT'])
@jwt_required()
def subir_nivel_edificio(id):
    """
    Sube el nivel de un edificio en la región actual del jugador.

    Parameters
    ----------
    id : str
        Identificador de la partida.

    Returns
    -------
    str
        Mensaje de éxito o error.
    int
        Código de estado HTTP.
    """

    user = get_jwt_identity()
    edificio = request.get_json()
    jugador : Jugador = partidas[id].jugadores[partidas[id].jugadores.index(user)]
    salida = jugador.subir_nivel_edificio(edificio)
    return salida,200
@app.route('/games/<id>/player/combatir',methods=['PUT'])
@jwt_required()
def combatir(id):
    """
    Realiza un combate entre dos regiones.

    Parameters
    ----------
    id : str
        Identificador de la partida.

    Returns
    -------
    dict
        Resultado del combate y estado de la partida.
    int
        Código de estado HTTP.
    """

    user = get_jwt_identity()
    parametros = request.get_json()
    salida = partidas[id].combatir(user,tuple(parametros['atacantes']),tuple(parametros['defensores']))
    salida_dict = {
        'texto': salida[0],
        'estado': salida[1]
    }
    return jsonify(salida_dict),200



scheduler = BackgroundScheduler() #Cada 10 min se guardarán los archivos.
scheduler.add_job(guardar_jugadores, 'interval', seconds=600)
scheduler.add_job(guardar_buzones, 'interval', seconds=600)
scheduler.start()

cargar_jugadores()
cargar_buzones()
cargar_partidas()

if __name__ == '__main__':
    app.run(debug=True)