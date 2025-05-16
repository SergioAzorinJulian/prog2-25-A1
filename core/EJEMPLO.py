import requests
import getpass
import os
from typing import *
import time
from mapa import Mapa
from copy import deepcopy
URL = 'MaritoTSF.pythonanywhere.com'
TERRENOS_JUEGO = Mapa.terrenos_disponibles
#------------FUNCIONES------------
def partida_custom():
    size = param('Introduce un tamaño del mapa: ',int, valores_validos=[i for i in range(3,51)])
    while True:
        terrenos = param('Introduce los terrenos del mapa separados por comas (min. 2): ', str)
        if len(terrenos.split(',')) < 2:
            print('Error: Debe introducir al menos 2 tipos de terreno.', style = 'warning')
            continue

        copia_terrenos = deepcopy(TERRENOS_JUEGO)
        for terreno in terrenos.split(','):
            if terreno.strip().lower() in copia_terrenos:
                copia_terrenos.remove(terreno.strip().lower())
            else:
                if terreno.strip().lower() in TERRENOS_JUEGO:
                    print(f'Error: El tipo de terreno "{terreno}" se ha introducido más de una vez.',)
                else:
                    print(f'Error: El tipo de terreno "{terreno}" no existe en el juego.')
                limpiar_pantalla()
                break
        return size,terrenos
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
#   SQL
def ver_ranking(token):
    r = requests.get(f'{URL}/users/ranking',headers={'Authorization': f'Bearer {token}'})
    ranking = r.json()
    return ranking
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
    return estado,r.status_code
def get_estado_jugador(token,id_partida):
    r = requests.get(f'{URL}/games/{id_partida}/player_state',headers={'Authorization': f'Bearer {token}'})
    estado = r.json()
    return estado
#/game/<id>/player
def ver_zona(token,id_partida,coordenada):
    diccionario = {'zona': coordenada}
    r = requests.post(f'{URL}/games/{id_partida}/player/ver_zona',headers={'Authorization': f'Bearer {token}'},json=(diccionario))
    zona = r.json()
    return zona,r.status_code
def ver_recursos(token,id_partida):
    r = requests.get(f'{URL}/games/{id_partida}/player/ver_recursos',headers={'Authorization': f'Bearer {token}'})
    return r.json()
def ver_mapa(token, id_partida):
    r = requests.get(f'{URL}/games/{id_partida}/player/ver_mapa',headers={'Authorization': f'Bearer {token}'})
    return r.text
def cambiar_turno(token, id_partida):
    r = requests.put(f'{URL}/games/{id_partida}/player/cambiar_turno',headers={'Authorization': f'Bearer {token}'})
    return r.text
def catalogos(token, id_partida):
    r = requests.get(f'{URL}/games/{id_partida}/player/catalogos',headers={'Authorization': f'Bearer {token}'})
    return r.json()
def add_tropa(token, id_partida, tropa, cantidad):
    diccionario = {'tropa':tropa,'cantidad':cantidad}
    r = requests.post(f'{URL}/games/{id_partida}/player/add_tropa',headers={'Authorization': f'Bearer {token}'},json=(diccionario))
    return r.text
def mover_tropa(token, id_partida, tropa, cantidad, destino):
    diccionario = {'tropa':tropa,'cantidad':cantidad, 'destino': destino}
    r = requests.put(f'{URL}/games/{id_partida}/player/mover_tropa',headers={'Authorization': f'Bearer {token}'},json=(diccionario))
    return r.json()
def mover_batallon(token, id_partida,destino):
    diccionario = {'destino': destino}
    r = requests.put(f'{URL}/games/{id_partida}/player/mover_batallon',headers={'Authorization': f'Bearer {token}'},json=(diccionario))
    return r.json()
def construir_edificio(token,id_partida,edificio):
    r = requests.post(f'{URL}/games/{id_partida}/player/edificio',headers={'Authorization': f'Bearer {token}'},json=(edificio))
    return r.text
def subir_nivel_edificio(token,id_partida,edificio):
    r = requests.put(f'{URL}/games/{id_partida}/player/edificio',headers={'Authorization': f'Bearer {token}'},json=(edificio))
    return r.text
def combatir(token, id_partida, atacantes_pos, defensores_pos):
    diccionario = {
        'atacantes': atacantes_pos,
        'defensores': defensores_pos
    }
    r = requests.put(f'{URL}/games/{id_partida}/player/combatir', headers={'Authorization': f'Bearer {token}'},
                     json=(diccionario))
    return r.json()

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
                        limpiar_pantalla()
                        while True:
                            print('1. CREAR PARTIDA')
                            print('2. UNIRSE A PARTIDA')
                            print('3. RANKING')
                            print('4. VOLVER')
                            choice = param('Eliga una opción: ',int,valores_validos=[1,2,3,4])
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
                                    print('1. PARTIDA CUSTOM')#/game [POST] -> Crear Partida con id random, el mapa y añade al primer usuario
                                    print('2. PARTIDA DEFAULT')#/game [POST]
                                    print('3. VOLVER')
                                    choice = param('Eliga una opción: ',int,valores_validos=[1,2,3])
                                    if choice == 1:
                                        size, terrenos = partida_custom()
                                        reino = param('Introduce el nombre de tu reino: ',str)
                                        mostrar_texto(crear_partida(token, privada, reino, invitado, size, terrenos))
                                        limpiar_pantalla()
                                        break
                                    elif choice == 2:
                                        reino = param('Introduce el nombre de tu reino: ',str)
                                        mostrar_texto(crear_partida(token,privada,reino,invitado))
                                        limpiar_pantalla()
                                        break
                                    elif choice == 3:
                                        limpiar_pantalla()
                                        break
                            elif choice == 2:
                                limpiar_pantalla()
                                while True:
                                    print('1. UNIRSE A UNA NUEVA PARTIDA') #/game [GET] y #/game/<id>/join [PUT] + /game/<id>/start [PUT]
                                    print('2. CONTINUAR') #/users/my_games [GET] #/game/<id>/game_state [GET] -> /game/<id>/ver_zona
                                    print('3. VOLVER')
                                    choice = param('Eliga una opción: ',int,valores_validos=[1,2,3])
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
                                        while True:
                                            estado_partida, r_estado = get_estado_partida(token,id_user_partida)
                                            if r_estado == 200:
                                                if estado_partida == 'Empezada':                                    
                                                    estado_jugador = get_estado_jugador(token,id_user_partida)
                                                    if estado_jugador:
                                                        mostrar_texto('Bienvenido a Kingdom Craft')
                                                        if 'catalogos_dict' not in locals().keys(): #Creamos el catalogo si no existe
                                                            catalogos_dict = catalogos(token,id_user_partida)
                                                        limpiar_pantalla()
                                                        print('===KINGDOM CRAFT===')
                                                        print('1. VER ZONA')
                                                        print('2.VER RECURSOS')
                                                        print('3. VER MAPA')
                                                        print('4. CAMBIAR TURNO')
                                                        print('5. SALIR')
                                                        choice = param('Eliga una opción: ',int,valores_validos=[1,2,3,4,5])
                                                        if choice == 1:
                                                            coordenada = to_tuple()                                                            
                                                            while True: 
                                                                zona,estado = ver_zona(token,id_user_partida,coordenada)
                                                                if estado == 200:
                                                                    if zona[1]:
                                                                        print(zona[0])
                                                                        print('1. AÑADIR TROPA')
                                                                        print('2. MOVER TROPA')
                                                                        print('3. MOVER BATALLÓN')
                                                                        print('4. CONSTRUIR EDIFICIO')
                                                                        print('5. SUBIR DE NIVEL EDIFICIO')
                                                                        print('6. VOLVER')
                                                                        choice = param('Eliga una opción: ',int,valores_validos=[1,2,3,4,5,6])
                                                                        match choice:
                                                                            case 1:
                                                                                mostrar_texto(catalogos_dict['tropas']['catalogo'])
                                                                                tropa = param('Introduzca el nombre de la tropa: ',str, valores_validos=catalogos_dict['tropas']['valores_validos'])
                                                                                cantidad = param('Introduzca la cantidad: ',int)
                                                                                mostrar_texto(add_tropa(token,id_user_partida,tropa,cantidad))
                                                                                limpiar_pantalla()
                                                                                
                                                                            case 2:
                                                                                tropa = param('Introduzca el nombre de la tropa: ',str, valores_validos=catalogos_dict['tropas']['valores_validos'])
                                                                                cantidad = param('Introduzca la cantidad: ',int)
                                                                                destino = to_tuple()
                                                                                salida = mover_tropa(token,id_user_partida,tropa,cantidad,destino)
                                                                                if isinstance(salida,list): #No se a podido mover la tropa, saltar opcion de combate
                                                                                    if isinstance(salida, list):
                                                                                        mostrar_texto(salida[0])
                                                                                        print('1. COMBATIR (Se enviarán a todas las tropas de la región)')
                                                                                        print('2. ABORTAR')
                                                                                        choice = param('Eliga una opción: ',int, valores_validos=[1,2])
                                                                                        if choice == 1:
                                                                                            salida = combatir(token,id_user_partida, coordenada, destino)
                                                                                            mostrar_texto(salida['texto'])
                                                                                            limpiar_pantalla()
                                                                                            if salida['estado'] == 'Finalizada':
                                                                                                break
                                                                                        else:
                                                                                            limpiar_pantalla()
                                                                                            continue
                                                                                else:
                                                                                    mostrar_texto(salida)
                                                                                    limpiar_pantalla()                                                                                                                       
                                                                            case 3:
                                                                                destino = to_tuple()
                                                                                salida = mover_batallon(token,id_user_partida,destino)
                                                                                if isinstance(salida,list):
                                                                                    mostrar_texto(salida[0])
                                                                                    print('1. COMBATIR (Se enviarán a todas las tropas de la región)')
                                                                                    print('2. ABORTAR')
                                                                                    choice = param('Eliga una opción: ',int, valores_validos=[1,2])
                                                                                    if choice == 1:
                                                                                        salida = combatir(token,id_user_partida, coordenada, destino)
                                                                                        mostrar_texto(salida['texto'])
                                                                                        limpiar_pantalla()
                                                                                        if salida['estado'] == 'Finalizada':
                                                                                            break
                                                                                    else:
                                                                                        limpiar_pantalla()
                                                                                        continue
                                                                                else:
                                                                                    mostrar_texto(salida)
                                                                                    limpiar_pantalla()
                                                                            case 4:
                                                                                mostrar_texto(catalogos_dict['edificios']['catalogo'])
                                                                                edificio = param('Introduzca el nombre del edificio: ',str, valores_validos=catalogos_dict['edificios']['valores_validos'])
                                                                                mostrar_texto(construir_edificio(token,id_user_partida,edificio))
                                                                            case 5:
                                                                                edificio = param('Introduzca el nombre del edificio: ',str, valores_validos=catalogos_dict['edificios']['valores_validos'])
                                                                                mostrar_texto(subir_nivel_edificio(token,id_user_partida,edificio))
                                                                            case 6:
                                                                                limpiar_pantalla()
                                                                                break
                                                                
                                                                    else:
                                                                        print(zona[0])
                                                                        print('1. VOLVER')
                                                                        choice = param('Eliga una opción: ',int,valores_validos=[1])
                                                                        if choice == 1:
                                                                            limpiar_pantalla()
                                                                            break
                                                                elif estado == 404:
                                                                    mostrar_texto(zona['error'])
                                                                    break
                                                        elif choice == 2:
                                                            mostrar_texto(ver_recursos(token,id_user_partida),enumerado=True)
                                                            print('1. VOLVER')
                                                            choice = param('Eliga una opción: ',int,valores_validos=[1])
                                                            if choice == 1:
                                                                limpiar_pantalla()
                                                                continue
                                                        elif choice == 3:
                                                            print(ver_mapa(token,id_user_partida))
                                                            print('1. VOLVER')
                                                            choice = param('Eliga una opción: ',int,valores_validos=[1])
                                                            if choice == 1:
                                                                limpiar_pantalla()
                                                                continue
                                                        elif choice == 4:
                                                            mostrar_texto(cambiar_turno(token,id_user_partida))
                                                            continue
                                                        else:
                                                            limpiar_pantalla()
                                                            break
                                                    else:
                                                        mostrar_texto('Todavía no es tu turno')
                                                        print('1. RECARGAR')
                                                        print('2. VOLVER')
                                                        choice = param('Eliga una opción: ',int,valores_validos=[1,2])
                                                        if choice == 1:
                                                            continue
                                                        else:
                                                            limpiar_pantalla()
                                                            break
                                                elif estado_partida == 'Esperando':
                                                    mostrar_texto('Esperando a que se una otro jugador')
                                                    limpiar_pantalla()
                                                    break
                                                elif estado_partida == 'Finalizada':
                                                    mostrar_texto('Kingdom Craft esta trabajando en ello')
                                                    limpiar_pantalla()
                                                    continue
                                            elif r_estado == 404:
                                                mostrar_texto(estado_partida)
                                                break
                                    else:
                                        limpiar_pantalla()
                                        break
                            elif choice == 3:
                                mostrar_texto(ver_ranking(token))
                                print('1. VOLVER')
                                choice = param('Eliga una opción: ',int,valores_validos=[1])
                                continue
                            elif choice == 4:
                                limpiar_pantalla()
                                break

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
                                            limpiar_pantalla()
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
                                    print('3. INVITACIONES DE PARTIDA')
                                    print('4. VOLVER')
                                    choice = param('Eliga una opción: ',int,valores_validos=[1,2,3,4])
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
                                        
                                    elif choice == 4:
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
