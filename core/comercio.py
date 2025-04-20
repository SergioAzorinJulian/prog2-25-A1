from tipos_recursos import Recurso
import random
recursos_jugador = Recurso.creados

class Comerciante:
    """
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
    """

    def __init__(self, nombre= int, inventario= dict, pos= tuple, rutas= list):
        '''constructor de la clase'''
        self.nombre = nombre
        self.inventario = {'madera': 0, 'metal': 0, 'alimento':0, 'agua':0}
        self.pos = pos
        self.rutas = rutas
        self.destino = self.elegir_destino()
        self.distancia = random.randint(1,4) # los numeros son los turnos tarda en llegar, para mas aletoriedad

    def generar_inventario(self):
        for cantidad in self.inventario:



    def precios(self):
        '''meotodo para generar los precios del comerciante'''
        precios = {}


    def elegir_destino(self):
        '''metodo para determinar hacia que parte del mapa se mueve el comerciante ambulante'''
        posibles_destinos = []
        for region in self.rutas:
            if region != self.pos:
                posibles_destinos.append(region)
        return random.choice(posibles_destinos)

    def avanzar(self):
        '''metodo para determinar como avanza el comerciante'''
        if self.distancia > 0: # si la distancia en mayor a 0 significa que aun no ha llegado
            self.distancia -= 1 # sigue avanzando
        elif self.distancia == 0:
            self.pos = self.destino #cuando la distancia es 0 significa que ha llegado a su destino, por lo tanto es su posicion actual
            self.destino = self.elegir_destino() # una vez llegado, vuelve a elegir el destino
            self.distancia = random.randint(1,4) # distancia hasta el proximo destino


    def comerciar(self):
        '''metodo para hacer el intercambio con el jugador'''

