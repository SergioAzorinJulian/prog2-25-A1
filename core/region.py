from copy import deepcopy
from typing import List, Dict, Optional
from recursos import Recurso # Para poder referenciar el tipo de recurso en la region
from tropas import Tropa # Para poder referenciar el tipo de recurso en la region
from edificios import Edificio # Para poder referenciar el tipo de recurso en la region

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
    _recursos : List[Recurso]
        Recursos disponibles en la región.
    _edificios : dict
        Edificios construidos en la región.
    _tropas : dict
        Tropas presentes en la región.
    _conexiones : list
        Lista de conexiones con otras regiones.
    _lugar_especial : Optional[str]
        Lugar especial presente en la región.
    """

    def __init__(self, posicion: tuple[int, int], tipo_terreno: str, es_reino: bool = False, recursos_base: List[Recurso] = None):
        """
        Parameters
        ----------
        posicion : tuple[int, int]
            Coordenadas de la región en el mapa.
        tipo_terreno : str
            Tipo de terreno de la región.
        es_reino : bool, optional
            Indica si la región es un reino (por defecto es False).
        recursos_base : list, optional
            Recursos iniciales de la región (por defecto es None).
        """

        self._posicion = posicion
        self._propietario: str = 'Neutral'
        self._tipo_terreno = tipo_terreno
        self._es_reino = es_reino
        self._recursos = recursos_base
        self._edificios: Dict[str, Edificio] = {}
        self._tropas: Dict[str, Tropa] = {}
        self._conexiones: list = []
        self._lugar_especial: Optional[str] = None

    ### GETTERS ###
    def get_posicion(self):
        """Devuelve la posición de la región."""
        return deepcopy(self._posicion)

    def get_propietario(self):
        """Devuelve el propietario de la región."""
        return self._propietario

    def get_tipo_terreno(self):
        """Devuelve el tipo de terreno de la región."""
        return self._tipo_terreno

    def get_es_reino(self):
        """Devuelve si la región es un reino."""
        return self._es_reino

    def get_recursos(self):
        """Devuelve los recursos de la región."""
        return deepcopy(self._recursos)

    def get_edificios(self):
        """Devuelve los edificios de la región."""
        return deepcopy(self._edificios)

    def get_tropas(self):
        """Devuelve las tropas de la región."""
        return deepcopy(self._tropas)

    def get_conexiones(self):
        """Devuelve las conexiones de la región."""
        return deepcopy(self._conexiones)

    def get_lugar_especial(self):
        """Devuelve el lugar especial de la región."""
        return self._lugar_especial


    ### SETTERS ###
    def set_posicion(self, nueva_posicion: tuple[int, int]):
        """Establece la posición de la región."""
        self._posicion = nueva_posicion

    def set_propietario(self, nuevo_propietario: str):
        """Establece el propietario de la región."""
        self._propietario = nuevo_propietario

    def set_tipo_terreno(self, nuevo_tipo_terreno: str):
        """Establece el tipo de terreno de la región."""
        self._tipo_terreno = nuevo_tipo_terreno

    def set_es_reino(self, nuevo_es_reino: bool):
        """Establece si la región es un reino."""
        self._es_reino = nuevo_es_reino

    def set_recursos(self, nuevo_recursos: List[Recurso]):
        """Establece los recursos de la región."""
        self._recursos = nuevo_recursos

    def set_edificios(self, nuevos_edificios: Dict):
        """Establece los edificios de la región."""
        self._edificios = nuevos_edificios

    def set_tropas(self, nuevas_tropas: Dict):
        """Establece las tropas de la región."""
        self._tropas = nuevas_tropas

    def set_conexiones(self, nueva_conexiones: list):
        """Establece las conexiones de la región."""
        self._conexiones = nueva_conexiones

    def set_lugar_especial(self, nuevo_lugar: str):
        """Establece el lugar especial de la región."""
        self._lugar_especial = nuevo_lugar


    ### METODO PARA MOSTRAR INFORMACION SOBRE LA REGION ###
    def __str__(self) -> str:
        return (f"Posición: {self._posicion} | Terreno: {self._tipo_terreno} | Reino: {self._es_reino} | "
                f"Propietario: {self._propietario} | "
                f"Recursos: {self._recursos} | "
                f"Edificios: {self._edificios} | Tropas: {self._tropas}")

    def __repr__(self) -> str:
        """Devuelve una representacion de una region de manera mas "tecnica"."""
        return f"Region(pos={self._posicion}, terreno={self._tipo_terreno}, reino={self._es_reino}, recursos={self._recursos})"





