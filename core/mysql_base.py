import mysql.connector
from mysql.connector import Error

#MYSQL
'''
TABLA RANKING:
CREATE TABLE ranking (
    id VARCHAR(13) PRIMARY KEY,
    rango INT DEFAULT 0
);

'''
config = {
    'host': 'Sergioazorinjulian.mysql.pythonanywhere-services.com',
    'user': 'Sergioazorinjulian',
    'password': 'databaseprog2',
    'database': 'Sergioazorinjuli$default'
}
def connect_to_db() -> None:
    '''
    Función que conecta con la base de datos MYSQL
    '''
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f'Error al conectar con la base de datos: {e}')
def add_user_ranking(id):
    conexion = connect_to_db()
    try:
        if conexion:
            cursor = conexion.cursor()
            query = ("INSERT INTO ranking (id) VALUES (%s)")
            cursor.execute(query, (id,))
            conexion.commit()
            return f'Usuario {id} añadido al ranking'
    except Error as e:
        return (f'Error: {e}')
    finally: #EJ: Usuario ya registrado daría error, por eso un finally
        if conexion: 
            cursor.close()
            conexion.close()
def ver_ranking():
    conexion = connect_to_db()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM ranking ORDER BY rango DESC")
        ranking = [f'{row[0]}: {row[1]}' for row in cursor.fetchall()] #fetchall varios Ej: [(Mario,0),(Pepe,25)...]
        cursor.close()
        conexion.close()
        return ranking
def add_elo(id, puntos):
    conexion = connect_to_db()
    if conexion:
        cursor = conexion.cursor()
        query = "UPDATE ranking SET rango = GREATEST(rango + %s, 0) WHERE id = %s" #Greatest por si es un numero negativo
        cursor.execute(query, (puntos, id))
        conexion.commit()
        query = "SELECT rango FROM ranking WHERE id = %s"
        cursor.execute(query, (id,))
        select = cursor.fetchone() #fetchone uno
        rango = select[0]
        conexion.close()
        return f'Rango actualizado: usuario: {id}, cantidad: {puntos}, rango: {rango}'