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
from rich import box

from mapa import Mapa

# Configuracion de rich
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
console = Console(theme=temas_predefinidos)

URL = 'https://sergioazorinjulian.pythonanywhere.com/'
TERRENOS_JUEGO = Mapa.terrenos_disponibles


# -----------------FUNCIONES-----------------
def partida_custom():
    """
    Permite al usuario configurar una partida personalizada eligiendo el tamaño del mapa y los tipos de terrenos.

    Parámetros
    ----------
    Ninguno

    Returns
    -------
    tuple
        Una tupla que contiene el tamaño del mapa (int) y los terrenos seleccionados (str).

    Raises
    ------
    None
    """
    size = param('Introduce el tamaño del mapa (min.3, max.50): ', int, valores_validos=[i for i in range(3, 51)],
                 estilo='input')

    mostrar_terrenos_en_tabla()

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

                mostrar_terrenos_en_tabla()

                break
        else:
            break

    return size, terrenos


def mostrar_terrenos_en_tabla():
    """
    Muestra una tabla con los tipos de terrenos disponibles utilizando Rich.

    Parámetros
    ----------
    Ninguno

    Returns
    -------
    None
        No retorna ningún valor.

    Raises
    ------
    None
        No lanza ninguna excepción.
    """
    console.print()
    table_terrenos = Table(box=box.ROUNDED, border_style='bold', header_style="bold white reverse blue")
    table_terrenos.add_column('TIPOS DE TERRENOS DISPONIBLES', justify='center', style='info')
    for terreno in TERRENOS_JUEGO:
        table_terrenos.add_row(terreno.capitalize())
    console.print(table_terrenos)
    console.print()


def to_tuple():
    """
    Solicita al usuario que introduzca dos coordenadas separadas por una coma y las devuelve como una tupla de enteros.

    Parámetros
    ----------
    Ninguno

    Returns
    -------
    tuple
        Tupla de dos enteros que representan la fila y la columna introducidas por el usuario.

    Raises
    ------
    ValueError
        Si la entrada no puede convertirse a enteros.
    TypeError
        Si la entrada no es válida o no se puede procesar.
    """
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
    """
    Solicita un parámetro al usuario, validando tipo, longitud mínima y valores permitidos.

    Parámetros
    ----------
    nombre : str
        Mensaje que se muestra al usuario solicitando la entrada.
    tipo : type
        Tipo al que se debe convertir la entrada del usuario.
    lon_min : int, opcional
        Longitud mínima permitida para la entrada (por defecto es 0).
    is_password : bool, opcional
        Si es True, la entrada se oculta como contraseña (por defecto es False).
    valores_validos : list, tuple o None, opcional
        Lista o tupla de valores válidos permitidos para la entrada (por defecto es None).
    estilo : str, opcional
        Estilo de Rich para el prompt de entrada (por defecto es 'input').

    Returns
    -------
    Any
        Valor introducido por el usuario, convertido al tipo especificado.

    Raises
    ------
    ValueError
        Si la entrada no puede convertirse al tipo especificado.
    TypeError
        Si la entrada no es válida o no se puede procesar.
    """
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
    """
    Limpia la pantalla de la terminal según el sistema operativo.

    Parámetros
    ----------
    Ninguno

    Returns
    -------
    None
        No retorna ningún valor.

    Raises
    ------
    None
        No lanza ninguna excepción.
    """
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def crear_tabla(info: dict, dim=True, forma=None) -> None:
    """
    Crea y muestra una tabla usando Rich.

    Esta función toma un diccionario de información y genera una tabla con estilos
    utilizando el módulo Rich. Cada clave del diccionario se convierte en una columna
    de la tabla, y los valores contienen el estilo de la columna en el primer elemento
    y los datos de las filas en el segundo.

    Parameters
    ----------
    info : dict
        Diccionario donde:
        - Las claves son los nombres de las columnas
        - Los valores son listas de dos elementos donde:
          * El primer elemento es el estilo de la columna (str)
          * El segundo elemento es una lista con los datos de las filas
        Ejemplo: {"Nombre": ["prompt", ["Ana", "Luis", "Marta"]]}
    dim : bool, optional
        Controla si la primera fila de la tabla debe tener un estilo dim.
        Si es True, la primera fila tendrá el estilo "dim".
        Por defecto es True.
    forma : Box, optional
        Tipo de borde de la tabla (por ejemplo, box.ROUNDED).
        Si es None, no se aplica ningún estilo de borde específico.
        Por defecto es None.

    Returns
    -------
    None

    Notes
    -----
    La función utiliza el operador de desempaquetado (*) para pasar los elementos
    de una lista como argumentos separados a la función add_row.

    Examples
    --------
    info = {
        "Nombre": ["prompt", ["Ana", "Luis", "Marta"]],
        "Edad": ["success", ["23", "31", "27"]],
        "Ciudad": ["warning", ["Madrid", "Sevilla", "Valencia"]]
        }
    tabla = crear_tabla(info, dim=True)
    console.print(tabla)
    """

    table = Table(show_edge=False, header_style="bold white reverse blue", box=forma) if forma else Table(
        show_edge=False, header_style="bold white reverse blue")

    # Obtener los nombres de las columnas del diccionario
    columnas = list(info.keys())

    # Agregar cada columna a la tabla con su estilo correspondiente
    for columna in columnas:
        # El primer elemento de cada valor es el estilo de la columna
        table.add_column(columna, justify="center", style=info[columna][0])

    # Determinamos el número de filas que habrán basándonos en la longitud de
    # la lista de datos de la primera columna (asumimos que todas las columnas tienen el mismo número de filas)
    num_filas = len(info[columnas[0]][1])

    if num_filas > 0:  # Solo procesamos las filas si hay al menos una ...
        # Agregamos filas a la tabla
        for i in range(num_filas):

            # Creamos una lista con los valores de cada columna en la posición i
            # La comprensión de lista hace lo siguiente:
            # 1. Para cada nombre de columna en la lista 'columnas'
            # 2. Accede a info[columna][1] (la lista de datos para esa columna)
            # 3. Obtiene el elemento en la posición i de esa lista
            # 4. Convierte ese valor a string para poder imprimirlo en la tabla
            fila = [str(info[columna][1][i]) for columna in columnas]

            # Si dim es True y estamos en la primera fila, usamos el estilo 'dim'
            if dim and i == 0:
                # El operador * desempaqueta la lista fila como argumentos separados
                table.add_row(*fila, style="dim")
            else:
                table.add_row(*fila)

    console.print(table)


def mostrar_texto(lista: list[str] | str, enumerado: bool = False, estilo: str = 'prompt') -> None:
    """
    Muestra texto o una lista de textos en la consola, con opción de enumerar y aplicar un estilo.

    Parámetros
    ----------
    lista : list[str] o str
        Texto o lista de textos a mostrar.
    enumerado : bool, opcional
        Si es True, enumera cada elemento de la lista (por defecto es False).
    estilo : str, opcional
        Estilo de Rich para el texto mostrado (por defecto es 'prompt').

    Returns
    -------
    None
        No retorna ningún valor.

    Raises
    ------
    None
        No lanza ninguna excepción.
    """
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
    """
    Muestra una tabla de espera con opciones de menú utilizando Rich.

    Parámetros
    ----------
    Ninguno

    Returns
    -------
    None
        No retorna ningún valor.

    Raises
    ------
    None
        No lanza ninguna excepción.
    """
    table_espera = Table(show_edge=False, header_style="bold white reverse blue")
    table_espera.add_column('MENÚ', justify='center', style='prompt')
    table_espera.add_row('0. Volver', style='dim')
    table_espera.add_row('1. Recargar')
    console.print(table_espera)
    console.print()


# ------------REQUESTS------------
# AUTENTICACIÓN
def signup(user, password):
    """
    Registra un nuevo usuario en el sistema.

    Parámetros
    ----------
    user : str
        Nombre de usuario para el registro.
    password : str
        Contraseña para el registro.

    Returns
    -------
    str
        Respuesta del servidor tras intentar registrar el usuario.
    """
    r = requests.post(f'{URL}/auth/signup?user={user}&password={password}')
    return r.text


def login(user, password):
    """
    Inicia sesión de un usuario en el sistema.

    Parámetros
    ----------
    user : str
        Nombre de usuario.
    password : str
        Contraseña del usuario.

    Returns
    -------
    tuple
        Una tupla que contiene la respuesta del servidor y un booleano que indica si el inicio de sesión fue exitoso.
    """
    r = requests.get(f'{URL}/auth/login?user={user}&password={password}')
    if r.status_code == 200:
        return r.text, True
    return r.text, False


# USERS -ranking
#   SQL
def ver_ranking(token):
    """
    Obtiene el ranking de usuarios desde el servidor.

    Parámetros
    ----------
    token : str
        Token de autenticación del usuario.

    Returns
    -------
    dict
        Diccionario con la información del ranking de usuarios.
    """
    r = requests.get(f'{URL}/users/ranking', headers={'Authorization': f'Bearer {token}'})
    ranking = r.json()
    return ranking


# USERS - BUZON
def notificaciones(token):
    """
    Obtiene las notificaciones del buzón del usuario desde el servidor.

    Parámetros
    ----------
    token : str
        Token de autenticación del usuario.

    Returns
    -------
    str
        Texto con las notificaciones recibidas.
    """
    r = requests.get(f'{URL}/users/mail/notificaciones', headers={'Authorization': f'Bearer {token}'})
    return r.text


def obtener_buzon(token):
    """
    Obtiene los mensajes del buzón del usuario desde el servidor.

    Parámetros
    ----------
    token : str
        Token de autenticación del usuario.

    Returns
    -------
    list
        Lista de mensajes recibidos por el usuario.

    Raises
    ------
    requests.RequestException
        Si ocurre un error en la solicitud HTTP.
    """
    r = requests.get(f'{URL}/users/mail', headers={'Authorization': f'Bearer {token}'})
    mensajes = r.json()
    return mensajes


def marcar_leido(token):
    """
    Marca como leídos todos los mensajes del buzón del usuario.

    Parámetros
    ----------
    token : str
        Token de autenticación del usuario.

    Returns
    -------
    str
        Respuesta del servidor tras marcar los mensajes como leídos.

    Raises
    ------
    requests.RequestException
        Si ocurre un error en la solicitud HTTP.
    """
    r = requests.put(f'{URL}/users/mail', headers={'Authorization': f'Bearer {token}'})
    return r.text


# USERS - AMIGOS
def obtener_amigos(token):
    """
    Obtiene la lista de amigos del usuario autenticado.

    Parámetros
    ----------
    token : str
        Token de autenticación del usuario.

    Returns
    -------
    list
        Lista de amigos del usuario.

    Raises
    ------
    requests.RequestException
        Si ocurre un error en la solicitud HTTP.
    """
    r = requests.get(f'{URL}/users/friends', headers={'Authorization': f'Bearer {token}'})
    amigos = r.json()
    return amigos


def obtener_solicitudes(token):
    """
    Obtiene la lista de solicitudes de amistad recibidas por el usuario autenticado.

    Parámetros
    ----------
    token : str
        Token de autenticación del usuario.

    Returns
    -------
    list
        Lista de solicitudes de amistad.

    Raises
    ------
    requests.RequestException
        Si ocurre un error en la solicitud HTTP.
    """
    r = requests.get(f'{URL}/users/friend-requests', headers={'Authorization': f'Bearer {token}'})
    solicitudes = r.json()
    return solicitudes


def enviar_solicitud(token, usuario):
    """
    Envía una solicitud de amistad a un usuario.

    Parámetros
    ----------
    token : str
        Token de autenticación del usuario.
    usuario : str
        Nombre de usuario al que se envía la solicitud.

    Returns
    -------
    str
        Respuesta del servidor tras enviar la solicitud.

    Raises
    ------
    requests.RequestException
        Si ocurre un error en la solicitud HTTP.
    """
    r = requests.post(f'{URL}/users/friend-requests?id_solicitud={usuario}',
                      headers={'Authorization': f'Bearer {token}'})
    return r.text


def aceptar_solicitud(token, nuevo_amigo):
    """
    Acepta una solicitud de amistad recibida.

    Parámetros
    ----------
    token : str
        Token de autenticación del usuario.
    nuevo_amigo : str
        Nombre de usuario cuya solicitud se acepta.

    Returns
    -------
    str
        Respuesta del servidor tras aceptar la solicitud.

    Raises
    ------
    requests.RequestException
        Si ocurre un error en la solicitud HTTP.
    """
    r = requests.post(f'{URL}/users/friend-requests/{nuevo_amigo}/accept', headers={'Authorization': f'Bearer {token}'})
    return r.text


def rechazar_solicitud(token, usuario):
    """
    Rechaza una solicitud de amistad recibida.

    Parámetros
    ----------
    token : str
        Token de autenticación del usuario.
    usuario : str
        Nombre de usuario cuya solicitud se rechaza.

    Returns
    -------
    str
        Respuesta del servidor tras rechazar la solicitud.

    Raises
    ------
    requests.RequestException
        Si ocurre un error en la solicitud HTTP.
    """
    r = requests.post(f'{URL}/users/friend-requests/{usuario}/reject', headers={'Authorization': f'Bearer {token}'})
    return r.text


def invitaciones_privadas(token):
    """
    Obtiene las invitaciones de partidas privadas recibidas por el usuario.

    Parámetros
    ----------
    token : str
        Token de autenticación del usuario.

    Returns
    -------
    dict
        Diccionario con las invitaciones de partidas privadas.

    Raises
    ------
    requests.RequestException
        Si ocurre un error en la solicitud HTTP.
    """
    r = requests.get(f'{URL}/users/game_requests', headers={'Authorization': f'Bearer {token}'})
    invitaciones = r.json()
    return invitaciones


# MY GAMES
def mis_partidas(token):
    """
    Obtiene las partidas en las que el usuario autenticado está participando.

    Parámetros
    ----------
    token : str
        Token de autenticación del usuario.

    Returns
    -------
    dict
        Diccionario con la información de las partidas del usuario.

    Raises
    ------
    requests.RequestException
        Si ocurre un error en la solicitud HTTP.
    """
    r = requests.get(f'{URL}/users/my_games', headers={'Authorization': f'Bearer {token}'})
    partidas = r.json()
    return partidas


# PARTIDA
def obtener_ganador(token, id_partida):
    """
    Obtiene el ganador de una partida finalizada.

    Parámetros
    ----------
    token : str
        Token de autenticación del usuario.
    id_partida : str
        Identificador de la partida.

    Returns
    -------
    str
        Mensaje indicando el ganador de la partida.

    Raises
    ------
    requests.RequestException
        Si ocurre un error en la solicitud HTTP.
    """
    r = requests.get(f'{URL}/games/{id_partida}/winner', headers={'Authorization': f'Bearer {token}'})
    return f'La partida ya ha finalizado. \nEl ganador ha sido {r.text}'


def crear_partida(token, privada, reino, invitado=None, size=3, terrenos=None):
    """
    Crea una nueva partida enviando los parámetros al servidor.

    Parámetros
    ----------
    token : str
        Token de autenticación del usuario.
    privada : bool
        Indica si la partida es privada.
    reino : str
        Nombre del reino del usuario.
    invitado : str, opcional
        Nombre del usuario invitado a la partida (solo para partidas privadas).
    size : int, opcional
        Tamaño del mapa de la partida (por defecto es 3).
    terrenos : any, opcional
        Tipos de terrenos seleccionados para la partida.

    Returns
    -------
    str
        Respuesta del servidor tras crear la partida.
    """
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
    """
    Obtiene la lista de partidas públicas disponibles desde el servidor.

    Parámetros
    ----------
    token : str
        Token de autenticación del usuario.

    Returns
    -------
    dict
        Diccionario con la información de las partidas públicas.
    """
    r = requests.get(f'{URL}/games', headers={'Authorization': f'Bearer {token}'})
    publicas = r.json()
    return publicas


# /game/<id>/
def unirse_partida(token, id_partida, reino):
    """
    Permite a un usuario unirse a una partida existente.

    Parámetros
    ----------
    token : str
        Token de autenticación del usuario.
    id_partida : str
        Identificador de la partida a la que se desea unir.
    reino : str
        Nombre del reino del usuario.

    Returns
    -------
    str
        Respuesta del servidor tras intentar unirse a la partida.

    Raises
    ------
    requests.RequestException
        Si ocurre un error en la solicitud HTTP.
    """
    r = requests.put(f'{URL}/games/{id_partida}/join?reino={reino}', headers={'Authorization': f'Bearer {token}'})
    return r.text


def iniciar_partida(token, id_partida):
    """
    Inicia una partida existente.

    Parámetros
    ----------
    token : str
        Token de autenticación del usuario.
    id_partida : str
        Identificador de la partida a iniciar.

    Returns
    -------
    str
        Respuesta del servidor tras intentar iniciar la partida.

    Raises
    ------
    requests.RequestException
        Si ocurre un error en la solicitud HTTP.
    """
    r = requests.put(f'{URL}/games/{id_partida}/start', headers={'Authorization': f'Bearer {token}'})
    return r.text


def cancelar_partida(token, id_partida):
    """
    Cancela una partida existente en el servidor.

    Parámetros
    ----------
    token : str
        Token de autenticación del usuario.
    id_partida : str
        Identificador de la partida a cancelar.

    Returns
    -------
    str
        Respuesta del servidor tras intentar cancelar la partida.

    Raises
    ------
    requests.RequestException
        Si ocurre un error en la solicitud HTTP.
    """
    r = requests.post(f'{URL}/games/{id_partida}/cancel', headers={'Authorization': f'Bearer {token}'})
    return r.text


def get_estado_partida(token, id_partida):
    """
    Obtiene el estado actual de una partida.

    Parámetros
    ----------
    token : str
        Token de autenticación del usuario.
    id_partida : str
        Identificador de la partida.

    Returns
    -------
    tuple
        Una tupla que contiene el estado de la partida (str) y el código de estado HTTP (int).

    Raises
    ------
    requests.RequestException
        Si ocurre un error en la solicitud HTTP.
    """
    r = requests.get(f'{URL}/games/{id_partida}/game_state', headers={'Authorization': f'Bearer {token}'})
    estado = r.text
    return estado, r.status_code


def get_estado_jugador(token, id_partida):
    """
    Obtiene el estado del jugador en una partida específica.

    Parámetros
    ----------
    token : str
        Token de autenticación del usuario.
    id_partida : str
        Identificador de la partida.

    Returns
    -------
    dict
        Diccionario con el estado del jugador.

    Raises
    ------
    requests.RequestException
        Si ocurre un error en la solicitud HTTP.
    """
    r = requests.get(f'{URL}/games/{id_partida}/player_state', headers={'Authorization': f'Bearer {token}'})
    estado = r.json()
    return estado


# /game/<id>/player
def ver_zona(token, id_partida, coordenada):
    """
    Obtiene la información de una zona específica del mapa de la partida.

    Parámetros
    ----------
    token : str
        Token de autenticación del usuario.
    id_partida : str
        Identificador de la partida.
    coordenada : any
        Coordenada de la zona a consultar.

    Returns
    -------
    tuple
        Una tupla que contiene el diccionario con la información de la zona y el código de estado HTTP.

    Raises
    ------
    requests.RequestException
        Si ocurre un error en la solicitud HTTP.
    """
    diccionario = {'zona': coordenada}
    r = requests.post(f'{URL}/games/{id_partida}/player/ver_zona', headers={'Authorization': f'Bearer {token}'},
                      json=diccionario)
    zona = r.json()
    return zona, r.status_code


def ver_recursos(token, id_partida):
    """
    Obtiene los recursos del jugador en una partida específica.

    Parámetros
    ----------
    token : str
        Token de autenticación del usuario.
    id_partida : str
        Identificador de la partida.

    Returns
    -------
    dict
        Diccionario con los recursos del jugador.

    Raises
    ------
    requests.RequestException
        Si ocurre un error en la solicitud HTTP.
    """
    r = requests.get(f'{URL}/games/{id_partida}/player/ver_recursos', headers={'Authorization': f'Bearer {token}'})
    return r.json()


def ver_mapa(token, id_partida):
    """
    Obtiene el mapa de la partida para el jugador autenticado.

    Parámetros
    ----------
    token : str
        Token de autenticación del usuario.
    id_partida : str
        Identificador de la partida.

    Returns
    -------
    str or None
        Mapa de la partida en formato texto si la solicitud es exitosa, None en caso de error.

    Raises
    ------
    requests.RequestException
        Si ocurre un error en la solicitud HTTP.
    """
    r = requests.get(f'{URL}/games/{id_partida}/player/ver_mapa', headers={'Authorization': f'Bearer {token}'})
    if r.status_code == 200:
        return r.text
    else:
        console.print(f"[error]Error al obtener el mapa: [/error]{r.status_code}")
        console.print("Respuesta recibida: ", r.text, style='error')
        return None


def cambiar_turno(token, id_partida):
    """
    Cambia el turno del jugador en una partida específica.

    Parámetros
    ----------
    token : str
        Token de autenticación del usuario.
    id_partida : str
        Identificador de la partida.

    Returns
    -------
    str or None
        Respuesta del servidor si la operación es exitosa, None en caso de error.

    Raises
    ------
    requests.RequestException
        Si ocurre un error en la solicitud HTTP.
    """
    r = requests.put(f'{URL}/games/{id_partida}/player/cambiar_turno', headers={'Authorization': f'Bearer {token}'})
    if r.status_code == 200:
        return r.text
    else:
        console.print(f"[error]Error al cambiar turno: [/error]{r.status_code}")
        console.print("Respuesta recibida: ", r.text, style='error')
        return None


def catalogos(token, id_partida):
    """
    Obtiene los catálogos de tropas y edificios disponibles para el jugador en una partida.

    Parámetros
    ----------
    token : str
        Token de autenticación del usuario.
    id_partida : str
        Identificador de la partida.

    Returns
    -------
    dict
        Diccionario con los catálogos de tropas y edificios.

    Raises
    ------
    requests.RequestException
        Si ocurre un error en la solicitud HTTP.
    """
    r = requests.get(f'{URL}/games/{id_partida}/player/catalogos', headers={'Authorization': f'Bearer {token}'})
    return r.json()


def add_tropa(token, id_partida, tropa, cantidad):
    """
    Añade una cantidad específica de una tropa al jugador en una partida.

    Parámetros
    ----------
    token : str
        Token de autenticación del usuario.
    id_partida : str
        Identificador de la partida.
    tropa : str
        Nombre de la tropa a añadir.
    cantidad : int
        Cantidad de tropas a añadir.

    Returns
    -------
    str
        Respuesta del servidor tras intentar añadir la tropa.

    Raises
    ------
    requests.RequestException
        Si ocurre un error en la solicitud HTTP.
    """
    diccionario = {'tropa': tropa, 'cantidad': cantidad}
    r = requests.post(f'{URL}/games/{id_partida}/player/add_tropa', headers={'Authorization': f'Bearer {token}'},
                      json=diccionario)
    return r.text


def mover_tropa(token, id_partida, tropa, cantidad, destino):
    """
    Mueve una cantidad específica de una tropa a una coordenada destino en una partida.

    Parámetros
    ----------
    token : str
        Token de autenticación del usuario.
    id_partida : str
        Identificador de la partida.
    tropa : str
        Nombre de la tropa a mover.
    cantidad : int
        Cantidad de tropas a mover.
    destino : any
        Coordenada de destino a la que se moverán las tropas.

    Returns
    -------
    tuple
        Una tupla que contiene la respuesta del servidor en formato JSON y el código de estado HTTP.

    Raises
    ------
    requests.RequestException
        Si ocurre un error en la solicitud HTTP.
    """
    diccionario = {'tropa': tropa, 'cantidad': cantidad, 'destino': destino}
    r = requests.put(f'{URL}/games/{id_partida}/player/mover_tropa', headers={'Authorization': f'Bearer {token}'},
                     json=diccionario)
    return r.json(), r.status_code


def mover_batallon(token, id_partida, destino):
    """
    Mueve un batallón completo a una coordenada destino en una partida.

    Parámetros
    ----------
    token : str
        Token de autenticación del usuario.
    id_partida : str
        Identificador de la partida.
    destino : any
        Coordenada de destino a la que se moverá el batallón.

    Returns
    -------
    tuple
        Una tupla que contiene la respuesta del servidor en formato JSON y el código de estado HTTP.

    Raises
    ------
    requests.RequestException
        Si ocurre un error en la solicitud HTTP.
    """
    diccionario = {'destino': destino}
    r = requests.put(f'{URL}/games/{id_partida}/player/mover_batallon', headers={'Authorization': f'Bearer {token}'},
                     json=diccionario)
    return r.json(), r.status_code


def mover_batallon(token, id_partida, destino):
    """
    Mueve un batallón completo a una coordenada destino en una partida.

    Parámetros
    ----------
    token : str
        Token de autenticación del usuario.
    id_partida : str
        Identificador de la partida.
    destino : any
        Coordenada de destino a la que se moverá el batallón.

    Returns
    -------
    tuple
        Una tupla que contiene la respuesta del servidor en formato JSON y el código de estado HTTP.
    """
    diccionario = {'destino': destino}
    r = requests.put(f'{URL}/games/{id_partida}/player/mover_batallon', headers={'Authorization': f'Bearer {token}'},
                     json=diccionario)
    return r.json(), r.status_code


def construir_edificio(token, id_partida, edificio):
    """
    Construye un edificio en la partida para el jugador autenticado.

    Parámetros
    ----------
    token : str
        Token de autenticación del usuario.
    id_partida : str
        Identificador de la partida.
    edificio : any
        Información del edificio a construir.

    Returns
    -------
    str
        Respuesta del servidor tras intentar construir el edificio.
    """
    r = requests.post(f'{URL}/games/{id_partida}/player/edificio', headers={'Authorization': f'Bearer {token}'},
                      json=edificio)
    return r.text


def subir_nivel_edificio(token, id_partida, edificio):
    """
    Sube el nivel de un edificio en la partida para el jugador autenticado.

    Parámetros
    ----------
    token : str
        Token de autenticación del usuario.
    id_partida : str
        Identificador de la partida.
    edificio : any
        Información del edificio a subir de nivel.

    Returns
    -------
    str
        Respuesta del servidor tras intentar subir el nivel del edificio.
    """
    r = requests.put(f'{URL}/games/{id_partida}/player/edificio', headers={'Authorization': f'Bearer {token}'},
                     json=edificio)
    return r.text


def combatir(token, id_partida, atacantes_pos, defensores_pos):
    """
    Realiza una acción de combate entre atacantes y defensores en una partida.

    Parámetros
    ----------
    token : str
        Token de autenticación del usuario.
    id_partida : str
        Identificador de la partida.
    atacantes_pos : any
        Información sobre los atacantes.
    defensores_pos : any
        Información sobre los defensores.

    Returns
    -------
    dict
        Respuesta del servidor en formato JSON con el resultado del combate.
    """
    diccionario = {
        'atacantes': atacantes_pos,
        'defensores': defensores_pos
    }
    r = requests.put(f'{URL}/games/{id_partida}/player/combatir', headers={'Authorization': f'Bearer {token}'},
                     json=(diccionario))
    return r.json()


def subir_partidas():
    """
    Sube el archivo de partidas al servidor.

    Returns
    -------
    str or None
        Respuesta del servidor si la actualización fue exitosa, o None si ocurrió un error.

    Raises
    ------
    requests.RequestException
        Si ocurre un error en la solicitud HTTP.
    """
    r = requests.post(f'{URL}/games/partidas.pkl')
    if r.status_code == 200:
        return r.text
    else:
        console.print(f"[error]Error al actualizar partidas: [/error]{r.status_code}")
        return None


def jugar(token):
    """
    Muestra y gestiona el menú principal de juego, permitiendo crear partidas, unirse a partidas existentes o ver el ranking.

    Parámetros
    ----------
    token : str
        Token de autenticación del usuario.

    Returns
    -------
    None
        No retorna ningún valor.

    Raises
    ------
    Exception
        Puede lanzar excepciones si ocurre un error inesperado durante la ejecución de las operaciones del menú.
    """
    limpiar_pantalla()
    while True:
        menu = {"Menu": ["prompt", ["0. Volver", "1. Crear partida", "2. Unirse a partida", "3. Ver ranking"]]}
        crear_tabla(menu, dim=True)

        choice = param('Eliga una opción: ', int, valores_validos=[0, 1, 2, 3])
        console.print()

        if choice == 1:
            limpiar_pantalla()
            while True:
                op1 = {"Crear partida": ["success", ["1. Pública", "2. Privada"]]}
                crear_tabla(op1, dim=True)

                console.print()

                privada = True if param('Elija una opción: ', int, valores_validos=[1, 2]) == 2 else False
                limpiar_pantalla()

                if privada:
                    amigos = obtener_amigos(token)
                    if amigos != []:
                        # Todo: mostrar mejor la lista de amigos
                        mostrar_texto(amigos, enumerado=True)
                        valores_validos = [n for n in range(0, len(amigos) + 1)]
                        amigo = param('¿A qué amigo desea invitar?: ', int, valores_validos=valores_validos)
                        invitado = amigos[amigo - 1]
                        limpiar_pantalla()
                    else:
                        mostrar_texto('Todavía no tienes amigos')
                        limpiar_pantalla()
                        break
                else:
                    invitado = None
                tipo = {
                    "Tipo de partida": ["prompt", ["0. Volver", "1. Partida personalizada", "2. Partida predefinida"]]}
                crear_tabla(tipo, dim=True)

                console.print()

                choice = param('Eliga una opción: ', int, valores_validos=[0, 1, 2])
                console.print()

                if choice == 1:
                    size, terrenos = partida_custom()
                    reino = param('Introduce el nombre de tu reino: ', str)
                    # (10, 0.1)
                    mostrar_texto(crear_partida(token, privada, reino, invitado, size, terrenos))
                    limpiar_pantalla()
                    break
                elif choice == 2:
                    reino = param('Introduce el nombre de tu reino: ', str)
                    # (10, 0.1)
                    mostrar_texto(crear_partida(token, privada, reino, invitado))
                    limpiar_pantalla()
                    break
                elif choice == 0:
                    limpiar_pantalla()
                    break
        elif choice == 2:
            limpiar_pantalla()
            while True:
                op2 = {"Dónde quiere jugar": ["prompt", ["0. volver", "1. Unirse a una nueva partida",
                                                         "2. Empezar/Continuar una partida a la que ya se ha unido"]]}
                crear_tabla(op2, dim=True)

                console.print()

                choice = param('Elija una opción: ', int, valores_validos=[0, 1, 2])
                console.print()

                if choice == 1:
                    # Todo: mostrar las partidas
                    publicas = partidas_publicas(token)
                    partidas_str = [partida for partida in publicas.values()]
                    mostrar_texto(partidas_str, enumerado=True)
                    # Todo: si nos metemos a una partida que no existe nos sale un error
                    id_partida = param('Introduzca el id de la partida a la que desea unirse (o 0 para volver): ', str)
                    if id_partida == '0':
                        limpiar_pantalla()
                        continue
                    reino = param('Introduce el nombre de tu reino: ', str)
                    mostrar_texto(unirse_partida(token, id_partida, reino))
                    mostrar_texto(iniciar_partida(token, id_partida))
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
                    id_user_partida = param('Introduzca el id de la partida: ', str)

                    while True:
                        estado_partida, r_estado = get_estado_partida(token, id_user_partida)
                        if r_estado == 200:

                            if estado_partida == 'Empezada':
                                estado_jugador = get_estado_jugador(token, id_user_partida)
                                if estado_jugador:
                                    if 'catalogos_dict' not in locals().keys():  # Creamos el catalogo si no existe
                                        catalogos_dict = catalogos(token, id_user_partida)
                                    limpiar_pantalla()

                                    op = {"Opciones durante la partida": ["prompt", ["0. Exit", "1. Ver zona",
                                                                                     "2. ver mis recursos",
                                                                                     "3. Ver mapa",
                                                                                     "4. Finalizar mi turno"]]}
                                    crear_tabla(op, dim=True)

                                    console.print()

                                    choice = param('Eliga una opción: ', int, valores_validos=[0, 1, 2, 3, 4])
                                    console.print()

                                    if choice == 1:
                                        coordenada = to_tuple()
                                        while True:
                                            zona, estado = ver_zona(token, id_user_partida, coordenada)
                                            if estado == 200:
                                                if zona[1]:
                                                    dict = {"Opciones dentro de la zona": ["success", ["0. Volver",
                                                                                                       "1. Añadir tropa",
                                                                                                       "2. Mover tropa",
                                                                                                       "3. Mover batallón",
                                                                                                       "4. Contruir edificio",
                                                                                                       "5. Subir de nivel edificio"]]}
                                                    crear_tabla(dict, dim=True)

                                                    console.print()

                                                    console.print(zona[0], style='prompt')

                                                    choice = param('Eliga una opción: ', int,
                                                                   valores_validos=[0, 1, 2, 3, 4, 5])
                                                    match choice:
                                                        case 0:
                                                            limpiar_pantalla()
                                                            break
                                                        case 1:
                                                            mostrar_texto(catalogos_dict['tropas']['catalogo'])
                                                            tropa = param('Introduzca el nombre de la tropa: ', str,
                                                                          valores_validos=catalogos_dict['tropas'][
                                                                              'valores_validos'])
                                                            cantidad = param('Introduzca la cantidad: ', int)
                                                            mostrar_texto(
                                                                add_tropa(token, id_user_partida, tropa, cantidad))
                                                            limpiar_pantalla()
                                                        case 2:
                                                            tropa = param('Introduzca el nombre de la tropa: ', str,
                                                                          valores_validos=catalogos_dict['tropas'][
                                                                              'valores_validos'])
                                                            cantidad = param('Introduzca la cantidad: ', int)
                                                            destino = to_tuple()
                                                            salida, estado = mover_tropa(token, id_user_partida, tropa,
                                                                                         cantidad, destino)
                                                            if isinstance(salida,
                                                                          list):  # No se a podido mover la tropa, saltar opcion de combate
                                                                mostrar_texto(salida[0])
                                                                dict = {"Opciones": ["prompt",
                                                                                     ["0. Abortar",
                                                                                      "1. Combatir (Se enviarán a todas las tropas de la región)"]]}

                                                                crear_tabla(dict, dim=False)

                                                                console.print()

                                                                choice = param('Eliga una opción: ', int,
                                                                               valores_validos=[0, 1])
                                                                if choice == 1:
                                                                    salida = combatir(token, id_user_partida,
                                                                                      coordenada, destino)
                                                                    mostrar_texto(salida['texto'])
                                                                    limpiar_pantalla()
                                                                    if salida['estado'] == 'Finalizada':
                                                                        break
                                                                else:
                                                                    limpiar_pantalla()
                                                                    continue

                                                            elif estado == 200:
                                                                mostrar_texto(salida)
                                                                mostrar_texto(cambiar_turno(token, id_user_partida))
                                                                subir_partidas()
                                                                param('Presione "Enter" para continuar ...', str,
                                                                      valores_validos=[''], estilo='info')
                                                                limpiar_pantalla()
                                                                break

                                                            else:  # Error al mover la tropa
                                                                mostrar_texto(salida)
                                                                limpiar_pantalla()
                                                                continue

                                                        case 3:
                                                            destino = to_tuple()
                                                            salida, estado = mover_batallon(token, id_user_partida,
                                                                                            destino)
                                                            if isinstance(salida, list):
                                                                mostrar_texto(salida[0])
                                                                dict = {"Opciones": ["prompt",
                                                                                     ["0. Abortar",
                                                                                      "1. Combatir (Se enviarán a todas las tropas de la región)"]]}

                                                                crear_tabla(dict, dim=False)

                                                                console.print()

                                                                choice = param('Eliga una opción: ', int,
                                                                               valores_validos=[0, 1])

                                                                if choice == 1:
                                                                    salida = combatir(token, id_user_partida,
                                                                                      coordenada, destino)
                                                                    mostrar_texto(salida['texto'])
                                                                    limpiar_pantalla()
                                                                    if salida['estado'] == 'Finalizada':
                                                                        break
                                                                else:
                                                                    limpiar_pantalla()
                                                                    continue
                                                            elif estado == 200:
                                                                mostrar_texto(salida)
                                                                mostrar_texto(cambiar_turno(token, id_user_partida))
                                                                subir_partidas()
                                                                param('Presione "Enter" para continuar ...', str,
                                                                      valores_validos=[''], estilo='info')
                                                                limpiar_pantalla()
                                                                break

                                                            else:  # Error al mover la tropa
                                                                mostrar_texto(salida)
                                                                limpiar_pantalla()
                                                                continue

                                                        case 4:
                                                            mostrar_texto(catalogos_dict['edificios']['catalogo'])
                                                            edificio = param('Introduzca el nombre del edificio: ', str,
                                                                             valores_validos=
                                                                             catalogos_dict['edificios'][
                                                                                 'valores_validos'])
                                                            mostrar_texto(
                                                                construir_edificio(token, id_user_partida, edificio))
                                                            limpiar_pantalla()
                                                        case 5:
                                                            edificio = param('Introduzca el nombre del edificio: ', str,
                                                                             valores_validos=
                                                                             catalogos_dict['edificios'][
                                                                                 'valores_validos'])
                                                            mostrar_texto(
                                                                subir_nivel_edificio(token, id_user_partida, edificio))
                                                            limpiar_pantalla()
                                                else:
                                                    console.print(zona[0], style='prompt')
                                                    table_volver = Table(show_edge=False,
                                                                         header_style="bold white reverse blue")
                                                    table_volver.add_column('MENÚ', justify='center', style='prompt')
                                                    table_volver.add_row('0. Volver', style='dim')
                                                    console.print(table_volver)
                                                    console.print()
                                                    choice = param('Eliga una opción: ', int, valores_validos=[0])
                                                    if choice == 0:
                                                        limpiar_pantalla()
                                                        break
                                            elif estado == 404:
                                                mostrar_texto(zona['error'])
                                                break
                                    elif choice == 2:
                                        mostrar_texto(ver_recursos(token, id_user_partida), enumerado=True)
                                        table_volver = Table(show_edge=False, header_style="bold white reverse blue")
                                        table_volver.add_column('MENÚ', justify='center', style='prompt')
                                        table_volver.add_row('0. Volver', style='dim')
                                        console.print(table_volver)
                                        console.print()
                                        choice = param('Eliga una opción: ', int, valores_validos=[0])
                                        if choice == 0:
                                            limpiar_pantalla()
                                            continue
                                    elif choice == 3:
                                        mapa = ver_mapa(token, id_user_partida)
                                        mostrar_texto(mapa)
                                        table_volver = Table(show_edge=False, header_style="bold white reverse blue")
                                        table_volver.add_column('MENÚ', justify='center', style='prompt')
                                        table_volver.add_row('0. Volver', style='dim')
                                        console.print(table_volver)
                                        console.print()
                                        choice = param('Eliga una opción: ', int, valores_validos=[0])
                                        if choice == 0:
                                            limpiar_pantalla()
                                            continue
                                    elif choice == 4:
                                        mostrar_texto(cambiar_turno(token, id_user_partida))
                                        subir_partidas()
                                        param('Presione "Enter" para continuar ...', str, valores_validos=[''],
                                              estilo='info')
                                        limpiar_pantalla()
                                        continue
                                    else:
                                        limpiar_pantalla()
                                        break
                                else:
                                    mostrar_texto('Todavía no es tu turno', estilo='info')
                                    tabla_espera()
                                    choice = param('Eliga una opción: ', int, valores_validos=[0, 1])
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
                                mostrar_texto(obtener_ganador(token, id_user_partida))
                                param('Presione "Enter" para continuar ...', str, valores_validos=[''], estilo='info')
                                limpiar_pantalla()
                                break
                        elif r_estado == 404:
                            mostrar_texto(estado_partida)
                            break
                else:
                    limpiar_pantalla()
                    break

        elif choice == 3:
            mostrar_texto(ver_ranking(token))
            param('Presione "Enter" para continuar ...', str, valores_validos=[''], estilo='info')
            limpiar_pantalla()
            continue

        elif choice == 0:
            limpiar_pantalla()
            break


# choice2- mostrar perfil del jugador
def mostrar_perfil(token):
    limpiar_pantalla()
    while True:
        perfil = {"Menú": ["prompt", ["0. Volver", "1. Buzón", "2. Amigos"]]}
        crear_tabla(perfil, dim=True)

        console.print()

        choice = param('Eliga una opción: ', int, valores_validos=[0, 1, 2])
        if choice == 1:
            limpiar_pantalla()
            while True:
                buzon = obtener_buzon(token)
                if buzon != []:
                    mostrar_texto(buzon)
                    buzon = {"Menú": ["prompt", ["0. Volver", "1. Marcar como leído todos los mensajes"]]}
                    crear_tabla(buzon, dim=True)

                    console.print()

                    choice = param('Eliga una opción: ', int, valores_validos=[0, 1])
                    if choice == 1:
                        mostrar_texto(marcar_leido(token))
                        limpiar_pantalla()
                    else:
                        limpiar_pantalla()
                        break
                else:
                    mostrar_texto('No tienes ningún mensaje', estilo='info')

                    tabla_espera()

                    choice = param('Eliga una opción: ', int, valores_validos=[0, 1])
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
                    mostrar_texto('Todavía no tienes amigos agregados', estilo='info')
                amigos = {"Menú": ["prompt",
                                   ["0. Volver", "1. Solicitudes de amistad", "2. Enviar solicitud de amistad",
                                    "3. Invitaciones de partida"]]}
                crear_tabla(amigos, dim=True)

                console.print()

                choice = param('Eliga una opción: ', int, valores_validos=[0, 1, 2, 3])
                if choice == 1:
                    limpiar_pantalla()
                    while True:
                        # Todo: tabla mostrando bien la información
                        solicitudes = obtener_solicitudes(token)
                        if solicitudes != []:
                            mostrar_texto(solicitudes, enumerado=True)
                            mostrar_texto(f'{len(solicitudes) + 1}. VOLVER')
                            valores_validos = [num for num in range(0, len(solicitudes) + 2)]
                            choice = param('Eliga una opción: ', int,
                                           valores_validos=valores_validos)
                            if choice != valores_validos[-1]:
                                solicitud = solicitudes[choice - 1]  # Porque las listas empiezan en 0
                                console.print('1. ACEPTAR SOLICITUD', style='prompt')
                                console.print('2. RECHAZAR SOLICITUD', style='prompt')
                                choice = param('Eliga una opción: ', int, valores_validos=[1, 2])
                                if choice == 1:
                                    mostrar_texto(aceptar_solicitud(token, solicitud))
                                    limpiar_pantalla()
                                elif choice == 2:
                                    mostrar_texto(rechazar_solicitud(token, solicitud))
                                    limpiar_pantalla()
                            else:
                                limpiar_pantalla()
                                break
                        else:
                            mostrar_texto('No tienes ninguna solicitud de amistad', estilo='info')

                            tabla_espera()

                            choice = param('Eliga una opción: ', int, valores_validos=[0, 1])
                            console.print()
                            if choice == 1:
                                continue
                            else:
                                limpiar_pantalla()
                                break
                elif choice == 2:
                    usuario = param('Introduzca el usuario: ', str)
                    mostrar_texto(enviar_solicitud(token, usuario))
                    limpiar_pantalla()
                elif choice == 3:  # Invitaciones de partida
                    limpiar_pantalla()
                    while True:
                        invitaciones_dict = invitaciones_privadas(token)
                        if invitaciones_dict != {}:
                            invitaciones_str = [partida for partida in invitaciones_dict.values()]
                            mostrar_texto(invitaciones_str, enumerado=True)
                            id_invitacion = param('Introduce el id de la invitación', str)
                            invitacion = {"Menú": ["prompt", ["1. Aceptar invitación", "2. Rechazar invitación"]]}
                            crear_tabla(invitacion, dim=True)

                            console.print()

                            choice = param('Eliga una opción: ', int, valores_validos=[1, 2])
                            if choice == 1:
                                reino = param('Introduce el nombre de tu reino: ', str)
                                mostrar_texto(unirse_partida(token, id_invitacion, reino))
                                mostrar_texto(iniciar_partida(token, id_invitacion))
                                break
                            elif choice == 2:
                                mostrar_texto(cancelar_partida(token, id_invitacion))
                                break
                        else:
                            mostrar_texto('No tienes ninguna invitación', estilo='info')

                            tabla_espera()

                            choice = param('Eliga una opción: ', int, valores_validos=[0, 1])
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


# MENU PRINCIPAL

def menu():
    console.print(Align.center(titulo_md), style='bold bright_yellow', )
    console.print()
    console.print(Align.center(parrafo_texto), style='green italic', )
    console.print()
    console.print(Align.center(despedida_md), style='bold bright_yellow', )

    param('Presione "Enter" para continuar ...', str,
          valores_validos=[''], estilo='info')

    limpiar_pantalla()

    while True:
        principal = {"Menú": ["prompt", ["0. Exit", "1. Registrarse", "2. Iniciar sesión"]]}
        crear_tabla(principal, dim=True)
        console.print()

        choice = param('Eliga una opción: ', int, valores_validos=[0, 1, 2])

        if choice == 1:
            user = param('Usuario: ', str)
            password = param('Contraseña: ', str, is_password=True)

            mostrar_texto(signup(user, password))
            limpiar_pantalla()
        elif choice == 2:
            user = param('Usuario: ', str)
            password = param('Contraseña: ', str, is_password=True)
            log_in = login(user, password)

            if log_in[1]:
                token = log_in[0]
                limpiar_pantalla()
                while True:
                    mostrar_texto(notificaciones(token))
                    lobby = {"Lobby": ["prompt", ["0. Log out", "1. Jugar", "2. Perfil"]]}
                    crear_tabla(lobby, dim=True)
                    console.print()

                    choice = param('Eliga una opción: ', int, valores_validos=[0, 1, 2])
                    console.print()
                    if choice == 1:
                        jugar(token)
                    elif choice == 2:
                        mostrar_perfil(token)
                    elif choice == 0:
                        limpiar_pantalla()
                        break
            else:
                mostrar_texto(log_in[0])
                limpiar_pantalla()
        elif choice == 0:
            console.print('Saliendo...', style='info')
            break


if __name__ == '__main__':
    menu()


