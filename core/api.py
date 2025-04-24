from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import hashlib

from jugador import Jugador
app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "Yt7#qW9z!Kp3$VmL"
jwt = JWTManager(app)

#DATOS
users={}
buzon={}
partidas={}
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
            'solicitudes_recibidas': []
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


if __name__ == '__main__':
    app.run(debug=True)
    