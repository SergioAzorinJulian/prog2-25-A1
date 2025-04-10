import hashlib
import secrets

from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt
import requests

URL='http://127.0.0.1:5000'
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "contraseñajwt"
jwt = JWTManager(app)
@app.route('/')
def mensaje():
    return 'API Funcionando'

@app.route('/')
@app.route('/singup',methods=['POST'])
def signup():

    user=request.args.get('user','')
    if user in users:
        return f'El usuario ya existe' ,409
    else:
        password=request.args.get('password','')

        users[user]=password
        return f'Usuario {user} registrado' ,200

@app.route('/login', methods=['GET'])
def login():
    user=request.args.get('user','')
    password=request.args.get('password','')

    if user in users and users[user]==password:
        return create_access_token(identity=user),200
    else:
        return f'Usuario o contraseña incorrectos',401

if __name__ == '__main__':
     app.run(debug=True)

users = {}