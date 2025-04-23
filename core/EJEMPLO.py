import requests
import getpass
import os
from typing import *
import time
URL = 'http://127.0.0.1:5000'
token = ''

#------------FUNCIONES------------

def param(
        nombre: str,
        tipo: type,
        lon_min: int = 0,
        is_password: bool = False,
        valores_validos: Union[list, tuple, None] = None,
) -> Any:
    """
    Solicita un valor por consola para la variable indicada, validando su tipo y longitud mínima.
    """
    valido = False
    out = None
    while not valido:
        prompt = (
            f'{nombre} (Longitud mínima: {lon_min}): '
            if lon_min
            else f'{nombre}: '
        )
        entrada = getpass.getpass(prompt) if is_password else input(prompt)
        if len(entrada) < lon_min:
            print(f'Longitud menor que la requerida: {lon_min}')
            continue
        try:
            out = tipo(entrada)
        except (ValueError, TypeError):
            print('El tipo de dato no es válido.')
            continue
        if valores_validos and out not in valores_validos:
            print(f'La entrada {out} no está presente en las opciones válidas {valores_validos}')
            continue
        valido = True
    return out

def limpiar_pantalla():
    # Para Windows
    if os.name == 'nt':
        os.system('cls')
    # Para Unix/Linux/macOS
    else:
        os.system('clear')

def mostrar_texto(lista : list[str]):
    for texto in lista:
        if texto == None:
            continue
        else:
            for caracter in texto:
                print(caracter,end='',flush=True)
                time.sleep(0.1)
            print('\n',end='')

#------------REQUESTS------------

def create(id, value):
    global token
    r = requests.post(f'{URL}/data/{id}?value={value}', headers={'Authorization': 'Bearer ' + token})
    print(r.text)


def read(id):
    global token
    r = requests.get(f'{URL}/data/{id}', headers={'Authorization': 'Bearer ' + token})

    print(r.status_code)
    print(r.text)


def update(id, value):
    global token
    r = requests.put(f'{URL}/data/{id}?value={value}', headers={'Authorization': 'Bearer ' + token})
    print(r.status_code)
    print(r.text)


def singup(user, password):
    r = requests.post(f'{URL}/signup?user={user}&password={password}')
    return (r.text)


def login(user, password):
    global token
    r = requests.get(f'{URL}/login?user={user}&password={password}')
    token = r.text
    if r.status_code == 200:
        create(str(user), 'jugador')
        return True
    else:
        return False


def ver_zona(usuario,tupla):
    r = requests.get(f'{URL}/data/ver_zona/{usuario}?value={tupla}')
    print(r.text)
def ver_recursos(usuario):
    r = requests.get(f'{URL}/data/ver_recursos/{usuario}')
    return r.text
def mostrar_catalogo(usuario):
    r = requests.get(f'{URL}/data/ver_zona/catalogo/{usuario}')
    return r.text
def mostrar_catalogo_edificios(usuario):
    r = requests.get(f'{URL}/data/ver_zona/catalogo_edificios/{usuario}')
    return r.text
def add_tropa(usuario,tropa,cantidad):
    r = requests.post(f'{URL}/data/ver_zona/add_tropa/{usuario}?tropa={tropa}&cantidad={cantidad}')
    return r.text
def mover_tropa(usuario,tropa,cantidad,destino):
    r = requests.put(f'{URL}/data/ver_zona/mover_tropa/{usuario}?tropa={tropa}&cantidad={cantidad}&tupla={destino}')
    return r.text
def crear_edificio(usuario,edificio):
    r = requests.post(f'{URL}/data/ver_zona/crear_edificio/{usuario}?edificio={edificio}')
    return r.text

def menu():
    while True:
        print("\n=== MENU ===")

        print("1. REGISTRATE")
        print("2. INICIAR SESIÓN")
        print("3. Exit")

        choice = input('Elige una opción (1-3): ')


        if choice == '1':
            user = param("Usuario Nuevo: ",str,4)
            password = param("Contraseña: ",str,8,is_password=True)
            mostrar_texto([singup(user, password)])
            limpiar_pantalla()

        elif choice == '2':
            user = param("Usuario: ",str,4)
            password = param("Contraseña: ",str,8,is_password=True)
            limpiar_pantalla()
            if login(user, password):
                while True:
                    print('1. VER REGIÓN')
                    print('2. VER RECURSOS')
                    print('3. VOLVER')
                    choice = input('Elige una opción (1-2):')
                    if choice == '1':
                        tupla = input('Tupla: ')
                        ver_zona(user,tupla) #FALTA DEVOLVER TRUE PARA MOSTRAR MENU, TAMBIÉN COMPROBAR QUE ES TU ZONA PARA VER LAS OPCIONES
                        while True:
                            print('1. AÑADIR TROPA')
                            print('2. MOVER TROPA')
                            print('3.CREAR EDIFICIO')
                            print('4.VOLVER')
                            choice = input('Elige una opción (1-3):')
                            if choice == '1':
                                print(mostrar_catalogo(user))
                                tropa = input('Que tropa desea añadir???: ').lower()
                                cantidad = int(input('Que cantidad???: '))
                                print(add_tropa(user,tropa,cantidad))
                            elif choice =='2':
                                tropa = input('Que tropa desea mover???: ').lower()
                                cantidad = int(input('Que cantidad???: '))
                                tupla = input('Tupla destino: ')
                                print(mover_tropa(user,tropa,cantidad,tupla))
                            elif choice == '3':
                                print(mostrar_catalogo_edificios(user))
                                edificio = input('Que edificio desea crear???: ').lower()
                                print(crear_edificio(user,edificio))
                            elif choice == '4':
                                break

                    elif choice == '2':
                        print(ver_recursos(user))
                    elif choice == '3':
                        break
                    else:
                        print('Opción invalida')
        elif choice == '3':
            print("Saliendo...")
            break
        else:
            print("Opción invalida.")


if __name__ == '__main__':
    menu()
