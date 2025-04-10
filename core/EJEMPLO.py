URL_BASE='http://127.0.0.1:5000'
TOKEN =None
import requests




def login():
    global TOKEN
    user = input("Usuario: ")
    passwd = input("Contraseña: ")
    r = requests.get(f"{URL_BASE}/login", params={"user": user, "passwd": passwd})
    print("Respuesta:", r.status_code, r.json())
    if r.status_code == 200:
        TOKEN = r.json()["access_token"]


def signup():
    user = input("Usuario nuevo: ")
    passwd = input("Contraseña: ")
    r = requests.post(f"{URL_BASE}/signup", json={"user": user, "passwd": passwd})
    print("Respuesta:", r.status_code, r.json())