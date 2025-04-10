import requests
import combate
import jugador
import mapa
URL = 'http://127.0.0.1:5000'
token = ''





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
    create(str(user), Jugador(mapa))


def menu():
    while True:
        print("\n=== MENU ===")

        print("1. Signup")
        print("2. Signin")
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
            id = input("Enter ID: ")
            read(id)

        elif choice == '4':
            print("Saliendo...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == '__main__':
    menu()