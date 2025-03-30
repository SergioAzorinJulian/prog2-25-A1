import random
class Comerciante():
    '''
    Clase para crear los comeriantes ambulantes
    ATRIBUTOS
    -----------
    nombre: int
    atributo de intancia, es el nombre del comerciante
    inventario: dict
    atributo de intancia, es un diccionario que contiene el inventario del comerciante
    pos: tuple
    representa la posicion actual de comerciante
    rutas: list
    son todas las posibles rutas que puede seguir el comerciante
    '''

    def __init__(self, nombre= int, inventario= dict, pos= tuple, rutas= list):
        '''constructor de la clase'''
        self.nombre = nombre
        self.inventario = inventario
        self.pos = pos
        self.rutas = rutas

    def