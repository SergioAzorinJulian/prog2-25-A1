import hashlib
import requests
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt
import requests
URL='http://127.0.0.1:5000'
TOKEN =None



def iniciar_sesion():
    usuario = str(input("Usuario: "))
    contrasena = str(input("Contraseña: "))
    r=requests.get(f'{URL}/login?user=<usuario>&password=<contraseña>')
    print(r.status_code)
    print(r.text)





def registrarse():
    usuario = str(input("Usuario nuevo: "))
    contrasena = str(input("Contraseña: "))
    r=requests.post(f"{URL}/signup?user=<string:usuario>&password=<string:contrasena>")
    print(r.status_code)
    print(r.text)
































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




        else:
            print("Opción no válida.")
