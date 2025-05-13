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

# MENU PRINCIPAL

