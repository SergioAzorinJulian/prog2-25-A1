from flask import Flask, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import hashlib
import mapa
app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this "super secret" to something else!
jwt = JWTManager(app)

users = {}
data = {}


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/data', methods=['GET'])
@jwt_required()
def get_data():
    return list(data.keys()), 200


@app.route('/data/<id>', methods=['GET'])
@jwt_required()
def get_data_id(id):
    try:
        return data[id], 200
    except KeyError:
        return f'Dato {id} No encontrado', 404


@app.route('/data/<id>', methods=['POST'])
@jwt_required()
def add_data(id):
    if id not in data:
        data[id] = request.args.get('value', '')
        return f'Dato {id} añadido', 200
    else:
        return f'Dato {id} ya existe', 409


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