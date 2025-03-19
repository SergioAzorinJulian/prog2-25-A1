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

    def crear_nodos(self)-> List[tuple]:

        mapa_nodos = []

        for fila in range(self.filas):
            for columna in range(self.columnas):
                mapa_nodos.append((fila, columna))

        return mapa_nodos


    def crear_aristas(self, nodos: List[tuple], diagonales: bool = True)-> List[list[tuple]]:

        aristas = [] # Listado de aristas para cada nodo
        cont = 0

        if diagonales:
            for nodo_diagonal in nodos:

                aristas.append([]) # Anydimos una lista vacia para cada nodo

                ### HORIZONTALES Y VERTICALES ###
                if 0 <= nodo_diagonal[0] - 1:                                                           # Fila arriba
                    aristas[cont].append((nodo_diagonal[0] - 1, nodo_diagonal[1]))
                if nodo_diagonal[0] + 1 < self.filas:                                                   # Fila abajo
                    aristas[cont].append((nodo_diagonal[0] + 1, nodo_diagonal[1]))
                if 0 <= nodo_diagonal[1] - 1:                                                           # Columna izquierda
                    aristas[cont].append((nodo_diagonal[0], nodo_diagonal[1] - 1))
                if nodo_diagonal[1] + 1 < self.columnas:                                                # Columna derecha
                    aristas[cont].append((nodo_diagonal[0], nodo_diagonal[1] + 1))

                ### DIAGONALES ###
                if (0 <= nodo_diagonal[0] - 1) and (0 <= nodo_diagonal[1] - 1):                         # Diagonal arriba izquierda
                    aristas[cont].append((nodo_diagonal[0] - 1, nodo_diagonal[1] - 1))
                if (0 <= nodo_diagonal[0] - 1) and (nodo_diagonal[1] + 1 < self.columnas):              # Diagonal arriba derecha
                    aristas[cont].append((nodo_diagonal[0] - 1, nodo_diagonal[1] + 1))
                if (nodo_diagonal[0] + 1 < self.filas) and (0 <= nodo_diagonal[1] - 1):                 # Diagonal abajo izquierda
                    aristas[cont].append((nodo_diagonal[0] + 1, nodo_diagonal[1] - 1))
                if (nodo_diagonal[0] + 1 < self.columnas) and (nodo_diagonal[1] + 1 < self.columnas):   # Diagonal abajo derecha
                    aristas[cont].append((nodo_diagonal[0] + 1, nodo_diagonal[1] + 1))

                cont += 1                                                                               # Incrementamos el contador para pasar al siguiente nodo

        else:
            for nodo in nodos:

                aristas.append([])  # Anydimos una lista vacia para cada nodo

                if 0 <= nodo[0] - 1:                                                                    # Fila arriba
                    aristas[cont].append((nodo[0] - 1, nodo[1]))
                if nodo[0] + 1 < self.filas:                                                            # Fila abajo
                    aristas[cont].append((nodo[0] + 1, nodo[1]))
                if 0 <= nodo[1] - 1:                                                                    # Columna izquierda
                    aristas[cont].append((nodo[0], nodo[1] - 1))
                if nodo[1] + 1 < self.columnas:                                                         # Columna derecha
                    aristas[cont].append((nodo[0], nodo[1] + 1))

                cont += 1                                                                               # Incrementamos el contador para pasar al siguiente nodo


        return aristas # Devolvemos las aristas para cada nodo


    













