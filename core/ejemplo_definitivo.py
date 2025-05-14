import requests
import getpass
import os
from typing import *
import time
from copy import deepcopy
from rich.console import Console
from rich.theme import Theme
from rich.table import Table
from rich.markdown import Markdown
from rich.align import Align
from rich.text import Text
from rich.progress import track
from rich import box

from core.EJEMPLO_rich import despedida_md, temas_predefinidos
from mapa import Mapa

#Configuracion de rich
titulo_md = Markdown("# Bienvenido a Kingdom Kraft")
parrafo_texto = Text(
    "Un juego de estrategia por turnos donde podrás construir tu reino, gestionar tus recursos y enfrentarte a otros jugadores.",
    justify="center"
)
despedida_md = Markdown("##### ¡Buena suerte!")

temas_predefinidos = Theme({
    "info": "blue",
    "error": "bold red",
    "success": "bold green",
    "warning": "yellow",
    "prompt": "magenta",
    "input": "cyan",
})
console = Console(theme = temas_predefinidos)

URL = 'http://127.0.0.1:5000'
TERRENOS_JUEGO = Mapa.terrenos_disponibles

#-----------------FUNCIONES-----------------
def partida_custom():
    size = param('Introduce el tamaño del mapa (min.3, max.50): ', int, valores_validos=[i for i in range(3, 51)],
                 estilo='input')
    while True:
        terrenos = param('Introduce los terrenos del mapa separados por comas (min. 2): ', str, estilo='input')
        if len(terrenos.split(',')) < 2:
            console.print('Error: Debe introducir al menos 2 tipos de terreno.', style='warning')
            continue

        copia_terrenos = deepcopy(TERRENOS_JUEGO)
        for terreno in terrenos.split(','):
            if terreno.strip().lower() in copia_terrenos:
                copia_terrenos.remove(terreno.strip().lower())
            else:
                if terreno.strip().lower() in TERRENOS_JUEGO:
                    console.print(
                        f'[error]Error: El tipo de terreno "{terreno}" se ha introducido más de una vez.[/error] \n[info]Ayuda: La multiplicidad máxima de cada terreno es 1.[/info]')
                else:
                    console.print(f'Error: El tipo de terreno "{terreno}" no existe en el juego.', style='error')
                console.print()
                table_terrenos = Table(box=box.ROUNDED, border_style='bold', header_style="bold white reverse blue")
                table_terrenos.add_column('TIPOS DE TERRENOS DISPONIBLES', justify='center', style='info')
                for terreno in TERRENOS_JUEGO:
                    table_terrenos.add_row(terreno.capitalize())
                console.print(table_terrenos)
                console.print()
                limpiar_pantalla()
                break
        else:
            break
    return size, terrenos

def to_tuple():
    while True:
        try:
            entrada = console.input("[input]Introduce las coordenadas (fila, columna): [/input]")
            entrada = entrada.strip()
            coordenadas_str = entrada.split(',')
            if len(coordenadas_str) != 2:
                console.print("Error: Debes introducir dos coordenadas separadas por una coma.", style='warning')
                continue
            fila = int(coordenadas_str[0].strip())
            columna = int(coordenadas_str[1].strip())
            return (fila, columna)
        except (ValueError, TypeError):
            console.print('El tipo de dato no es válido.', style='error')
            continue

def param(
        nombre: str,
        tipo: type,
        lon_min: int = 0,
        is_password: bool = False,
        valores_validos: Union[list, tuple, None] = None,
        estilo: str = 'input'
) -> Any:
    valido = False
    out = None
    while not valido:
        prompt = (
            f'{nombre} (Longitud mínima: {lon_min}): '
            if lon_min
            else f'{nombre}'
        )
        entrada = getpass.getpass(prompt) if is_password else console.input(f"[{estilo}]{prompt}[/{estilo}]")
        if len(entrada) < lon_min:
            console.print(f'Longitud menor que la requerida: {lon_min}', style='warning')
            continue
        try:
            out = tipo(entrada)
        except (ValueError, TypeError):
            console.print('El tipo de dato no es válido.', style='error')
            continue
        if valores_validos and out not in valores_validos:
            console.print(f'La entrada {out} no está presente en las opciones válidas {valores_validos}', style='error')
            continue
        valido = True
    return out

def limpiar_pantalla() -> None:
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def mostrar_texto(lista: list[str] | str, enumerado: bool = False, estilo: str = 'prompt') -> None:
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
                    console.print(letra, end='', style=estilo)
                n += 1
            for caracter in texto:
                console.print(caracter, end='', style=estilo)
                time.sleep(0.03)
            console.print('\n', end='')

def tabla_espera():
    table_espera = Table(show_edge=False, header_style="bold white reverse blue")
    table_espera.add_column('MENÚ', justify='center', style='prompt')
    table_espera.add_row('0. Volver', style='dim')
    table_espera.add_row('1. Recargar')
    console.print(table_espera)
    console.print()

def barra_de_progreso(ritmo, tiempo):
    for _ in track(range(ritmo), description="Procesando..."):
        time.sleep(tiempo)

# ------------REQUESTS------------
# AUTENTICACIÓN
def signup(user, password):
    obtener_jugadores()
    r = requests.post(f'{URL}/auth/signup?user={user}&password={password}')
    subir_jugadores()
    subir_buzones()
    return r.text

def login(user, password):
    obtener_jugadores()
    r = requests.get(f'{URL}/auth/login?user={user}&password={password}')
    if r.status_code == 200:
        return r.text, True
    return r.text, False

# USERS - BUZON
def notificaciones(token):
    obtener_buzones()
    r = requests.get(f'{URL}/users/mail/notificaciones', headers={'Authorization': f'Bearer {token}'})
    return r.text

def obtener_buzon(token):
    r = requests.get(f'{URL}/users/mail', headers={'Authorization': f'Bearer {token}'})
    mensajes = r.json()
    return mensajes

def marcar_leido(token):
    r = requests.put(f'{URL}/users/mail', headers={'Authorization': f'Bearer {token}'})
    return r.text

# USERS - AMIGOS
def obtener_amigos(token):
    r = requests.get(f'{URL}/users/friends', headers={'Authorization': f'Bearer {token}'})
    amigos = r.json()
    return amigos

def obtener_solicitudes(token):
    r = requests.get(f'{URL}/users/friend-requests', headers={'Authorization': f'Bearer {token}'})
    solicitudes = r.json()
    return solicitudes

def enviar_solicitud(token, usuario):
    r = requests.post(f'{URL}/users/friend-requests?id_solicitud={usuario}', headers={'Authorization': f'Bearer {token}'})
    return r.text

def aceptar_solicitud(token, nuevo_amigo):
    r = requests.post(f'{URL}/users/friend-requests/{nuevo_amigo}/accept', headers={'Authorization': f'Bearer {token}'})
    return r.text

def rechazar_solicitud(token, usuario):
    r = requests.post(f'{URL}/users/friend-requests/{usuario}/reject', headers={'Authorization': f'Bearer {token}'})
    return r.text

# USERS - GAME REQUESTS
def invitaciones_privadas(token):
    r = requests.get(f'{URL}/users/game_requests', headers={'Authorization': f'Bearer {token}'})
    invitaciones = r.json()
    return invitaciones

# MY GAMES
def mis_partidas(token):
    r = requests.get(f'{URL}/users/my_games', headers={'Authorization': f'Bearer {token}'})
    partidas = r.json()
    return partidas

# PARTIDA
def crear_partida(token, privada, reino, invitado=None, size=3, terrenos=None):
    parametros_partida = {
        'privada': privada,
        'invitado': invitado,
        'reino': reino,
        'size': size,
        'terrenos': terrenos
    }
    r = requests.post(f'{URL}/games', headers={'Authorization': f'Bearer {token}'}, json=parametros_partida)
    return r.text

def partidas_publicas(token):
    r = requests.get(f'{URL}/games', headers={'Authorization': f'Bearer {token}'})
    publicas = r.json()
    return publicas

# /game/<id>/
def unirse_partida(token, id_partida, reino):
    r = requests.put(f'{URL}/games/{id_partida}/join?reino={reino}', headers={'Authorization': f'Bearer {token}'})
    return r.text

def iniciar_partida(token, id_partida):
    r = requests.put(f'{URL}/games/{id_partida}/start', headers={'Authorization': f'Bearer {token}'})
    return r.text

def cancelar_partida(token, id_partida):
    r = requests.post(f'{URL}/games/{id_partida}/cancel', headers={'Authorization': f'Bearer {token}'})
    return r.text

def get_estado_partida(token, id_partida):
    r = requests.get(f'{URL}/games/{id_partida}/game_state', headers={'Authorization': f'Bearer {token}'})
    estado = r.text
    return estado, r.status_code

def get_estado_jugador(token, id_partida):
    r = requests.get(f'{URL}/games/{id_partida}/player_state', headers={'Authorization': f'Bearer {token}'})
    try:
        respuesta_json = r.json()
        return respuesta_json.get("es_turno")
    except requests.exceptions.JSONDecodeError as e:
        console.print(f"ERROR: Fallo al decodificar JSON en get_estado_jugador. Respuesta recibida: {r.text}", style='error')
        return None
    except AttributeError:
        console.print(f"ERROR: La respuesta JSON no era un diccionario o no tenía la clave 'es_turno'. Respuesta: {r.text}", style='error')
        return None

# /game/<id>/player
def ver_zona(token, id_partida, coordenada):
    diccionario = {'zona': coordenada}
    r = requests.post(f'{URL}/games/{id_partida}/player/ver_zona', headers={'Authorization': f'Bearer {token}'}, json=diccionario)
    zona = r.json()
    return zona, r.status_code

def ver_recursos(token, id_partida):
    r = requests.get(f'{URL}/games/{id_partida}/player/ver_recursos', headers={'Authorization': f'Bearer {token}'})
    return r.json()

def ver_mapa(token, id_partida):
    r = requests.get(f'{URL}/games/{id_partida}/player/ver_mapa', headers={'Authorization': f'Bearer {token}'})
    if r.status_code == 200:
        return r.text
    else:
        console.print(f"[error]Error al obtener el mapa: [/error]{r.status_code}")
        console.print("Respuesta recibida: ", r.text, style='error')
        return None

def cambiar_turno(token, id_partida):
    r = requests.put(f'{URL}/games/{id_partida}/player/cambiar_turno', headers={'Authorization': f'Bearer {token}'})
    if r.status_code == 200:
        return r.text
    else:
        console.print(f"[error]Error al cambiar turno: [/error]{r.status_code}")
        console.print("Respuesta recibida: ", r.text, style='error')
        return None

def catalogos(token, id_partida):
    r = requests.get(f'{URL}/games/{id_partida}/player/catalogos', headers={'Authorization': f'Bearer {token}'})
    return r.json()

def add_tropa(token, id_partida, tropa, cantidad):
    diccionario = {'tropa': tropa, 'cantidad': cantidad}
    r = requests.post(f'{URL}/games/{id_partida}/player/add_tropa', headers={'Authorization': f'Bearer {token}'}, json=diccionario)
    return r.text

def mover_tropa(token, id_partida, tropa, cantidad, destino):
    diccionario = {'tropa': tropa, 'cantidad': cantidad, 'destino': destino}
    r = requests.put(f'{URL}/games/{id_partida}/player/mover_tropa', headers={'Authorization': f'Bearer {token}'}, json=diccionario)
    return r.json()

def mover_batallon(token, id_partida, destino):
    diccionario = {'destino': destino}
    r = requests.put(f'{URL}/games/{id_partida}/player/mover_batallon', headers={'Authorization': f'Bearer {token}'}, json=diccionario)
    return r.json()

def construir_edificio(token, id_partida, edificio):
    r = requests.post(f'{URL}/games/{id_partida}/player/edificio', headers={'Authorization': f'Bearer {token}'}, json=edificio)
    return r.text

def subir_nivel_edificio(token, id_partida, edificio):
    r = requests.put(f'{URL}/games/{id_partida}/player/edificio', headers={'Authorization': f'Bearer {token}'}, json=edificio)
    return r.text

def obtener_jugadores():
    r = requests.get(f'{URL}/users/jugadores.pkl')
    if r.status_code == 200:
        return r.text
    else:
        console.print(f"[error]Error al actualizar jugadores: [/error]{r.status_code}")
        return None

def obtener_buzones():
    r = requests.get(f'{URL}/users/mail/buzones.pkl')
    if r.status_code == 200:
        return r.text
    else:
        console.print(f"[error]Error al actualizar buzones: [/error]{r.status_code}")
        return None

def subir_jugadores():
    r = requests.post(f'{URL}/users/jugadores.pkl')
    if r.status_code == 200:
        return r.text
    else:
        console.print(f"[error]Error al actualizar jugadores: [/error]{r.status_code}")
        return None

def subir_buzones():
    r = requests.post(f'{URL}/users/mail/buzones.pkl')
    if r.status_code == 200:
        return r.text
    else:
        console.print(f"[error]Error al actualizar buzones: [/error]{r.status_code}")
        return None

def obtener_partidas():
    r = requests.get(f'{URL}/games/partidas.pkl')
    if r.status_code==200:
        return r.text
    else:
        console.print(f"[error]Error al actualizar partidas: [/error]{r.status_code}")
        return None

def subir_partidas():
    r = requests.post(f'{URL}/games/partidas.pkl')
    if r.status_code==200:
        return r.text
    else:
        console.print(f"[error]Error al actualizar partidas: [/error]{r.status_code}")
        return None
def obtener_datos():
    obtener_partidas()
    obtener_buzones()
    obtener_jugadores()

def subir_datos():
    subir_partidas()
    subir_buzones()
    subir_jugadores()

# MENU PRINCIPAL

def menu():


    console.print(Align.center(titulo_md), style='bold bright_yellow', )
    console.print()
    console.print(Align.center(parrafo_texto), style='green italic', )
    console.print()
    console.print(Align.center(despedida_md), style='bold bright_yellow', )

    param('Presione "Enter" para continuar ...', str,
          valores_validos=[''], estilo='info')

    barra_de_progreso(10, 0.1)
    limpiar_pantalla()

    while True:
        table_inicio = Table(show_edge = False, header_style="bold white reverse blue")

        table_inicio.add_column('MENÚ', justify = 'center', style = 'prompt')

        table_inicio.add_row('0. Exit', style = 'dim')
        table_inicio.add_row('1. Registrarse')
        table_inicio.add_row('2. Iniciar sesión')

        console.print(table_inicio)

        console.print()
        choice = param('Eliga una opción: ', int, valores_validos=[0, 1, 2])
        console.print()
        if choice == 1:
            user = param('Usuario: ', str)
            password = param('Contraseña: ', str, is_password=True)
            barra_de_progreso(10, 0.1)
            mostrar_texto(signup(user, password))
            limpiar_pantalla()
        elif choice == 2:
            user = param('Usuario: ', str)
            password = param('Contraseña: ', str, is_password=True)
            log_in = login(user, password)
            barra_de_progreso(10, 0.2)
            if log_in[1]:
                token = log_in[0]
                limpiar_pantalla()
                while True:
                    mostrar_texto(notificaciones(token))

                    table_lobby = Table(show_edge=False, header_style="bold white reverse blue")

                    table_lobby.add_column('LOBBY', justify='center', style='prompt')

                    table_lobby.add_row('0. Log out', style='dim')
                    table_lobby.add_row('1. Jugar')
                    table_lobby.add_row('2. Perfil')

                    console.print(table_lobby)

                    console.print()

                    choice = param('Eliga una opción: ', int, valores_validos=[0, 1, 2])
                    console.print()
                    if choice == 1:
                        limpiar_pantalla()
                        while True:

                            table_para_jugar = Table(show_edge=False, header_style="bold white reverse blue")

                            table_para_jugar.add_column('MENÚ', justify='center', style='prompt')

                            table_para_jugar.add_row('0. Volver', style='dim')
                            table_para_jugar.add_row('1. Crear partida')
                            table_para_jugar.add_row('2. Unirse a partida')

                            console.print(table_para_jugar)

                            console.print()

                            choice = param('Eliga una opción: ', int, valores_validos=[0, 1, 2])
                            console.print()
                            if choice == 1:
                                limpiar_pantalla()
                                while True:

                                    table_alcance_partida = Table(show_edge=False, header_style="bold white reverse blue")

                                    table_alcance_partida.add_column('ALCANCE DE LA PARTIDA', justify='center', style='prompt')

                                    table_alcance_partida.add_row('1. Pública')
                                    table_alcance_partida.add_row('2. Privada')

                                    console.print(table_alcance_partida)

                                    console.print()

                                    privada = True if param('Elija una opción: ', int, valores_validos=[1, 2]) == 2 else False
                                    limpiar_pantalla()

                                    if privada:
                                        amigos = obtener_amigos(token)
                                        if amigos != []:
                                            # Todo: hacer una tabla
                                            mostrar_texto(amigos, enumerado=True)
                                            valores_validos = [n for n in range(0, len(amigos) + 1)]
                                            amigo = param('Que amigo desea invitar: ', int,
                                                          valores_validos=valores_validos)
                                            invitado = amigos[amigo - 1]
                                        else:
                                            mostrar_texto('Todavía no tienes amigos')
                                            limpiar_pantalla()
                                            break
                                    else:
                                        invitado = None

                                    table_tipo_partida = Table(show_edge=False, header_style="bold white reverse blue")

                                    table_tipo_partida.add_column('TIPOS DE PARTIDA', justify='center', style='prompt')

                                    table_tipo_partida.add_row('0. Volver', style='dim')
                                    table_tipo_partida.add_row('1. Partida personalizada')
                                    table_tipo_partida.add_row('2. Partida predefinida')

                                    console.print(table_tipo_partida)

                                    console.print()

                                    choice = param('Eliga una opción: ', int, valores_validos=[0, 1, 2])
                                    console.print()
                                    if choice == 1:
                                        tamanyo = param('Introduce el tamaño del mapa (min.3, max. 50): ', int, valores_validos=[3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50])
                                        while True:
                                            terrenos = param('Introduce los terrenos del mapa separados por comas (min. 2): ', str)
                                            if len(terrenos.split(',')) < 2:
                                                console.print('Error: Debe introducir al menos 2 tipos de terreno.', style = 'warning')
                                                continue

                                            copia_terrenos = deepcopy(TERRENOS_JUEGO)
                                            for terreno in terrenos.split(','):
                                                if terreno.strip().lower() in copia_terrenos:
                                                    copia_terrenos.remove(terreno.strip().lower())
                                                else:
                                                    if terreno.strip().lower() in TERRENOS_JUEGO:
                                                        console.print(
                                                            f'[error]Error: El tipo de terreno "{terreno}" se ha introducido más de una vez.[/error] \n[info]Ayuda: La multiplicidad máxima de cada terreno es 1.[info]',)
                                                    else:
                                                        console.print(f'Error: El tipo de terreno "{terreno}" no existe en el juego.', style = 'error')

                                                    console.print()

                                                    table_terrenos = Table(box = box.ROUNDED, border_style = 'bold', header_style="bold white reverse blue")
                                                    table_terrenos.add_column('TIPOS DE TERRENOS DISPONIBLES', justify='center', style='info')
                                                    for tereno in TERRENOS_JUEGO:
                                                        table_terrenos.add_row(tereno.capitalize())

                                                    console.print(table_terrenos)
                                                    console.print()

                                                    break
                                            else:
                                                break

                                        reino = param('Introduce el nombre de tu reino: ', str)

                                        barra_de_progreso(10, 0.1)
                                        mostrar_texto(crear_partida(token, privada, reino, invitado, tamanyo, terrenos))
                                        limpiar_pantalla()
                                        break
                                    elif choice == 2:
                                        reino = param('Introduce el nombre de tu reino: ', str)
                                        barra_de_progreso(10, 0.1)
                                        mostrar_texto(crear_partida(token, privada, reino, invitado))
                                        limpiar_pantalla()
                                        break
                                    elif choice == 0:
                                        limpiar_pantalla()
                                        break
                            elif choice == 2:
                                limpiar_pantalla()
                                while True:

                                    table_que_jugar = Table(show_edge=False, header_style="bold white reverse blue")

                                    table_que_jugar.add_column('DÓNDE QUIERE JUGAR', justify='center', style='prompt')

                                    table_que_jugar.add_row('0. Volver', style='dim')
                                    table_que_jugar.add_row('1. Unirse a una nueva partida')
                                    table_que_jugar.add_row('2. Empezar/Continuar una partida a la que ya se ha unido')

                                    console.print(table_que_jugar)

                                    console.print()

                                    choice = param('Elija una opción: ', int, valores_validos=[0, 1, 2])
                                    console.print()
                                    if choice == 1:
                                        # Todo: hacer una tabla
                                        publicas = partidas_publicas(token)
                                        partidas_str = [partida for partida in publicas.values()]
                                        mostrar_texto(partidas_str, enumerado=True)
                                        id_partida = param('Introduzca el id de la partida a la que desea unirse: ',
                                                           str)
                                        reino = param('Introduce el nombre de tu reino: ', str)
                                        barra_de_progreso(10, 0.2)
                                        mostrar_texto(unirse_partida(token, id_partida, reino))
                                        mostrar_texto(iniciar_partida(token, id_partida))
                                        limpiar_pantalla()
                                    elif choice == 2:
                                        # Todo: hacer una tabla
                                        user_partidas = mis_partidas(token)
                                        if user_partidas != {}:
                                            str_partidas = [partida for partida in user_partidas.values()]
                                            mostrar_texto(str_partidas)
                                        else:
                                            mostrar_texto('Todavía no te has unido a ninguna partida')
                                            limpiar_pantalla()
                                            continue
                                        id_user_partida = param('Introduzca el id de la partida: ', str)
                                        barra_de_progreso(10, 0.1)
                                        estado_partida = get_estado_partida(token, id_user_partida)
                                        if estado_partida == 'Empezada':
                                            while True:
                                                if get_estado_jugador(token, id_user_partida):
                                                    # Todo: usar markdown
                                                    mostrar_texto('Bienvenido a Kingdom Craft')
                                                    limpiar_pantalla()
                                                    while get_estado_jugador(token, id_user_partida) == True:

                                                        table_opciones_partida = Table(show_edge=False, header_style="bold white reverse blue")

                                                        table_opciones_partida.add_column('OPCIONES DURANTE LA PARTIDA', justify='center', style='prompt')

                                                        table_opciones_partida.add_row('0. Exit', style='dim')
                                                        table_opciones_partida.add_row('1. Ver zona')
                                                        table_opciones_partida.add_row('2. Ver mis recursos')
                                                        table_opciones_partida.add_row('3. Ver mapa')
                                                        table_opciones_partida.add_row('4. Finalizar mi turno')

                                                        console.print(table_opciones_partida)

                                                        console.print()

                                                        choice = param('Eliga una opción: ', int, valores_validos=[0, 1, 2, 3, 4])
                                                        console.print()
                                                        if choice == 1:
                                                            coordenada = to_tuple()
                                                            zona, estado = ver_zona(token, id_user_partida, coordenada)
                                                            if estado == 200:
                                                                while True:
                                                                    if zona[1]:
                                                                        table_opciones_dentro_zona = Table(show_edge=False, header_style="bold white reverse blue")

                                                                        table_opciones_dentro_zona.add_column(f'OPCIONES DENTRO DE LA ZONA', justify='center', style='prompt')

                                                                        table_opciones_dentro_zona.add_row('0. Volver', style='dim')
                                                                        table_opciones_dentro_zona.add_row('1. Añadir tropa')
                                                                        table_opciones_dentro_zona.add_row('2. Mover batallón')
                                                                        table_opciones_dentro_zona.add_row('3. Construir edificio')
                                                                        table_opciones_dentro_zona.add_row('4. Finalizar mi turno')

                                                                        console.print(table_opciones_dentro_zona)

                                                                        console.print()

                                                                        console.print(zona[0], style = 'prompt')

                                                                        choice = param('Eliga una opción: ', int,
                                                                                       valores_validos=[0, 1, 2, 3])
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

