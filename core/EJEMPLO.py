import requests
import getpass
import os
from typing import *
import time
URL = 'http://127.0.0.1:5000'

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

def limpiar_pantalla() -> None:
    # Para Windows
    if os.name == 'nt':
        os.system('cls')
    # Para Unix/Linux/macOS
    else:
        os.system('clear')

def mostrar_texto(lista : list[str] | str,enumerado : bool = False) -> None:
    n = 1
    if isinstance(lista, str):
        lista = [lista]
    for texto in lista:
        if texto is None:
            continue
        else:
            if enumerado:
                num = f'{n}. '
                for letra in num:
                    print(letra, end='',flush=True)
                n += 1
            for caracter in texto:
                print(caracter,end='',flush=True)
                time.sleep(0.05)
            print('\n',end='')
            

#------------REQUESTS------------
# AUTENTICACIÓN
def signup(user, password):
    r = requests.post(f'{URL}/auth/signup?user={user}&password={password}')
    return r.text

def login(user, password):
    r = requests.get(f'{URL}/auth/login?user={user}&password={password}')
    if r.status_code == 200:
        return r.text, True
    return r.text, False
#USERS
#   BUZON
def notificaciones(token):
    r = requests.get(f'{URL}/users/mail/notificaciones',headers={'Authorization': f'Bearer {token}'})
    return r.text
def obtener_buzon(token):
    r = requests.get(f'{URL}/users/mail',headers={'Authorization': f'Bearer {token}'})
    mensajes = r.json()
    return mensajes  
def marcar_leido(token):
    r = requests.put(f'{URL}/users/mail',headers={'Authorization': f'Bearer {token}'})
    return r.text
#USERS
#   AMIGOS
def obtener_amigos(token):
    r = requests.get(f'{URL}/users/friends',headers={'Authorization': f'Bearer {token}'})
    amigos = r.json()
    return amigos
def obtener_solicitudes(token):
    r = requests.get(f'{URL}/users/friend-requests',headers={'Authorization': f'Bearer {token}'})
    solicitudes = r.json()
    return solicitudes
def enviar_solicitud(token,usuario):
    r = requests.post(f'{URL}/users/friend-requests?id_solicitud={usuario}',headers={'Authorization': f'Bearer {token}'})
    return r.text
def aceptar_solicitud(token,nuevo_amigo):
    r = requests.post(f'{URL}/users/friend-requests/{nuevo_amigo}/accept',headers={'Authorization': f'Bearer {token}'})
    return r.text
def rechazar_solicitud(token,usuario):
    r = requests.post(f'{URL}/users/friend-requests/{usuario}/reject',headers={'Authorization': f'Bearer {token}'})
    return r.text
def menu():
    while True:
        print('=== MENU ===')
        print('1. REGISTRARSE')
        print('2. INICIAR SESIÓN')
        print('3. Exit')
        choice = param('Eliga una opción: ',int,valores_validos=[1,2,3])
        if choice == 1:
            user = param('Usuario: ',str)
            password = param('Contraseña: ',str,is_password=True)
            mostrar_texto(signup(user, password))
            limpiar_pantalla()
        elif choice == 2:
            user = param('Usuario: ',str)
            password = param('Contraseña: ',str,is_password=True)
            log_in = login(user,password)
            if log_in[1]:
                token = log_in[0]
                limpiar_pantalla()
                while True:
                    mostrar_texto(notificaciones(token))
                    print('1. JUGAR')
                    print('2. PERFIL')
                    print('3. LOG OUT')
                    choice = param('Eliga una opción: ',int,valores_validos=[1,2,3])
                    if choice == 1:
                        pass
                    elif choice == 2:
                        limpiar_pantalla()
                        while True:
                            print('1. BUZÓN')
                            print('2. AMIGOS')
                            print('3. VOLVER')
                            choice = param('Eliga una opción: ',int,valores_validos=[1,2,3])
                            if choice == 1:
                                limpiar_pantalla()
                                while True:
                                    buzon = obtener_buzon(token)
                                    if buzon != []:
                                        mostrar_texto(buzon)
                                        print('1. MARCAR COMO LEÍDO')
                                        print('2. VOLVER')
                                        choice = param('Eliga una opción: ',int,valores_validos=[1,2])
                                        if choice == 1:
                                            mostrar_texto(marcar_leido(token))
                                        elif choice == 2:
                                            limpiar_pantalla()
                                            break
                                    else:
                                        mostrar_texto('No tienes ningún mensaje')
                                        print('1. RECARGAR')
                                        print('2. VOLVER')
                                        choice = param('Eliga una opción: ',int,valores_validos=[1,2])
                                        if choice == 1:
                                            continue
                                        else:
                                            limpiar_pantalla()
                                            break
                            elif choice == 2:
                                limpiar_pantalla()
                                while True:
                                    amigos = obtener_amigos(token)
                                    if amigos != []:
                                        mostrar_texto(amigos)
                                    else:
                                        mostrar_texto('Todavía no tienes amigos')
                                    print('1. SOLICITUDES DE AMISTAD')
                                    print('2. ENVIAR SOLICITUD DE AMISTAD')
                                    print('3. VOLVER')
                                    choice = param('Eliga una opción: ',int,valores_validos=[1,2,3])
                                    if choice == 1:
                                        limpiar_pantalla()
                                        while True:
                                            solicitudes = obtener_solicitudes(token)
                                            if solicitudes !=[]:
                                                mostrar_texto(solicitudes,enumerado=True)
                                                mostrar_texto(f'{len(solicitudes)+1}. VOLVER')
                                                valores_validos = [num for num in range(0,len(solicitudes) + 2)]
                                                choice = param('Eliga una opción: ',int,valores_validos=valores_validos)
                                                if choice != valores_validos[-1]:
                                                    solicitud = solicitudes[choice - 1] #Porque las listas empiezan en 0
                                                    print('1. ACEPTAR SOLICITUD')
                                                    print('2. RECHAZAR SOLICITUD')
                                                    choice = param('Eliga una opción: ',int,valores_validos=[1,2])
                                                    if choice == 1:
                                                        mostrar_texto(aceptar_solicitud(token,solicitud))
                                                        limpiar_pantalla()
                                                    elif choice == 2:
                                                        mostrar_texto(rechazar_solicitud(token,solicitud))
                                                        limpiar_pantalla()
                                                else:
                                                    limpiar_pantalla()
                                                    break
                                            else:
                                                mostrar_texto('No tienes ninguna solicitud de amistad')
                                                print('1. RECARGAR')
                                                print('2. VOLVER')
                                                choice = param('Eliga una opción: ',int,valores_validos=[1,2])
                                                if choice == 1:
                                                    continue
                                                else:
                                                    limpiar_pantalla()
                                                    break
                                    elif choice == 2:
                                        usuario = param('Introduzca el usuario: ',str)
                                        mostrar_texto(enviar_solicitud(token,usuario))
                                        limpiar_pantalla()
                                    elif choice == 3:
                                        limpiar_pantalla()
                                        break
                            elif choice == 3:
                                limpiar_pantalla()
                                break
                    elif choice == 3:
                        limpiar_pantalla()
                        break
            else:
                mostrar_texto(log_in[0])
                limpiar_pantalla()            
        elif choice == 3:
            print('Saliendo...')
            break


if __name__ == '__main__':
    menu()
