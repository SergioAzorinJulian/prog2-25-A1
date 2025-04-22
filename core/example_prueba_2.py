from typing import Any, Union
import requests
import getpass
import os

URL = 'http://127.0.0.1:5000'
# Variable global para almacenar el token de sesión
token: Union[str, None] = ''
# Variable global para almacenar el ID de la partida actual
partida_actual_id: Union[str, None] = None


# Para limpiar la pantalla
def limpiar_pantalla():
    # Para Windows
    if os.name == 'nt':
        os.system('cls')
    # Para Unix/Linux/macOS
    else:
        os.system('clear')


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


def opciones_partida(jugador: str = 'Jugador', nombre_reino: str = 'Reino'):
    """
    Muestra las opciones que tiene disponible un jugador durante una partida.

    Parámetros
    ----------
    jugador: str
        Indica el nombre del jugador (nombre de usuario)
    nombre_reino: str
        Indica el nombre del reino del jugador
    """
    limpiar_pantalla()
    print(f'=== Turno del jugador {jugador} - ({nombre_reino}) ===')
    print("  --- Información ---")
    print("  1 : Ver detalles de una zona de tu territorio")
    print("  2 : Ver mis recursos actuales")
    print("  3 : Ver mis edificios y sus niveles")
    print("  4 : Ver mis tropas")
    print("-----------------------------------------")
    print("  --- Acciones del Reino ---")
    print("  5 : Construir/Mejorar edificio en una zona")
    print("  6 : Comerciar (No implementado)")
    print("-----------------------------------------")
    print("  --- Acciones Militares ---")
    print("  7 : Reclutar tropas")
    print("  8 : Mover un tipo de tropa")
    print("  9 : Mover batallón (varias tropas)")
    print("-----------------------------------------")
    print("  --- Fin de Turno ---")
    print("  10: Terminar mi turno")
    print("-----------------------------------------")
    print("  --- Opciones de Partida ---")
    print("  11: Guardar Partida (No implementado)")
    print("   0: Salir de la partida (Volver al menú principal)")

    option = param('Elija una opción', int, 1, valores_validos=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    return option


def menu():

    global token
    global partida_actual_id
    jugador_actual: Union[str, None] = None  # Nombre del jugador principal (el que crea/carga la partida)


    while True:
        # limpiar_pantalla()
        print('\n=== KINGDOM CRAFT ===\n')
        if jugador_actual:
            print(f"--- Sesión iniciada como: {jugador_actual} ---")
        if partida_actual_id:
            print(f"--- Actualmente en Partida: {partida_actual_id} ---")

        # Opciones del menú básicas
        print(' 1. Registrar un nuevo usuario')
        print(' 2. Iniciar sesión')
        if token:  # Opciones que requieren iniciar sesión
            print(' 3. Crear Nueva Partida / Desafiar Jugador')
            print(' 4. Ver Mis Desafíos Pendientes')
            print(' 5. Ver/Seleccionar Mis Partidas Activas')
            print(' 6. Entrar/Reanudar Partida Seleccionada')
            print(' 7. Mostrar datos del usuario (No implementado)')  # Se mantiene por consistencia
            print(' 8. Cerrar sesión')
            print(' 9. Eliminar mi cuenta')
        print(' 0. Salir\n')

        # Manejo de elección basado en el estado de inicio de sesión
        if token:
            choice = param('Elija una opción', int, 1, valores_validos=[0, 3, 4, 5, 6, 7, 8, 9])
        else:
            choice = param('Elija una opción', int, 1, valores_validos=[0, 1, 2])

        match choice:

            case 1: # Registrar
                user = param('Introduzca su nombre de usuario', str, 4)
                password = param('Introduzca su contraseña', str, 8, is_password=True)
                # TODO crear usuario en API
                print('Creando usuario ...')

            case 2: # Iniciar sesión
                user = param('Introduzca su nombre de usuario', str, 4)
                password = param('Introduzca su contraseña', str, 8, is_password=True)
                # TODO log in en API
                token = 'fake_token'  # Simulación de token
                print('Iniciando sesión ...') if user and password else \
                print(f'No existe dicho usuario {user} con contraseña {password}. \
Verifique las credenciales o cree una cuenta en la opción 1.')

            case 3: # Crear Partida / Desafiar
                print("Crear Nueva Partida:")
                oponente = param('Nombre de usuario del oponente (dejar vacío para partida abierta)', str, 0)  # Permitir vacío
                print(f'Enviando solicitud para crear partida...')

            case 4: # Ver Desafíos Pendientes
                print("Buscando desafíos pendientes para ti...")

            case 5: # Ver Partidas Activas
                print("Buscando tus partidas activas...")

            case 6:# Entrar/Reanudar Partida Seleccionada
                if not partida_actual_id:
                    print("Primero selecciona una partida activa (Opción 5).")
                    continue  # Vuelve al inicio del bucle while principal

                print(f"Entrando en partida {partida_actual_id}...")
                en_partida = True
                while en_partida:
                    limpiar_pantalla()
                    print(f"--- Partida: {partida_actual_id} ---")
                    print("Consultando estado de la partida...")
                    # TODO: Llamar API: GET /games/{partida_actual_id} (Headers: {'Authorization': f'Bearer {token}'})
                    # Si tiene éxito:
                    #    estado_partida = response.json() # Contiene status, current_turn, player_state etc.
                    #    nombre_oponente = estado_partida['opponent'] # Campo asumido
                    #    # TODO: Obtener el nombre del reino del jugador si está guardado/se necesita
                    #    nombre_reino_jugador_actual = "Mi Reino" # Valor provisional

                    #    if estado_partida['status'] == 'waiting_for_opponent':
                    #        print(f"Esperando a que {nombre_oponente} se una...")
                    #        accion_espera = input("Pulsa Enter para volver a comprobar, o escribe 'menu' para salir al menú principal: ")
                    #        if accion_espera.lower() == 'menu':
                    #            en_partida = False # Sale del bucle while en_partida
                    #        continue # Vuelve a comprobar el estado

                    #    elif estado_partida['status'] == 'opponent_turn':
                    #        print(f"Esperando el turno de {nombre_oponente}...")
                    #        # Usar la opción de polling con salida al menú
                    #        accion_espera = input("Pulsa Enter para comprobar de nuevo, o escribe 'menu' para salir al menú principal: ")
                    #        if accion_espera.lower() == 'menu':
                    #             en_partida = False # Sale del bucle while en_partida
                    #        continue # Si no escribió 'menu', vuelve a comprobar el estado

                    #    elif estado_partida['status'] == 'your_turn':
                    #        print("¡Es tu turno!")
                    #        # TODO: Pasar la info necesaria del estado de la partida si opciones_partida la necesita
                    #        opcion_juego = opciones_partida(jugador_actual, nombre_reino_jugador_actual) # ¿Pasar game_id y token también?

                    #        match opcion_juego:
                    #            case 1: # Ver detalles zona
                    #                 coords_zona = param("Introduce coordenadas (x,y) de la zona a ver", str)
                    #                 # TODO: Validar formato de coordenadas
                    #                 # TODO: Llamar API: GET /games/{partida_actual_id}/map/regions/{coords_zona} (Headers: {'Authorization': f'Bearer {token}'})
                    #                 # Imprimir detalles de la respuesta
                    #                 print(f"Mostrando detalles de la zona {coords_zona}...")
                    #                 input("Pulsa Enter para continuar...")
                    #            case 2: # Ver recursos
                    #                 # TODO: Llamar API: GET /games/{partida_actual_id}/player/resources (Headers: {'Authorization': f'Bearer {token}'})
                    #                 # Imprimir recursos de la respuesta
                    #                 print("Mostrando tus recursos...")
                    #                 input("Pulsa Enter para continuar...")
                    #            case 3: # Ver edificios
                    #                 # TODO: Llamar API: GET /games/{partida_actual_id}/player/buildings (Headers: {'Authorization': f'Bearer {token}'})
                    #                 # Imprimir edificios de la respuesta
                    #                 print("Mostrando tus edificios...")
                    #                 input("Pulsa Enter para continuar...")
                    #            case 4: # Ver tropas
                    #                 # TODO: Llamar API: GET /games/{partida_actual_id}/player/troops (Headers: {'Authorization': f'Bearer {token}'})
                    #                 # Imprimir tropas de la respuesta
                    #                 print("Mostrando tus tropas...")
                    #                 input("Pulsa Enter para continuar...")
                    #            case 5: # Construir/Mejorar
                    #                 # TODO: Preguntar tipo, región, etc.
                    #                 # TODO: Llamar API: POST /games/{partida_actual_id}/player/buildings o PUT /games/{partida_actual_id}/player/buildings/{building_id}
                    #                 print("Construyendo/Mejorando edificio...")
                    #                 input("Pulsa Enter para continuar...")
                    #            case 7: # Reclutar
                    #                 # TODO: Preguntar tipo, cantidad, región
                    #                 # TODO: Llamar API: POST /games/{partida_actual_id}/player/troops
                    #                 print("Reclutando tropas...")
                    #                 input("Pulsa Enter para continuar...")
                    #            case 8: # Mover Tropa (Simplificado para usar lógica de mover batallón)
                    #            case 9: # Mover Batallón
                    #                 # TODO: Preguntar unidades (tipo/cantidad), origen, destino
                    #                 # TODO: Llamar API: POST /games/{partida_actual_id}/player/actions {'action': 'move_troops', 'units': [...], 'origin': '...', 'destination': '...'}
                    #                 print("Moviendo batallón...")
                    #                 input("Pulsa Enter para continuar...")
                    #            case 10: # Terminar Turno
                    #                 print("Terminando tu turno...")
                    #                 # TODO: Llamar API: POST /games/{partida_actual_id}/end_turn (Headers: {'Authorization': f'Bearer {token}'})
                    #                 # El bucle comprobará automáticamente el estado de nuevo
                    #            case 0: # Salir Partida
                    #                 print("Saliendo de la partida...")
                    #                 # partida_actual_id = None # Opcional: Limpiar ID de partida seleccionada
                    #                 en_partida = False # Sale del bucle while en_partida
                    #            case _:
                    #                 print("Opción de juego inválida.")
                    #                 input("Pulsa Enter para continuar...")

                    #    elif estado_partida['status'] == 'finished':
                    #         # TODO: Obtener info de ganador/perdedor del estado_partida
                    #         print(f"La partida {partida_actual_id} ha terminado.")
                    #         print(f"Ganador: {estado_partida['winner']}") # Campo asumido
                    #         partida_actual_id = None # Limpiar ID
                    #         en_partida = False # Salir del bucle
                    #         input("Pulsa Enter para volver al menú principal...")

                    #    else: # Estado desconocido
                    #         print(f"Estado desconocido de la partida: {estado_partida['status']}")
                    #         en_partida = False # Salir del bucle
                    #         input("Pulsa Enter para volver al menú principal...")

                    # Si no (llamada a la API falló):
                    #    print(f"Error al obtener estado de la partida: {response.status_code} {response.json()['msg']}")
                    #    en_partida = False # Salir del bucle interno en caso de error
                    #    input("Pulsa Enter para volver al menú principal...")

            case 7: # Mostrar datos del usuario
                print("Mostrando datos del usuario (a implementar)...")

            case 8:  # Cerrar sesión
                if token:
                    print("Cerrando sesión...")
                    token = None
                    jugador_actual = None
                    partida_actual_id = None  # También limpiar partida seleccionada al cerrar sesión
                    print("Sesión cerrada localmente.")
                else:
                    print("No has iniciado sesión.")

            case 9:  # Eliminar Usuario
                confirmar = param(
                    f"¿Estás seguro de que quieres eliminar tu cuenta '{jugador_actual}'? Esta acción es irreversible. (sí/no)",
                    str,  valores_validos=['sí', 'si', 'Sí', 'Si', 'no', 'No'])  # Incluir variaciones

                # Convertimos la respuesta a minúsculas DESPUÉS de obtenerla para la comparación lógica
                if confirmar.lower() in ['sí', 'si']:
                    print("Eliminando tu cuenta...")
                else:
                    print("Eliminación cancelada.")

            case 0: # Salir del programa
                print('Gracias por jugar a Kingdom Craft. ¡Hasta pronto!')
                exit()

            case _: # Opción inválida
                print('Opción inválida')


"""
ESTRUCTURA PARA GUARDAR LAS PARTIDAS (EN LA API)
games = {
    "game_123": { # Clave: game_id
        "player1_id": "jugador1",
        "player2_id": "jugador2",
        "status": "player1_turn",
        "current_turn": "jugador1", # o jugador 2
        "map_data": mapa_obj, # El objeto Mapa compartido
        "player_states": { # Estado específico de cada jugador dentro de esta partida
            "jugador1": jugador1_obj, # el objeto Jugador
            "jugador2": jugador2_obj
        }
    },
    # ... otras partidas ...
}
"""

if __name__ == '__main__':
    menu()
