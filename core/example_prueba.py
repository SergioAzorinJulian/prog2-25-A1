from typing import Any, Union
import requests
import getpass
import os

URL = 'http://127.0.0.1:5000'
token: Union[str, None] = ''


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

    jugador_actual: Union[str, None] = None  # Nombre del jugador principal (el que crea/carga la partida)
    contrincante: Union[str, None] = None # Nombre del otro jugador
    nombre_reino_jugador_actual: Union[str, None] = None  # Nombre del reino del jugador principal
    nombre_reino_contrincante: Union[str, None] = None  # Nombre del reino del contrincante


    while True:
        limpiar_pantalla()
        print('\n=== KINGDOM CRAFT ===\n')

        print('1. Registrar un nuevo usuario')
        print('2. Iniciar sesión (requiere que exista el usuario)')
        print('3. Jugar (requiere iniciar sesión)')
        print('4. Mostrar datos del usuario (requiere iniciar sesión)')
        print('5. Cerrar sesión (requiere haber iniciado sesión)')
        print('6. Eliminar un usuario (requiere haber iniciado sesión)')
        print('0. Salir\n')

        choice = param('Elija una opción', int, 1, valores_validos=[0, 1, 2, 3, 4, 5, 6])

        match choice:

            case 1:
                user = param('Introduzca su nombre de usuario', str, 4)
                password = param('Introduzca su contraseña', str, 8, is_password=True)
                # TODO crear usuario en API
                print('Creando usuario ...')

            case 2:
                user = param('Introduzca su nombre de usuario', str, 4)
                password = param('Introduzca su contraseña', str, 8, is_password=True)
                # TODO log in en API

                print('Iniciando sesión ...') if user and password else \
                print(f'No existe dicho usuario {user} con contraseña {password}. \
Verifique las credenciales o cree una cuenta en la opción 1.')

            case 3:
                if not token:
                    print('No ha iniciado sesión, acceda a la opción 2. primero.')
                    continue

                limpiar_pantalla()
                while True:
                    print('\n1. Crear una partida nueva')
                    print('2. Cargar una partida ya existente')
                    print('0. Volver\n')
                    choice = param('Elija una opción', int, 1, valores_validos=[0, 1, 2])

                    if choice == 1:

                        limpiar_pantalla()
                        while True:
                            print('\n1. Crear un mapa genérico')
                            print('2. Crear un mapa con personalizado')
                            print('3. Seleccionar contrincante (requiere tener un mapa ya creado)')
                            print('0. Volver\n')
                            choice = param('Elija una opción', int, 1, valores_validos=[0, 1, 2, 3])

                            if choice == 1:
                                # TODO crear mapa genérico en la API
                                print('Creando mapa genérico ...')
                            elif choice == 2:
                                # TODO crear mapa personalizado en la API, dimensiones, terreno, etc.
                                print('Creando mapa personalizado ...')

                            elif choice == 3:

                                limpiar_pantalla()
                                while True:
                                    print('\n1. Contrincante aleatorio')
                                    print('2. Contrincante específico (lo indicas tú)')
                                    print('3. Iniciar partida (requiere haber seleccionado un contrincante)')
                                    print('0. Volver\n')
                                    choice = param('Elija una opción', int, 1, valores_validos=[0, 1, 2, 3])

                                    if choice == 1:
                                        # TODO seleccionar un contrincante aleatorio del listado de usuarios de la API (que no sea él mismo)
                                        print('Seleccionando contrincante aleatorio ...')
                                        contrincante = "ContrincanteAleatorio"  # Asignar nombre aleatorio
                                        print(f"Contrincante {contrincante} seleccionado")

                                    elif choice == 2:
                                        # TODO mostrar el listado de usuarios de la API (que no sea él mismo)
                                        contrincante = param('Elija un contrincante del listado', str, 4) #valores_validos=listado_usuarios)
                                        print(f'Contrincante {contrincante} seleccionado')

                                    elif choice == 3:
                                        if contrincante is None:
                                            print("Debe seleccionar un contrincante primero.")
                                            continue
                                        # TODO iniciar partida con el contrincante seleccionado
                                        print('Iniciando partida ...')

                                        limpiar_pantalla()
                                        # TODO darle la opcion al jugador de ponerle un nombre a su reino

                                        # Pedir el nombre del reino a ambos jugadores
                                        nombre_reino_jugador_actual = param('Introduzca el nombre de su reino', str,4)

                                        print("Ahora es el turno del otro jugador (el contrincante)")
                                        nombre_reino_contrincante = param('Introduzca el nombre de su reino', str,4)

                                        es_turno_jugador_actual = True

                                        while True:
                                            # TODO obtener el nombre del jugador de la API
                                            # Llamamos a la función para mostrar las opciones de partida
                                            if es_turno_jugador_actual:
                                                # Lógica del turno del jugador principal
                                                choice = opciones_partida(jugador_actual, nombre_reino_jugador_actual)
                                            else:
                                                choice = opciones_partida(contrincante, nombre_reino_contrincante)

                                            match choice:
                                                case 1:
                                                    # TODO ver detalles de una zona del mapa
                                                    print('Detalles de la zona ...')
                                                case 2:
                                                    # TODO ver recursos actuales
                                                    print('Recursos actuales ...')
                                                case 3:
                                                    # TODO ver edificios y sus niveles
                                                    print('Edificios y niveles ...')
                                                case 4:
                                                    # TODO ver las tropas
                                                    print('Tropas ...')
                                                case 5:
                                                    # TODO construir o mejorar un edificio en una zona
                                                    print('Construir/Mejorar edificio ...')
                                                case 6:
                                                    # TODO comerciar
                                                    print('Comerciar ...')
                                                case 7:
                                                    # TODO preguntale al usuario qué tropa quiere reclutar y cuanta cantidad
                                                    # TODO la tropa se crea en el reino, con el correspondiente edificio que las cree
                                                    print('Reclutando tropas ...')
                                                case 8:
                                                    # TODO preguntar al usuario qué tropa quiere mover y a qué zona
                                                    # TODO verificar si la tupla a la que quiere mover las tropas está o no en su territorio
                                                    # TODO si lo está se puede mover, si no lo está solo podrá moverse a la region que esté al lado
                                                    # TODO si se está moviendo a una zona enemiga advertir que entrará en combate ...
                                                    print('Moviendo tropa ...')
                                                case 9:
                                                    # TODO preguntar al usuario qué tropas quiere mover y a qué zona. Las pasamos como una lista
                                                    # TODO verificar si la tupla a la que quiere mover las tropas está o no en su territorio
                                                    # TODO si lo está se puede mover, si no lo está solo podrá moverse a la region que esté al lado
                                                    # TODO si se está moviendo a una zona enemiga advertir que entrará en combate ...
                                                    print('Moviendo batallón ...')
                                                case 10:
                                                    # TODO terminar el turno del jugador y cambiar al otro jugador
                                                    print('Terminando turno ...')
                                                case 11:
                                                    # TODO guardar partida en algún archivo (binario, json, ...) dentro de un directorio para guardar archivos (ej: data)
                                                    print('Guardando partida ...')
                                                case 0:
                                                    # TODO salir de la partida y volver al menú principal
                                                    print('Saliendo de la partida ...')
                                                    es_turno_jugador_actual = True
                                                    contrincante = None
                                                    nombre_reino_jugador_actual = None
                                                    nombre_reino_contrincante = None
                                                    break

                                                case _:
                                                    print('Opción inválida')

                                    elif choice == 0:
                                        break
                                    else:
                                        print('Opción inválida')

                            elif choice == 0:
                                break
                            else:
                                print('Opción inválida')

                    elif choice == 2:
                        # TODO cargar partida desde un archivo (binario, json, ...)
                        print('Cargando partida ...')
                    elif choice == 0:
                        break
                    else:
                        print('Opción inválida')

            case 4:
                # TODO mostrar los datos del usuario de un archivo (sus partidas)
                print('Datos del usuario ...')

            case 5:
                # TODO cerrar sesión en la API
                print('Cerrando sesión')

            case 6:
                # TODO eliminar un usuario (es el usuario que está logeado ya)
                print('Usuario eliminado ...')

            case 0:
                print('Gracias por jugar a Kingdom Craft. ¡Hasta pronto!')

            case _:
                print('Opción inválida')


if __name__ == '__main__':
    menu()
