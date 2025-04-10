import requests
from combate import Batalla
from jugador import Jugador
from mapa import Mapa

URL = 'http://127.0.0.1:5000'
token = ''

def crear_mapa():
    """Crea el mapa por defecto y lo devuelve."""

    # Inicializar el mapa con 6 filas y 6 columnas
    map = Mapa(5, 5)

    # Crear nodos y conexiones
    nodos = map.crear_nodos()
    conexiones = map.crear_aristas(nodos)

    # Asignar terrenos a los nodos
    map.anyadir_terreno(conexiones)

    # Asignar zonas y generar recursos
    map.asigna_zonas()

    return map

def to_tuple():
    """
    Obtiene coordenadas del usuario a través de input y las convierte en una tupla.
    Maneja errores de formato y rango, y se mantiene en un bucle hasta que se ingrese un valor válido.

    Returns:
        tuple[int, int]: Una tupla con las coordenadas ingresadas por el usuario.
    """
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

        except ValueError:
            print("Error: Las coordenadas deben ser números enteros.")
            continue  # Volver al inicio del bucle


def create(id, value):
    global token
    r = requests.post(f'{URL}/data/{id}?value={value}', headers={'Authorization': 'Bearer ' + token})
    print(r.status_code)
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

    print(r.status_code)
    print(r.text)


def signin(user, password):
    global token
    r = requests.get(f'{URL}/signin?user={user}&password={password}')

    print(r.status_code)
    print(r.text)
    token = r.text
    create(str(user), Jugador(str(user), crear_mapa()))

def ver_zona(usuario,tupla):
    r = requests.get(f'{URL}/data/ver_zona/<{usuario}?value={tupla}>')
    print(r)
def menu():
    while True:
        print("\n=== MENU ===")

        print("1. REGISTRATE")
        print("2. INICIAR SESIÓN")
        print("3. Read Data")
        print("4. Exit")

        choice = input('Elige una opción (1-4): ')


        if choice == '1':
            user = input("Usuario Nuevo: ")
            password = input("Contraseña: ")
            singup(user, password)
        elif choice == '2':
            user = input("Usuario: ")
            password = input("Contraseña: ")
            signin(user, password)
            while True:
                print('1. VER REGIÓN')
                print('2. VOLVER')
                choice = input('Elige una opción (1-2):')
                if choice == '1':
                    tupla = to_tuple()
                    ver_zona(user,tupla)
                elif choice == '2':
                    break
                else:
                    print('Opción invalida')
        elif choice == '3':
            id = user
            read(id)

        elif choice == '4':
            print("Saliendo...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == '__main__':
    menu()
