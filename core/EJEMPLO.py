import requests
import getpass
import os
from typing import *
import time
URL = 'http://127.0.0.1:5000'

#------------FUNCIONES------------
def to_tuple():
    while True:
        try:
            entrada = input("Introduce las coordenadas (fila, columna): ")
            # Eliminar espacios en blanco al principio y al final y luego dividir la cadena por la coma
            entrada = entrada.strip()
            coordenadas_str = entrada.split(',')

            # Verificar que haya exactamente dos coordenadas
            if len(coordenadas_str) != 2:
                print("Error: Debes introducir dos coordenadas separadas por una coma.")
                continue  # Volver al inicio del bucle

            # Eliminar espacios en blanco alrededor de cada coordenada y convertir a entero
            fila = int(coordenadas_str[0].strip())
            columna = int(coordenadas_str[1].strip())
            return (fila, columna)
        except (ValueError, TypeError):
            print('El tipo de dato no es válido.')
            continue

                
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
            else f'{nombre}'
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
                time.sleep(0.03)
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
#USERS
#   GAME REQUESTS
def invitaciones_privadas(token):
    r = requests.get(f'{URL}/users/game_requests',headers={'Authorization': f'Bearer {token}'})
    invitaciones = r.json()
    return invitaciones
#   MY GAMES
def mis_partidas(token):
    r = requests.get(f'{URL}/users/my_games',headers={'Authorization': f'Bearer {token}'})
    partidas = r.json()
    return partidas
#PARTIDA
def crear_partida(token,privada,reino, invitado = None, size=3, terrenos=None):
    parametros_partida = {
        'privada': privada,
        'invitado': invitado,
        'reino': reino,
        'size' : size,
        'terrenos': terrenos
    }
    r = requests.post(f'{URL}/games',headers={'Authorization': f'Bearer {token}'},json=parametros_partida)
    return r.text
def partidas_publicas(token):
    r = requests.get(f'{URL}/games',headers={'Authorization': f'Bearer {token}'})
    publicas = r.json()
    return publicas
#/game/<id>/
def unirse_partida(token,id_partida,reino):
    r = requests.put(f'{URL}/games/{id_partida}/join?reino={reino}',headers={'Authorization': f'Bearer {token}'})
    return r.text
def iniciar_partida(token,id_partida):
    r = requests.put(f'{URL}/games/{id_partida}/start',headers={'Authorization': f'Bearer {token}'})
    return r.text
def cancelar_partida(token,id_partida):
    r = requests.post(f'{URL}/games/{id_partida}/cancel',headers={'Authorization': f'Bearer {token}'})
    return r.text
def get_estado_partida(token,id_partida):
    r = requests.get(f'{URL}/games/{id_partida}/game_state',headers={'Authorization': f'Bearer {token}'})
    estado = r.text
    return estado

def get_estado_jugador(token, id_partida):
    r = requests.get(f'{URL}/games/{id_partida}/player_state', headers={'Authorization': f'Bearer {token}'})
    try:
        respuesta_json = r.json()
        # Usamos .get() por seguridad, devuelve None si la clave no existe
        return respuesta_json.get("es_turno")
    except requests.exceptions.JSONDecodeError as e:
        print(f"ERROR: Fallo al decodificar JSON en get_estado_jugador. Respuesta recibida: {r.text}")
        return None
    except AttributeError: # En caso de que r.json() devolviera algo inesperado o la clave faltara
         print(f"ERROR: La respuesta JSON no era un diccionario o no tenía la clave 'es_turno'. Respuesta: {r.text}")
         return None


#/game/<id>/player
def ver_zona(token,id_partida, coordenada):
    diccionario = {'zona': coordenada}
    r = requests.post(f'{URL}/games/{id_partida}/player/ver_zona',headers={'Authorization': f'Bearer {token}'},json=(diccionario))
    zona = r.json()
    return zona,r.status_code

def ver_recursos(token, id_partida):
    r = requests.get(f'{URL}/games/{id_partida}/player/ver_recursos',headers={'Authorization': f'Bearer {token}'})
    return r.json()

def ver_mapa(token, id_partida):
    r = requests.get(f'{URL}/games/{id_partida}/player/ver_mapa',headers={'Authorization': f'Bearer {token}'})
    if r.status_code == 200:
        return r.text
    else:
        print(f"Error al obtener el mapa: {r.status_code}")
        print("Respuesta recibida: ", r.text)
        return None

def cambiar_turno(token, id_partida):
    r = requests.put(f'{URL}/games/{id_partida}/player/cambiar_turno',headers={'Authorization': f'Bearer {token}'})
    if r.status_code == 200:
        return r.text
    else:
        print(f"Error al obtener el mapa: {r.status_code}")
        print("Respuesta recibida: ", r.text)
        return None

def todos_mis_recursos(token, id_partida):
    r = requests.get(f'{URL}/games/{id_partida}/player/todos_mis_recursos',headers={'Authorization': f'Bearer {token}'})
    if r.status_code == 200:
        return r.text
    else:
        print(f"Error al obtener todos los recursos: {r.status_code}")
        print("Respuesta recibida: ", r.text)
        return None


### MENU PRINCIPAL ###
def menu():
    while True:
        print('=== MENU ===')
        print('1. REGISTRARSE')
        print('2. INICIAR SESIÓN')
        print('3. Exit')
        choice = param('Eliga una opción: ',int,valores_validos=[1,2,3])
        print()
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
                    print()
                    if choice == 1:
                        limpiar_pantalla()
                        while True:
                            print('0. VOLVER')
                            print('1. CREAR PARTIDA')
                            print('2. UNIRSE A PARTIDA')
                            choice = param('Eliga una opción: ',int,valores_validos=[0, 1, 2])
                            print()
                            if choice == 1:
                                limpiar_pantalla()
                                while True:
                                    privada = True if param('Publica o privada?: ',str,valores_validos=['publica','privada','Publica','Privada']).lower() == 'privada' else False
                                    if privada:
                                        amigos = obtener_amigos(token)
                                        if amigos != []:
                                            mostrar_texto(amigos,enumerado=True)
                                            valores_validos = [n for n in range(0,len(amigos)+1)]
                                            amigo = param('Que amigo desea invitar: ',int,valores_validos=valores_validos)
                                            invitado = amigos[amigo - 1]
                                        else:
                                            mostrar_texto('Todavía no tienes amigos')
                                            limpiar_pantalla()
                                            break
                                    else:
                                        invitado = None

                                    print('0. VOLVER')
                                    print('1. PARTIDA CUSTOM')#/game [POST] -> Crear Partida con id random, el mapa y añade al primer usuario
                                    print('2. PARTIDA DEFAULT')#/game [POST]
                                    choice = param('Eliga una opción: ',int,valores_validos=[0, 1, 2])
                                    print()
                                    if choice == 1:
                                        mostrar_texto('Kingdom Kraft esta trabajando en ello, vuelva más tarde')
                                        break
                                    elif choice == 2:
                                        reino = param('Introduce el nombre de tu reino: ',str)
                                        mostrar_texto(crear_partida(token,privada,reino,invitado))
                                        limpiar_pantalla()
                                        break
                                    elif choice == 0:
                                        limpiar_pantalla()
                                        break
                            elif choice == 2:
                                limpiar_pantalla()
                                while True:
                                    print('0. VOLVER')
                                    print('1. UNIRSE A UNA NUEVA PARTIDA') #/game [GET] y #/game/<id>/join [PUT] + /game/<id>/start [PUT]
                                    print('2. CONTINUAR') #/users/my_games [GET] #/game/<id>/game_state [GET] -> /game/<id>/ver_zona
                                    choice = param('Eliga una opción: ',int,valores_validos=[0, 1, 2])
                                    print()
                                    if choice == 1:
                                        publicas = partidas_publicas(token)
                                        partidas_str = [partida for partida in publicas.values()]
                                        mostrar_texto(partidas_str,enumerado=True)
                                        id_partida = param('Introduzca el id de la partida a la que desea unirse: ',str)
                                        reino = param('Introduce el nombre de tu reino: ',str)
                                        mostrar_texto(unirse_partida(token,id_partida,reino))
                                        mostrar_texto(iniciar_partida(token,id_partida))
                                        limpiar_pantalla()
                                    elif choice == 2:
                                        user_partidas = mis_partidas(token)
                                        if user_partidas != {}:
                                            str_partidas = [partida for partida in user_partidas.values()]
                                            mostrar_texto(str_partidas)
                                        else:
                                            mostrar_texto('Todavía no te has unido a ninguna partida')
                                            limpiar_pantalla()
                                            continue
                                        id_user_partida = param('Introduzca el id de la partida: ',str)
                                        estado_partida = get_estado_partida(token,id_user_partida)
                                        if estado_partida == 'Empezada':
                                            while True:
                                                if get_estado_jugador(token,id_user_partida):
                                                    mostrar_texto('Bienvenido a Kingdom Craft')
                                                    limpiar_pantalla()
                                                    while get_estado_jugador(token,id_user_partida) == True:
                                                        print('===KINGDOM CRAFT===')
                                                        print('0. SALIR')
                                                        print('1. VER ZONA')
                                                        print('2. VER MIS RECURSOS')
                                                        print('3. VER MAPA')
                                                        print('4. FINALIZAR MI TURNO')
                                                        choice = param('Eliga una opción: ',int,valores_validos=[0, 1, 2, 3, 4])
                                                        print()
                                                        if choice == 1:
                                                            coordenada = to_tuple()
                                                            zona, estado = ver_zona(token,id_user_partida,coordenada)
                                                            if estado == 200:
                                                                while True:
                                                                    if zona[1]:
                                                                        print(zona[0])
                                                                        print('0. VOLVER')
                                                                        print('1. AÑADIR TROPA')
                                                                        print('2. MOVER TROPA')
                                                                        print('3. MOVER BATALLÓN')
                                                                        print('4. CONSTRUIR EDIFICIO')
                                                                        choice = param('Eliga una opción: ',int,valores_validos=[0, 1, 2, 3, 4])
                                                                        match choice:
                                                                            case 0:
                                                                                limpiar_pantalla()
                                                                                break
                                                                            case 1:
                                                                                pass
                                                                            case 2:
                                                                                pass
                                                                            case 3:
                                                                                pass
                                                                            case 4:
                                                                                pass

                                                                    else:
                                                                        print(zona[0])
                                                                        print('1. VOLVER')
                                                                        choice = param('Eliga una opción: ',int,valores_validos=[1])
                                                                        if choice == 1:
                                                                            limpiar_pantalla()
                                                                            break
                                                            elif estado == 404:
                                                                mostrar_texto(zona['error'])
                                                                continue

                                                        elif choice == 2:
                                                            mostrar_texto(todos_mis_recursos(token, id_user_partida))
                                                            param('Presione "Enter" para continuar ...', str, valores_validos=[''])
                                                            limpiar_pantalla()
                                                            continue

                                                        elif choice == 3:
                                                            mapa = ver_mapa(token, id_user_partida)
                                                            mostrar_texto(mapa)
                                                            param('Presione "Enter" para continuar ...', str, valores_validos=[''])
                                                            limpiar_pantalla()
                                                            continue

                                                        elif choice == 4:
                                                            mostrar_texto(cambiar_turno(token,id_user_partida))
                                                            param('Presione "Enter" para continuar ...', str, valores_validos=[''])
                                                            limpiar_pantalla()
                                                            break

                                                        else:
                                                            limpiar_pantalla()
                                                            break
                                                else:
                                                    mostrar_texto('Todavía no es tu turno')
                                                    print('0. VOLVER')
                                                    print('1. RECARGAR')
                                                    choice = param('Eliga una opción: ',int,valores_validos=[0, 1])
                                                    if choice == 1:
                                                        continue
                                                    else:
                                                        limpiar_pantalla()
                                                        break
                                        elif estado_partida == 'Esperando':
                                            mostrar_texto('Esperando a que se una otro jugador')
                                            limpiar_pantalla()
                                            continue
                                        elif estado_partida == 'Finalizada':
                                            mostrar_texto('Kingdom Craft esta trabajando en ello')
                                            limpiar_pantalla()
                                            continue
                                    else:
                                        limpiar_pantalla()
                                        break
                            elif choice == 0:
                                limpiar_pantalla()
                                break

                    elif choice == 2:
                        limpiar_pantalla()
                        while True:
                            print('0. VOLVER')
                            print('1. BUZÓN')
                            print('2. AMIGOS')
                            choice = param('Eliga una opción: ',int,valores_validos=[0, 1, 2])
                            if choice == 1:
                                limpiar_pantalla()
                                while True:
                                    buzon = obtener_buzon(token)
                                    if buzon != []:
                                        mostrar_texto(buzon)
                                        print('0. VOLVER')
                                        print('1. MARCAR COMO LEÍDO')
                                        choice = param('Eliga una opción: ',int,valores_validos=[0, 1])
                                        if choice == 1:
                                            mostrar_texto(marcar_leido(token))
                                            limpiar_pantalla()
                                        else:
                                            limpiar_pantalla()
                                            break
                                    else:
                                        mostrar_texto('No tienes ningún mensaje')
                                        print('0. VOLVER')
                                        print('1. RECARGAR')
                                        choice = param('Eliga una opción: ',int,valores_validos=[0, 1])
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
                                        mostrar_texto('Todavía no tienes amigos agregados')

                                    print('0. VOLVER')
                                    print('1. SOLICITUDES DE AMISTAD')
                                    print('2. ENVIAR SOLICITUD DE AMISTAD')
                                    print('3. INVITACIONES DE PARTIDA')
                                    choice = param('Eliga una opción: ',int,valores_validos=[0, 1, 2, 3])
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
                                                print('0. VOLVER')
                                                print('1. RECARGAR')
                                                choice = param('Eliga una opción: ',int,valores_validos=[0, 1])
                                                print()
                                                if choice == 1:
                                                    continue
                                                else:
                                                    limpiar_pantalla()
                                                    break
                                    elif choice == 2:
                                        usuario = param('Introduzca el usuario: ',str)
                                        mostrar_texto(enviar_solicitud(token,usuario))
                                        limpiar_pantalla()
                                    elif choice == 3: #Invitaciones de partida
                                        limpiar_pantalla()
                                        while True:
                                            invitaciones_dict = invitaciones_privadas(token)
                                            if invitaciones_dict != {}:
                                                invitaciones_str = [partida for partida in invitaciones_dict.values()]
                                                mostrar_texto(invitaciones_str,enumerado=True)
                                                id_invitacion = param('Introduce el id de la invitación',str)
                                                print('1. ACEPTAR INVITACIÓN')
                                                print('2. RECHAZAR INVITACIÓN')
                                                choice = param('Eliga una opción: ',int,valores_validos=[1,2])
                                                if choice == 1:
                                                    reino = param('Introduce el nombre de tu reino: ',str)
                                                    mostrar_texto(unirse_partida(token,id_invitacion,reino))
                                                    mostrar_texto(iniciar_partida(token,id_invitacion))
                                                    break
                                                elif choice == 2:
                                                    mostrar_texto(cancelar_partida(token,id_invitacion))
                                                    break
                                            else:
                                                mostrar_texto('No tienes ninguna invitación')
                                                print('1. RECARGAR')
                                                print('2. VOLVER')
                                                choice = param('Eliga una opción: ',int,valores_validos=[1,2])
                                                if choice == 1:
                                                    continue
                                                else:
                                                    limpiar_pantalla()
                                                    break
                                        
                                    elif choice == 0:
                                        limpiar_pantalla()
                                        break
                            elif choice == 0:
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
