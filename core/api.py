import hashlib
import secrets

from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt
import requests


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "contraseñajwt"
jwt = JWTManager(app)
@app.route('/')
def mensaje():
    return 'API Funcionando'




@app.route('/users', methods=['GET'])
def get_users():
    return list(users.keys()), 200


@app.route('/users/<string:id>', methods=['POST'])
def add_user(id):
    if id not in users:
        users[id] = request.args.get('value','')
        return f'Dato {id} añadido' ,200
    else:
        return f'El usuario ya existe' ,409


@app.route('/singup',methods=['POST'])
def signup():
    user=request.args.get('user','')
    if user in users:
        return f'El usuario ya existe' ,409
    else:
        password=request.args.get('password','')
        hashed=hashlib.sha256(password.encode()).hexdigest()
        users[user]=hashed
        return f'Usuario {user} registrado' ,200

@app.route('/login', methods=['GET'])
def login():
    user=request.args.get('user','')
    password=request.args.get('password','')
    hashed=hashlib.sha256(password.encode()).hexdigest()
    if user in users and users[user]==hashed:
        return create_access_token(identity=user),200
    else:
        return f'Usuario o contraseña incorrectos',401

if __name__ == '__main__':
     app.run(debug=True)

users={}