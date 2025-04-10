from region_manager import RegionManager
from region import Region
from random import randint, choice
from typing import List, Dict
from copy import deepcopy


class Mapa:

    """
    Clase que representa un mapa con nodos, conexiones entre ellos y sus tipos de terreno.

    Parameters
    ----------
    filas : int
        Número de filas del mapa.
    columnas : int
        Número de columnas del mapa.

    Attributes
    ----------
    _filas : int
        Número de filas del mapa.
    _columnas : int
        Número de columnas del mapa.
    _conexiones : dict
        Diccionario con los nodos como clave y una lista con los vecinos del nodo como valor.
    _terrenos : dict
        Diccionario con los nodos como clave y el tipo de terreno como valor.

    Methods
    -------
    get_filas() -> int
        Devuelve el número de filas del mapa.
    get_columnas() -> int
        Devuelve el número de columnas del mapa.
    get_conexiones() -> dict
        Devuelve una copia del diccionario de conexiones del mapa.
    get_terrenos() -> dict
        Devuelve una copia del diccionario de terrenos del mapa.
    set_filas(filas: int)
        Establece un nuevo valor para el número de filas del mapa.
    set_columnas(columnas: int)
        Establece un nuevo valor para el número de columnas del mapa.
    crear_nodos() -> List[tuple[int, int]]
        Crea y devuelve una lista de nodos del mapa representados como tuplas de coordenadas (fila, columna).
    crear_aristas(nodos: List[tuple[int, int]], diagonales: bool = True) -> Dict[tuple[int, int], list[int]]
        Crea y devuelve un diccionario con las conexiones entre los nodos del mapa.
    anyadir_terreno(nodos_conectados: Dict[tuple[int, int], list[int]], terrenos: list[str] = None) -> dict[tuple[int, int], dict[str, list[int] | str]]
        Asigna un tipo de terreno a cada nodo del mapa y devuelve un diccionario con los nodos, sus vecinos y sus tipos de terreno.

    Raises
    ------
    ValueError
        Si se proporciona un tipo de terreno que no existe en el juego.
    """

    def __init__(self, filas: int, columnas: int):

        """
        Inicializa una instancia de la clase Mapa.

        Parameters
        ----------
        filas : int
            Número de filas del mapa.
        columnas : int
            Número de columnas del mapa.

        Attributes
        ----------
        self._filas : int
            Número de filas del mapa.
        self._columnas : int
            Número de columnas del mapa.
        self._conexiones : dict
            Diccionario con los nodos como clave y una lista con los vecinos del nodo como valor.
        self._terrenos : dict
            Diccionario con los nodos como clave y el tipo de terreno como valor.
        self.regiones : dict
            Diccionario con las regiones del mapa.
        self.region_manager : RegionManager
            Instancia de la clase RegionManager encargada de gestionar las regiones y sus recursos.
        """

        self._filas = 0 # Inicializamos el numero de filas a 0
        self._columnas = 0 # Inicializamos el numero de columnas a 0
        self.set_filas(filas) # Verificamos que el valor que nos pasa el usuario es valido y lo establecemos
        self.set_columnas(columnas) # Verificamos que el valor que nos pasa el usuario es valido y lo establecemos
        self._conexiones: dict[tuple, list[tuple]] = {} # Diccionario con los nodos como clave y una lista con los vecinos del nodo como valor
        self._terrenos: dict[tuple, str] = {} # Diccionario con los nodos como clave y el tipo de terreno como valor
        self.regiones: dict[tuple, Region] = {} # Diccionario con los nodos como clave y el objeto Region como valor

        # Crear instancia de RegionManager con referencia a este mapa
        self.region_manager = RegionManager(self)


    ### FUNCIONES PARA OBTENER LOS ATRIBUTOS PROTEGIDOS ###
    def get_filas(self) -> int:
        """
        Devuelve el número de filas del mapa.

        Returns
        -------
        int
            Número de filas del mapa.
        """

        return self._filas

    def get_columnas(self) -> int:
        """
        Devuelve el número de columnas del mapa.

        Returns
        -------
        int
            Número de columnas del mapa.
        """

        return self._columnas

    def get_conexiones(self) -> dict:
        """
        Devuelve una copia del diccionario de conexiones del mapa.

        Returns
        -------
        dict
            Copia del diccionario de conexiones del mapa.
        """

        return deepcopy(self._conexiones) # Importante lo de deepcopy para que no se modifique el diccionario original

    def get_terrenos(self) -> dict:
        """
        Devuelve una copia del diccionario de terrenos del mapa.

        Returns
        -------
        dict
            Copia del diccionario de terrenos del mapa.
        """

        return deepcopy(self._terrenos) # Importante lo de deepcopy para que no se modifique el diccionario original

    def get_regiones(self) -> dict:
        """
        Devuelve una copia del diccionario de regiones del mapa.

        Returns
        -------
        dict
            Una copia del diccionario de regiones del mapa.
        """

        return deepcopy(self.regiones)

    ### FUNCIONES PARA ESTABLECER NUEVOS VALORES A LOS ATRIBUTOS PROTEGIDOS ###
    def set_filas(self, filas: int):
        """
        Establece un nuevo valor para el número de filas del mapa.

        Parameters
        ----------
        filas : int
            Nuevo número de filas del mapa.

        Raises
        ------
        ValueError
            Si el número de filas es menor o igual a 0.
        """

        try:
            if filas <= 0:
                raise ValueError("El número de filas debe ser mayor que 0.")
            self._filas = filas
        except ValueError as e:
            print(e)

    def set_columnas(self, columnas: int):
        """
        Establece un nuevo valor para el número de columnas del mapa.

        Parameters
        ----------
        columnas : int
            Nuevo número de columnas del mapa.

        Raises
        ------
        ValueError
            Si el número de columnas es menor o igual a 0.
        """

        try:
            if columnas <= 0:
                raise ValueError("El número de columnas debe ser mayor que 0.")
            self._columnas = columnas
        except ValueError as e:
            print(e)


    def crear_nodos(self)-> List[tuple[int, int]]:

        """
        Crea los nodos del mapa.

        Returns
        -------
        list[tuple[int, int]]
            Listado de nodos del mapa representados como tuplas de coordenadas (fila, columna).

        Attributes
        ----------
        self._filas : int
            Número de filas del mapa.
        self._columnas : int
            Número de columnas del mapa.
        """

        mapa_nodos: list = [] # Creamos un listado vacio para albergar a los nodos

        for fila in range(self.get_filas()):
            for columna in range(self.get_columnas()):
                mapa_nodos.append((fila, columna))

        return mapa_nodos


    def crear_aristas(self, nodos_mapa: List[tuple[int, int]], diagonales: bool = True) -> Dict[tuple[int, int], list[tuple[int, int]]]:

        """
        Crea las aristas (conexiones) entre los nodos del mapa.

        Parameters
        ----------
        nodos_mapa : list[tuple[int, int]]
            Listado de nodos del mapa representados como tuplas de coordenadas (fila, columna).
        diagonales : bool, optional
            Indica si se deben considerar conexiones diagonales entre los nodos (por defecto es True).

        Returns
        -------
        dict[tuple[int, int], list[int]]
            Diccionario con los nodos como clave y una lista de sus vecinos (nodos conectados) como valor.

        Attributes
        ----------
        self._conexiones : dict
            Diccionario con los nodos como clave y una lista de sus vecinos como valor.
        """

        nodos_aristas: dict = {} # Diccionario con los nodos como clave y una lista con los vecinos del nodo como valor

        for nodo_diagonal in nodos_mapa: # Iteramos sobre los nodos para calcular sus vecinos

            aristas: list = []  # Listado de aristas para cada nodo

            ### HORIZONTALES Y VERTICALES ###
            if 0 <= nodo_diagonal[0] - 1:  # Fila arriba
                aristas.append((nodo_diagonal[0] - 1, nodo_diagonal[1]))
            if nodo_diagonal[0] + 1 < self.get_filas():  # Fila abajo
                aristas.append((nodo_diagonal[0] + 1, nodo_diagonal[1]))
            if 0 <= nodo_diagonal[1] - 1:  # Columna izquierda
                aristas.append((nodo_diagonal[0], nodo_diagonal[1] - 1))
            if nodo_diagonal[1] + 1 < self.get_columnas():  # Columna derecha
                aristas.append((nodo_diagonal[0], nodo_diagonal[1] + 1))

            if diagonales: # Si el usuario no ha puesto diagonales a falso, se calcularan las conexiones en diagonal
                ### DIAGONALES ###
                if (0 <= nodo_diagonal[0] - 1) and (0 <= nodo_diagonal[1] - 1):  # Diagonal arriba izquierda
                    aristas.append((nodo_diagonal[0] - 1, nodo_diagonal[1] - 1))
                if (0 <= nodo_diagonal[0] - 1) and (nodo_diagonal[1] + 1 < self.get_columnas()):  # Diagonal arriba derecha
                    aristas.append((nodo_diagonal[0] - 1, nodo_diagonal[1] + 1))
                if (nodo_diagonal[0] + 1 < self.get_filas()) and (0 <= nodo_diagonal[1] - 1):  # Diagonal abajo izquierda
                    aristas.append((nodo_diagonal[0] + 1, nodo_diagonal[1] - 1))
                if (nodo_diagonal[0] + 1 < self.get_filas()) and (nodo_diagonal[1] + 1 < self.get_columnas()):  # Diagonal abajo derecha
                    aristas.append((nodo_diagonal[0] + 1, nodo_diagonal[1] + 1))

            nodos_aristas[nodo_diagonal] = aristas # Anyadimos los vecinos correspondientes al nodo al diccionario
            self._conexiones[nodo_diagonal] = aristas # Anyadimos los vecinos correspondientes al nodo al atributo de instancia


        return nodos_aristas  # Devolvemos el diccionario con los vecinos de cada nodo


    def anyadir_terreno(self, nodos_conectados: Dict[tuple[int, int], list[tuple[int, int]]], terrenos:list[str] = None) -> dict[tuple[int, int], dict[str, list[int] | str]]:

        """
        Asigna un tipo de terreno a cada nodo del mapa. Se hace una distribucion en bloques del terreno
        para darle realismo al mapa. Es decir, que varios nodos colindantes comparten el mismo tipo de terreno.

        Parameters
        ----------
        nodos_conectados : dict[tuple[int, int], list[int]]
            Diccionario con los nodos como clave y una lista de sus vecinos como valor.
        terrenos : list[str], optional
            Listado de tipos de terreno específicos a asignar. Si no se proporciona, se usarán terrenos genéricos.

        Returns
        -------
        dict[tuple[int, int], dict[str, list[int] | str]]
            Diccionario con los nodos como clave y un diccionario como valor que contiene:
            - 'vecinos': list[int]
                Lista de vecinos del nodo.
            - 'terreno': str
                Tipo de terreno asignado al nodo.

        Raises
        ------
        ValueError
            Si se proporciona un tipo de terreno que no existe en el juego.

        Attributes
        ----------
        self._terrenos : dict
            Diccionario con los nodos como clave y el tipo de terreno como valor.
        """


        # Listado con todos los terrenos disponibles dentro del juego
        terrenos_disponibles = ['terreno1', 'terreno2', 'terreno3', 'terreno4', 'terreno5', 'terreno6', 'terreno7', 'terreno8','terrenoN']

        if terrenos: # Si el usuario me ha pasado un listado de terrenos especificos
            try:
                for terreno in terrenos:  # Iteramos sobre el listado para verificar si todos los terrenos existen en el juego o no
                    if terreno not in terrenos_disponibles:  # Si se detecta algun terreno que no existe, se lanza una excepcion
                        raise ValueError(f'El terreno {terreno} no existe en el juego')
            except ValueError as e: # Capturamos la excepcion
                print(e)
                return {} # Devolvemos un diccionario vacio para mantener la consistencia de los datos

        nodos_disponibles: List[tuple[int, int]] = deepcopy(list(nodos_conectados.keys())) # Copia del listado de nodos (claves del diccionario)
        # Lo convertimos a lista para poder iterar, eliminar elementos, ...
        # Listado de nodos que todavia no tienen un tipo de terreno establecido

        resultado: dict = {} # Diccionario compuesto por los nodos (clave), sus vecinos (valor) y sus tipos de terreno (valor)

        for nodo, vecinos in nodos_conectados.items(): # Inicializamos el diccionario con todos los terrenos como vacios
            resultado[nodo] = {
                'vecinos' : vecinos,
                'terreno' : ''
            }

        if not terrenos: # Si no se pasan unos terrenos especificos se usaran unos genericos
            terrenos = ['terreno1', 'terreno2', 'terreno3' ,'terrenoN']

        while nodos_disponibles: # Mientras queden nodos sin terreno establecido
            nodo_actual: tuple[int, int] = choice(nodos_disponibles) # Nodo en el que se esta trabajando actualmente

            nodos_disponibles.remove(nodo_actual) # Eliminamos el nodo actual del listado de disponibles

            extension_terreno: int = randint(4, 6) # Cantidad de nodos que van a compartir un terreno (colindantes)
            tipo_terreno: str = choice(terrenos) # Tipo de terreno que se va a asignar a los nodos (aleatoriamente)

            nodos_a_procesar: list[tuple[int, int]] = [nodo_actual] # Nodos a los que se les va a asignar el tipo de terreno 'tipo_terreno'
            nodos_procesados: int = 0 # Cantidad de nodos a los que ya se les ha asignado dicho tipo de terreno

            while nodos_a_procesar and (nodos_procesados < extension_terreno): # Mientras queden nodos por procesar y la cantidad de
                                                                               # nodos procesados sea menor a la de 'extension_terreno'

                nodo: tuple[int, int] = nodos_a_procesar.pop(0) # Eliminamos el nodo de la lista de nodos a procesar para trabajar con el

                if resultado[nodo]['terreno'] != '': # Si el nodo ya tiene un tipo de terreno, pasamos al siguiente nodo
                    continue # Volvemos al principio del bucle

                # Sino, establecemos el tipo de terreno al nodo
                resultado[nodo]['terreno'] = tipo_terreno
                self._terrenos[nodo] = tipo_terreno # Anyadimos el tipo de terreno al atributo de instancia
                nodos_procesados += 1 # Incrementamos en una unidad la cantidad de nodos procesados

                if nodo in nodos_disponibles: # Si el nodo esta en la lista de nodos disponibles, lo eliminamos. Porque ya le hemos asignado un terreno
                    nodos_disponibles.remove(nodo)


                for vecino in resultado[nodo]['vecinos']: # Nos movemos a los vecinos del nodo actual
                    if vecino in nodos_disponibles and vecino not in nodos_a_procesar: # Si el vecino del nodo actual esta en la lista de nodos disponibles (sin terreno)
                                                                                       # y no lo teniamos en el listado de nodos a procesar lo anyadimos
                        nodos_a_procesar.append(vecino)

        return resultado

    def asigna_zonas(self):

        """
        Asigna zonas y genera recursos para cada región del mapa.

        Los reinos se dispondrán en los bordes del mapa, ya sea en los laterales o en la parte superior e inferior.
        El resto de regiones se asignarán aleatoriamente.

        See Also
        --------
        RegionManager : Clase encargada de gestionar las regiones y sus recursos.
        Region : Clase que representa una región del mapa.

        Notes
        -----
        La asignación de zonas incluye la creación de regiones, la definición de si son reinos o no,
        y la generación de recursos para cada región.
        """

        # Si es 1 los reinos se dispondran uno a la izquierda y el otro a la derecha
        # Si es 0 los reinos se dispondran uno arriba y el otro abajo
        orientacion_reino = randint(0, 1)

        if orientacion_reino:  # orientacion_reino != 0 -> 1 (izquierda/derecha)
            # Generamos aleatoriamente la posicion de la fila de los reinos
            # porque ya sabemos que la columna sera la primera y la ultima
            reino_1 = (randint(0, self.get_filas() - 1), 0)  # Primera columna
            reino_2 = (randint(0, self.get_filas() - 1), self.get_columnas() - 1)  # Última columna

        else:  # orientacion_reino == 0 (arriba/abajo)
            # Generamos aleatoriamente la posicion de la columna de los reinos
            # porque ya sabemos que la fila sera la primera y la ultima
            reino_1 = (0, randint(0, self.get_columnas() - 1))  # Primera fila
            reino_2 = (self.get_filas() - 1, randint(0, self.get_columnas() - 1))  # Última fila

        # Asignar regiones a los nodos del mapa
        for fila in range(self.get_filas()):
            for columna in range(self.get_columnas()):
                # La tupla con las coordenadas de la region a crear (fila, columna)
                punto = (fila, columna)
                # Accedemos al tipo de terreno de dicha coordenada
                tipo_terreno = self._terrenos.get(punto, 'desconocido')
                # Verificamos si la coordenada elegida es el reino 1 o 2
                es_reino = (punto == reino_1 or punto == reino_2)
                # Creamos la region desde la clase Region
                region = Region(punto, tipo_terreno, es_reino)
                # Se anyaden las conexiones de dicho nodo en la region si existe, sino simplemente ponemos una lista vacia
                region.set_conexiones(self._conexiones.get(punto, []))
                # Anyadimos la region al diccionario del mapa
                self.regiones[punto] = region

        # Generar recursos para cada región
        self.region_manager.regiones = self.regiones
        self.region_manager.generar_recursos()

    def __str__(self):
        """
        Devuelve una representación en cadena del mapa con la distribución de terrenos.

        Returns
        -------
        str
            Representación en cadena del mapa con la distribución de terrenos.
        """

        map_str = ''
        for fila in range(self._filas):
            for columna in range(self._columnas):
                punto = (fila, columna)  # Posición actual en el mapa
                if punto in self._terrenos:
                    map_str += f"{self._terrenos[punto]} "
                else:
                    map_str += "None "
            map_str += '\n'  # Nueva línea al final de cada fila
        return map_str



