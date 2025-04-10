from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt
import requests


app = Flask(__name__)
@app.route('/')
def mensaje():
    return 'API Funcionando'

if __name__ == '__main__':
     app.run(debug=True)

users={}


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


