#from random import randintf
from typing import List

class Mapa:

    def __init__(self, filas: int, columnas: int):

        self.filas = filas
        self.columnas = columnas

    """def crear_conexiones(self):
        
        mapa_conexiones = []
        
        # Si es 1 -> izquierda/derecha. Si es 0 -> arriba/abajo
        #orientacion_reino = randint(2)

        

        if orientacion_reino: # orientacion_reino != 0 -> 1
            pass
        
        else: # orientacion_reino == 0
            # Generamos aleatoriamente la posicion de la columna los reinos 
            #reino_1 = (0, randint(self.columnas)) # Primera fila
            #reino_2 = (self.filas - 1, randint(self.columnas)) # Ultima fila
            
            for fila in range(self.filas):
                for columna in range(self.columnas):
                    
                    mapa_conexiones.append((fila, columna))
                    #if (fila, columna) == (reino_1 or reino_2):
                    #    pass"""

    def crear_conexiones(self)-> List[tuple]:

        mapa_conexiones = []

        for fila in range(self.filas):
            for columna in range(self.columnas):
                mapa_conexiones.append((fila, columna))

        return mapa_conexiones

