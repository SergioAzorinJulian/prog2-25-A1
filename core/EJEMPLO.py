import hashlib
import requests
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt
import requests
URL='http://127.0.0.1:5000'
TOKEN =None
r=requests.get('http://123.0.0.1.5000/')

def get_headers(auth_required=False):
    headers = {"Content-Type": "application/json"}
    if auth_required and TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    return headers


def iniciar_sesion():
    usuario = input("Usuario: ")
    contrasena = input("Contraseña: ")
    r=requests.get(f'{URL}/login?user=<usuario>&password=<contraseña>')
    print(r.status_code)
    print(r.text)





def registrarse():
    usuario = input("Usuario nuevo: ")
    contrasena = input("Contraseña: ")
    r=requests.post(f"{URL}/signup?user=<usuario>&password=<contrasena>")
    print(r.status_code)
    print(r.text)

def users_list():
    r = requests.get(f"{URL}/users", headers=get_headers(auth_required=True))
    print("Respuesta:", r.status_code, r.json())






























def menu():
    print("1. Iniciar sesión")
    print("2. Registrarse")
    print("3. Listar Users")





if __name__ == '__main__':
    while True:
        menu()
        opcion = input("Elige una opción: ")
        if opcion == "0":
            print("Adios......")
            break

        if opcion == "1":
            iniciar_sesion()

        if opcion == "2":
            registrarse()

        if opcion == "3":
            users_list()


        else:
            print("Opción no válida.")
