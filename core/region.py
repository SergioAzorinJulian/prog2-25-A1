from copy import deepcopy
from typing import List, Optional
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
    recursos : List[Recurso]
        Recursos disponibles en la región.
    edificios : list[Edificio]
        Edificios construidos en la región.
    tropas : List[Tropa]
        Tropas presentes en la región.
    _conexiones : list
        Lista de conexiones con otras regiones.
    _lugar_especial : Optional[str]
        Lugar especial presente en la región.
    _nombre_reino : Optional[str]
        Nombre específico de la región si es un reino.
    """

    def __init__(self, posicion: tuple[int, int], tipo_terreno: str, es_reino: bool = False, recursos_base: List[Recurso] = None, nombre_reino: Optional[str] = None, propietario: str = 'Neutral'):
        """
        Parameters
        ----------
        posicion : tuple[int, int]
            Coordenadas de la región en el mapa.
        tipo_terreno : str
            Tipo de terreno de la región.
        es_reino : bool, optional
            Indica si la región es un reino (por defecto es False).
        recursos_base : List[Recurso], optional
            Recursos iniciales de la región (por defecto es None).
        nombre_reino : Optional[str]
            Nombre específico de la región si es un reino (por defecto es None).
        propietario : str, optional
            Nombre del propietario de la región (por defecto es 'Neutral').
        """

        self._posicion = posicion
        self._propietario: str = propietario
        self._tipo_terreno = tipo_terreno
        self._es_reino = es_reino
        self.recursos = recursos_base
        self.edificios: list[Edificio] = []
        self.tropas: list[Tropa] = []
        self._conexiones: list = []
        self._lugar_especial: Optional[str] = None
        self._nombre_reino = nombre_reino if self._es_reino else f""

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
        return deepcopy(self.recursos)

    def get_edificios(self):
        """Devuelve los edificios de la región."""
        return deepcopy(self.edificios)

    def get_tropas(self):
        """Devuelve las tropas de la región."""
        return deepcopy(self.tropas)

    def get_conexiones(self):
        """Devuelve las conexiones de la región."""
        return deepcopy(self._conexiones)

    def get_lugar_especial(self):
        """Devuelve el lugar especial de la región."""
        return self._lugar_especial

    def get_nombre_reino(self):
        """Devuelve el nombre especifico de la region."""
        return self._nombre_reino


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
        self.recursos = nuevo_recursos

    def set_edificios(self, nuevos_edificios: list[Edificio]):
        """Establece los edificios de la región."""
        self.edificios = nuevos_edificios

    def set_tropas(self, nuevas_tropas: list[Tropa]):
        """Establece las tropas de la región."""
        self.tropas = nuevas_tropas

    def set_conexiones(self, nueva_conexiones: list):
        """Establece las conexiones de la región."""
        self._conexiones = nueva_conexiones

    def set_lugar_especial(self, nuevo_lugar: str):
        """Establece el lugar especial de la región."""
        self._lugar_especial = nuevo_lugar

    def set_nombre_reino(self, nuevo_nombre: str):
        """Establece el nombre especifico de la region."""
        self._nombre_reino = nuevo_nombre


    ### METODO PARA MOSTRAR INFORMACION SOBRE LA REGION ###
    def __str__(self) -> str:
        tropas_str = ''
        for troop in self.tropas:
            tropas_str += f' {troop.__str__()} |\n'

        recursos_str = ''
        for resource in self.recursos:
            recursos_str += f' {resource.__str__()} |\n'

        edificios_str = ''
        for edificio in self.edificios:
            edificios_str += f' {edificio.__str__()} |\n'

        mensaje = (f"Posición: {self._posicion} | Terreno: {self._tipo_terreno} | Reino: {self._es_reino} | \n"
                f"Propietario: {self._propietario} |\n"
                f"Recursos: \n{recursos_str}"
                f"Edificios: \n{edificios_str}"
                f"Tropas: \n{tropas_str}")

        return mensaje if not self.get_es_reino() else mensaje + f"Nombre: {self.get_nombre_reino()} |"

    def __repr__(self) -> str:
        """Devuelve una representacion de una region de manera mas "tecnica"."""
        mensaje = f"Region(pos={self._posicion}, terreno={self._tipo_terreno}, reino={self._es_reino}, recursos={self.recursos})"
        return mensaje if not self.get_es_reino() else mensaje + f" | Nombre: {self.get_nombre_reino()}"




