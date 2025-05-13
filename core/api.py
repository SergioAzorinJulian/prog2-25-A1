from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import hashlib
import random
from partida import Partida
from jugador import Jugador
import pickle

from jugador import Jugador
app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "Yt7#qW9z!Kp3$VmL"
jwt = JWTManager(app)

#DATOS
users={}
buzon={}
partidas={}

### FUNCIONES ###
def id_partida() -> str:
    while True:
        n = random.randint(0,999)
        if n not in partidas.keys():
            n = str(n)
            return n
        else:
            continue
#API
@app.route('/')
def kingdom_craft():
    return 'KINGDOM CRAFT'
#AUTENTICACIÓN
@app.route('/auth/signup', methods=['POST'])
def signup():

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



        return f'Usuario {user} registrado', 200

@app.route('/auth/login', methods=['GET'])
def login():
    user = request.args.get('user', '')
    password = request.args.get('password', '')
    hashed = hashlib.sha256(password.encode()).hexdigest()

    if user in users and users[user]['hashed'] == hashed:
        return create_access_token(identity=user), 200
    else:
        return f'Usuario o contraseña incorrectos', 401

#USUARIOS
#   AMIGOS
@app.route('/users/friends', methods=['GET'])
@jwt_required()
def amigos():
    amigos = users[get_jwt_identity()]['amigos']
    return jsonify(amigos),200    

@app.route('/users/friend-requests', methods=['POST'])
@jwt_required()
def enviar_solicitud():
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
    solicitudes = users[get_jwt_identity()]['solicitudes_recibidas']
    return jsonify(solicitudes),200
   
@app.route('/users/friend-requests/<id>/accept', methods=['POST'])
@jwt_required()
def aceptar_solicitud(id):
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
    user = get_jwt_identity()
    users[user]['solicitudes_recibidas'].remove(id)
    users[id]['solicitudes_enviadas'].remove(user)
    buzon[id].append({'mensaje':f'{user} rechazo tu solicitud de amistad','leido': False})
    return 'Solicitud de amistad rechazada',200
#USUARIOS
#   BUZON
@app.route('/users/mail/notificaciones', methods=['GET'])
@jwt_required()
def notificaciones():
    user = get_jwt_identity()

    notificaciones = 0

    for mensaje in buzon[user]:
        if mensaje['leido'] == False:
            notificaciones += 1
    return f'\nTienes {notificaciones} notificaciones nuevas',200

@app.route('/users/mail', methods=['PUT'])
@jwt_required()
def marcar_leido():
    user = get_jwt_identity()
    for mensaje in buzon[user]:
        mensaje['leido'] = True
    return 'Mensajes marcados como leído',200

@app.route('/users/mail', methods=['GET'])
@jwt_required()
def ver_buzon():
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
    user = get_jwt_identity()
    id_privadas = users[user]['invitaciones_partida']
    partidas_privadas = {key : str(value) for key,value in partidas.items() if key in id_privadas}
    return jsonify(partidas_privadas),200
@app.route('/users/my_games', methods=['GET'])
@jwt_required()
def mis_partidas():
    user = get_jwt_identity()
    id_partidas_user = users[user]['partidas']
    partidas_user = {key : str(value) for key,value in partidas.items() if key in id_partidas_user}
    return jsonify(partidas_user),200
#PARTIDA
@app.route('/games',methods=['POST'])
@jwt_required()
def crear_partida():
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
@app.route('/games',methods=['GET'])
@jwt_required()
def partidas_publicas():
    user = get_jwt_identity()
    publicas = {key: str(value) for key, value in partidas.items() if not value.privada and value.estado == 'Esperando' and value.host != user}
    return jsonify(publicas),200

@app.route('/games/<id>/join',methods=['PUT'])
@jwt_required()
def unirse_partida(id):
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
def iniciar_partida(id): #Poner un mensaje al jugador que comienza el turno
    try:
        jugador = partidas[id].inicializar_partida()
        buzon[jugador].append({'mensaje':f'Es tu turno! Partida: {id}','leido':False})
        return f'Partida {id} inicializada, comienza {jugador}',200
    except KeyError:
        return None,404
@app.route('/games/<id>/cancel',methods=['POST'])
@jwt_required()
def cancelar_partida(id):
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
    try:
        estado = partidas[id].estado_partida()
        return estado, 200
    except KeyError:
        return 'Partida no encontrada', 404
@app.route('/games/<id>/player_state',methods=['GET'])
@jwt_required()
def estado_jugador(id):
    user = get_jwt_identity()
    return jsonify(partidas[id].estado_jugador(user)),200


#/games/<id>/player/
@app.route('/games/<id>/player/ver_zona',methods=['POST'])
@jwt_required()
def ver_zona(id):
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
    Gestiona la funcionalidad de cambio de turno para un juego específico identificado por su ID.
    Utiliza el metodo HTTP PUT y requiere autenticación JWT para garantizar que la solicitud esté autorizada.
    La función localiza la instancia del juego en el diccionario `partidas` usando el ID, cambia el turno
    utilizando el metodo `cambiar_turno` de la instancia del juego y proporciona una respuesta de éxito.

    Parameters
    ----------
    id : str
        El identificador único del juego cuyo turno necesita ser cambiado.

    Returns
    -------
    tuple
        Un mensaje de éxito y un código de estado HTTP 200 que indica que el turno se ha cambiado con éxito.
    """
    user = get_jwt_identity()
    jugador = partidas[id].jugadores[partidas[id].jugadores.index(user)]

    return jsonify(jugador.ver_recursos()),200

@app.route('/games/partidas.pkl',methods=['POST'])
@jwt_required()
def guardar_partidas():
    """
    Metemos en archivo pkl las partidas
    """
    with open('partidas.pkl', 'wb') as f:
        pickle.dump(partidas, f)
    return f'Partidas guardadas', 200


@app.route('/users/jugadores.pkl',methods=['POST'])
def guardar_jugadores():
    """
    Metemos en archivo pkl los jugadores
    """
    with open('jugadores.pkl', 'wb') as f:
        pickle.dump(users, f)
    return f'Jugadores guardados', 200

@app.route('/users/mail/buzones.pkl',methods=['POST'])
def guardar_buzones():
    """
    Metemos en archivo pkl los buzones (notificaciones)
    """

    with open('buzones.pkl', 'wb') as f:
        pickle.dump(buzon, f)
    return f'Buzones guardados', 200


@app.route('/games/partidas.pkl',methods=['GET'])
@jwt_required()
def obtener_partidas():
    """
        Cargamos las partidas
    """
    try:
        with open('partidas.pkl', 'rb') as f:
            partidas_nuevo=pickle.load(f)

        for keys in partidas_nuevo:
            users[keys]=partidas_nuevo[keys]
    except EOFError:
        with open('partidas.pkl', 'wb') as f:
            pickle.dump(partidas, f)

    return 'Partidas obtenidas', 200

@app.route('/users/jugadores.pkl',methods=['GET'])
def obtener_jugadores():
    """
        Cargamos los jugadores

        """
    try:
        with open('jugadores.pkl', 'rb') as f:
            users_nuevo=pickle.load(f)
        for keys in users_nuevo:
            users[keys] = users_nuevo[keys]
    except EOFError:
        with open('jugadores.pkl', 'wb') as f:
            pickle.dump(users, f)


    return 'Jugadores obtenidos', 200


@app.route('/users/mail/buzones.pkl',methods=['GET'])
def obtener_buzones():
    """
        Cargamos los buzones (notificaciones)
        """
    try:
        with open('buzones.pkl', 'rb') as f:
            buzon_nuevo=pickle.load(f)
        for keys in buzon_nuevo:
            buzon[keys] = buzon_nuevo[keys]
    except EOFError:
        with open('buzones.pkl', 'wb') as f:
            pickle.dump(buzon, f)


    return 'Buzones obtenidos', 200

@app.route('/games/<id>/player/ver_mapa',methods=['GET'])
@jwt_required()
def ver_mapa(id):
    """
    Recupera la representación gráfica del mapa para un jugador
    en una partida específica. Este endpoint está protegido y requiere
    un token JWT válido para acceder. Identifica al usuario autenticado,
    recupera su instancia de jugador correspondiente dentro de la partida
    y obtiene la representación gráfica del mapa del jugador.

    Parameters
    ----------
    id : str
        ID de la partida en la que está jugando el jugador.

    Returns
    -------
    tuple
        Una tupla que contiene la representación gráfica del mapa del jugador
        y el código de estado HTTP.
    """
    user = get_jwt_identity()
    jugador = partidas[id].jugadores[partidas[id].jugadores.index(user)]
    mapa_grafico = jugador.mapa_grafico()
    return mapa_grafico, 200

@app.route('/games/<id>/player/cambiar_turno',methods=['PUT'])
@jwt_required()
def cambiar_turno(id):
    """
    Gestiona la funcionalidad de cambio de turno para un juego específico identificado por su ID.
    Utiliza el metodo HTTP PUT y requiere autenticación JWT para garantizar que la solicitud esté autorizada.
    La función localiza la instancia del juego en el diccionario `partidas` usando el ID, cambia el turno
    utilizando el metodo `cambiar_turno` de la instancia del juego y proporciona una respuesta de éxito.

    Parameters
    ----------
    id : str
        El identificador único del juego cuyo turno necesita ser cambiado.

    Returns
    -------
    tuple
        Un mensaje de éxito y un código de estado HTTP 200 que indica que el turno se ha cambiado con éxito.
    """
    partida = partidas[id]
    partida.cambiar_turno()
    le_toca_a = partida.turno
    buzon[le_toca_a].append({'mensaje': f'Es tu turno! Partida: {id}','leido':False})
    return "Turno cambiado con éxito", 200
@app.route('/games/<id>/player/catalogos',methods=['GET'])
@jwt_required()
def catalogos(id):
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
    user = get_jwt_identity()
    tropa_dict = request.get_json()
    jugador : Jugador = partidas[id].jugadores[partidas[id].jugadores.index(user)]
    salida = jugador.add_tropa(tropa_dict['tropa'],tropa_dict['cantidad'])
    return salida, 200
@app.route('/games/<id>/player/mover_tropa',methods=['PUT'])
@jwt_required()
def mover_tropa(id):
    user = get_jwt_identity()
    tropa_dict = request.get_json()
    jugador : Jugador = partidas[id].jugadores[partidas[id].jugadores.index(user)]
    salida = jugador.mover_tropa(tuple(tropa_dict['destino']),tropa_dict['tropa'],tropa_dict['cantidad'])
    return jsonify(salida), 200
@app.route('/games/<id>/player/mover_batallon',methods=['PUT'])
@jwt_required()
def mover_batallon(id):
    user = get_jwt_identity()
    destino_dict = request.get_json()
    jugador : Jugador = partidas[id].jugadores[partidas[id].jugadores.index(user)]
    salida = jugador.mover_batallon(tuple(destino_dict['destino']))
    return jsonify(salida), 200
@app.route('/games/<id>/player/edificio',methods=['POST'])
@jwt_required()
def construir_edificio(id):
    user = get_jwt_identity()
    edificio = request.get_json()
    jugador : Jugador = partidas[id].jugadores[partidas[id].jugadores.index(user)]
    salida = jugador.construir_edificio(edificio)
    return salida,200
@app.route('/games/<id>/player/edificio',methods=['PUT'])
@jwt_required()
def subir_nivel_edificio(id):
    user = get_jwt_identity()
    edificio = request.get_json()
    jugador : Jugador = partidas[id].jugadores[partidas[id].jugadores.index(user)]
    salida = jugador.subir_nivel_edificio(edificio)
    return salida,200
@app.route('/games/<id>/player/combatir',methods=['PUT'])
@jwt_required()
def combatir(id):
    parametros = request.get_json()
    salida = partidas[id].combatir(tuple(parametros['atacantes']),tuple(parametros['defensores']))
    salida_dict = {
        'texto': salida[0],
        'estado': salida[1]
    }
    return jsonify(salida_dict),200


if __name__ == '__main__':
    app.run(debug=True)