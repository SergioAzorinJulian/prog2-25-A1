from copy import deepcopy

class Region:
    """
    Clase que representa una región del mapa.

    Attributes
    ----------
    _posicion : tuple[int, int]
        Coordenadas de la región en el mapa.
    _propietario : str
        Nombre del propietario de la región.
    _tipo_terreno : str
        Tipo de terreno de la región.
    _es_reino : bool
        Indica si la región es un reino.
    _recursos : dict
        Recursos disponibles en la región.
    _edificios : dict
        Edificios construidos en la región.
    _tropas : dict
        Tropas presentes en la región.
    _conexiones : list
        Lista de conexiones con otras regiones.
    _lugar_especial : str or None
        Lugar especial presente en la región.
    """

    def __init__(self, posicion: tuple[int, int], tipo_terreno: str, es_reino: bool = False, recursos_base: dict = None):
        """
        Parameters
        ----------
        posicion : tuple[int, int]
            Coordenadas de la región en el mapa.
        tipo_terreno : str
            Tipo de terreno de la región.
        es_reino : bool, optional
            Indica si la región es un reino (por defecto es False).
        recursos_base : dict, optional
            Recursos iniciales de la región (por defecto es None).
        """

        self._posicion = posicion
        self._propietario: str = 'Neutral'
        self._tipo_terreno = tipo_terreno
        self._es_reino = es_reino
        self._recursos = recursos_base
        self._edificios: dict = {}
        self._tropas: dict = {}
        self._conexiones: list = []
        self._lugar_especial: str | None = None

    ### GETTERS ###
    def get_posicion(self):
        return deepcopy(self._posicion)

    def get_propietario(self):
        return self._propietario

    def get_tipo_terreno(self):
        return self._tipo_terreno

    def get_es_reino(self):
        return self._es_reino

    def get_recursos(self):
        return deepcopy(self._recursos)

    def get_edificios(self):
        return deepcopy(self._edificios)

    def get_tropas(self):
        return deepcopy(self._tropas)

    def get_conexiones(self):
        return deepcopy(self._conexiones)

    def get_lugar_especial(self):
        return self._lugar_especial


    ### SETTERS ###
    def set_posicion(self, nueva_posicion: tuple[int, int]):
        self._posicion = nueva_posicion

    def set_propietario(self, nuevo_propietario: str):
        self._propietario = nuevo_propietario

    def set_tipo_terreno(self, nuevo_tipo_terreno: str):
        self._tipo_terreno = nuevo_tipo_terreno

    def set_es_reino(self, nuevo_es_reino: bool):
        self._es_reino = nuevo_es_reino

    def set_recursos(self, nuevo_recursos: dict):
        self._recursos = nuevo_recursos

    def set_edificio(self, nuevo_edificios: dict):
        self._edificios = nuevo_edificios

    def set_tropas(self, nueva_tropas: dict):
        self._tropas = nueva_tropas

    def set_conexiones(self, nueva_conexiones: list):
        self._conexiones = nueva_conexiones

    def set_lugar_especial(self, nuevo_lugar: str):
        self._lugar_especial = nuevo_lugar


    ### METODOS PARA EDIFICIOS ###
    def construir_edificio(self, nombre: str, nivel: int = 1):
        """Añade un edificio o mejora su nivel."""
        try:
            if nombre in self._edificios:
                self._edificios[nombre] += 1
            else:
                self._edificios[nombre] = nivel
        except Exception as e:
            print('Error al construir edificio:', e)

    def eliminar_edificio(self, nombre: str):
        try:
            if nombre in self._edificios:
                del self._edificios[nombre]
        except Exception as e:
            print('Error al eliminar edificio:', e)

    ### METODOS PARA TROPAS ###     
    def agregar_tropa(self, tipo: str, cantidad: int):
        try:
            if tipo in self._tropas:
                self._tropas[tipo] += cantidad
            else:
                self._tropas[tipo] = cantidad
        except Exception as e:
            print('Error al agregar tropa:', e)

    def eliminar_tropa(self, tipo: str, cantidad: int):
        try:
            if tipo in self._tropas:
                self._tropas[tipo] -= cantidad
                if self._tropas[tipo] <= 0:
                    del self._tropas[tipo]
        except Exception as e:
            print('Error al eliminar tropa:', e)


    ### METODO PARA MOSTRAR INFORMACION SOBRE LA REGION ###
    def __str__(self) -> str:
        return (f"Posición: {self._posicion} | Terreno: {self._tipo_terreno} | Reino: {self._es_reino} | "
                f"Propietario: {self._propietario} | "
                f"Recursos: {self._recursos} | "
                f"Edificios: {self._edificios} | Tropas: {self._tropas}")

    def __repr__(self) -> str:
        """Returns a string representation of the region for debugging."""
        return f"Region(pos={self._posicion}, terreno={self._tipo_terreno}, reino={self._es_reino}, recursos={self._recursos})"





