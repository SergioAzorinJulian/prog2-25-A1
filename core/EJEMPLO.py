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


def menu():
    while True:
        print("\n=== MENU ===")

        print("1. REGISTRATE")
        print("2. INICIAR SESIÓN")
        print("3. Read Data")
        print("4. Exit")

        choice = input("Enter your choice (1-8): ")


        if choice == '1':
            user = input("Usuario Nuevo: ")
            password = input("Contraseña: ")
            singup(user, password)
        elif choice == '2':
            user = input("Usuario: ")
            password = input("Contraseña: ")
            signin(user, password)
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