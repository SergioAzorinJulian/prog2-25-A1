import random
import math
class Recurso:
    """
    Con la clase recurso se crean los diferentes recursos

     Attributos
     -------------
     PESOS_RECURSOS_BASE : dict
        Atributo de clase que define los pesos para la generación de recursos base.
    RECURSOS_ESPECIALES : list
        Atributo de clase que define los recursos especiales.
    creados : dict
        Atributo de clase que almacena los recursos creados.
    nombre : str
        Nombre del recurso.
    cantidad : int
        Cantidad de unidades del recurso.
    regeneracion : int
        Cantidad de regeneración del recurso por turno.
    valor_max : int
        valor maximo de regeneracion de un recurso


     Metodos
     ---------
     __init__(nombre: str, cantidad: int, regeneracion: int)
        Constructor de la clase Recurso.
    __str__() -> str
        Retorna una representación en cadena del recurso.
    to_dict() -> dict
        Convierte la instancia del recurso en un diccionario.
    desde_dict(datos: dict)
        Crea una instancia de Recurso a partir de un diccionario.
    __isub__(other: int)
        Resta la cantidad especificada al recurso.
    __iadd__(other: int)
        Añade la cantidad especificada al recurso.
    regenerar()
        Regenera el recurso en la cantidad definida en el atributo 'regeneracion'.
    """

    PESOS_RECURSOS_BASE = {
        "madera": 4,
        "caza": 3,
        "recolección": 3,
        "agua": 3,
        "piedra": 2,
        "hierro": 2,
    }

    RECURSOS_ESPECIALES = ["oro"]

    creados = {}

    def __init__(self, nombre: str, cantidad: int, regeneracion: int, valor_max: int = 300):
        """
        Inicializa un nuevo recurso con nombre y cantidad.

        Parámetros
        ----------
        nombre : str
            Nombre del recurso.
        cantidad : int
            Cantidad inicial del recurso.
        """

        self.nombre = nombre
        self.cantidad = cantidad
        self.regeneracion = regeneracion
        self.valor_max = valor_max
        self.creados[self.nombre] = self.to_dict()


    def to_dict(self) -> dict:
        """
        Convierte la instancia del recurso en un diccionario.

        Returns
        -------
        dict
            Diccionario con los atributos del recurso: nombre, cantidad y regeneración.
        """

        return {
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "regeneracion": self.regeneracion,
        }


    @classmethod
    def desde_dict(cls, datos: dict):
        """
        Construye una instancia de Recurso a partir de un diccionario.

        Parameters
        ----------
        datos : dict
            Diccionario con las claves 'nombre', 'cantidad', 'regeneracion' y 'valor_max' que representan
            los atributos del recurso.

        Returns
        -------
        Recurso
            Instancia de la clase Recurso creada a partir del diccionario proporcionado.
        """
        nombre = datos["nombre"]
        cantidad = datos["cantidad"]
        regeneracion = datos["regeneracion"]
        valor_maximo = datos["valor_max"]

        return cls(nombre, cantidad, regeneracion, valor_maximo)


    def __str__(self) -> str:
        """
        Devuelve una representación en cadena del recurso.

        Returns
        -------
        str
            Representación en cadena del recurso.
        """

        if self.regeneracion > 0:
            return f"{self.nombre.capitalize():<11}: {self.cantidad:<4} unidades | Tasa de regeneración: {self.regeneracion:<3}"
        else:
            return f"{self.nombre.capitalize():<11}: {self.cantidad:<4} unidades"


    def __repr__(self) -> str:
        """
        Devuelve una representación detallada del recurso, incluyendo su cantidad actual,
        valor máximo y tasa de regeneración.

        Returns
        -------
        str
            Cadena con el nombre, cantidad actual, valor máximo y tasa de regeneración del recurso.
        """

        return f"{self.nombre.capitalize():<11}: {self.cantidad:<4}/{self.valor_max:<4} unidades | Tasa de regeneración: {self.regeneracion:<3}"


    def __sub__(self, other: int):
        """
        Resta una cantidad o la cantidad de otro recurso a este recurso y devuelve una nueva instancia.

        Parameters
        ----------
        other : int or Recurso
            Cantidad a restar o instancia de Recurso cuya cantidad será restada.

        Returns
        -------
        Recurso
            Nueva instancia de Recurso con la cantidad resultante.

        Raises
        ------
        TypeError
            Si `other` no es un entero ni una instancia de Recurso.
        """

        nueva_cantidad = self.cantidad
        if isinstance(other, Recurso):
            nueva_cantidad -= other.cantidad
        else:
            nueva_cantidad -= other

        return self.__class__(self.nombre,nueva_cantidad,self.regeneracion,self.valor_max)


    def __isub__(self, other: int):
        """
        Resta una cantidad o la cantidad de otro recurso a este recurso, modificando la instancia actual.

        Parámetros
        ----------
        other : int o Recurso
            Cantidad a restar o instancia de Recurso cuya cantidad será restada.

        Retorna
        -------
        Recurso
            La instancia actual de Recurso con la cantidad actualizada.
        """

        if isinstance(other, Recurso):
            self.cantidad -= other.cantidad
        else:
            self.cantidad -= other
        return self


    def __iadd__(self, other: int):
        """
        Incrementa la cantidad del recurso sumando una cantidad o la cantidad de otro recurso.

        Parámetros
        ----------
        other : int o Recurso
            Cantidad a sumar o instancia de Recurso cuya cantidad será sumada.

        Retorna
        -------
        Recurso
            La instancia actual de Recurso con la cantidad actualizada.
        """
        if isinstance(other, Recurso):
            self.cantidad += other.cantidad
        else:
            self.cantidad += other
        return self


    def __mul__(self,other : int):
        """
        Multiplica la cantidad del recurso por un valor entero y retorna una nueva instancia.

        Parameters
        ----------
        other : int
            Valor por el cual se multiplicará la cantidad del recurso.

        Returns
        -------
        Recurso
            Nueva instancia de Recurso con la cantidad multiplicada.
        """

        return self.__class__(self.nombre,math.ceil(self.cantidad * other),self.regeneracion,self.valor_max)

    
    def __imul__(self, other : int):
        """
        Multiplica la cantidad del recurso por un valor entero, modificando la instancia actual.

        Parameters
        ----------
        other : int
            Valor por el cual se multiplicará la cantidad del recurso.

        Returns
        -------
        Recurso
            La instancia actual de Recurso con la cantidad actualizada.
        """

        self.cantidad *= other
        return self


    def __eq__(self, other):
        """
        Compara si dos recursos son iguales por su nombre.

        Parámetros
        ----------
        other : object
            Objeto a comparar, puede ser una instancia de Recurso.

        Returns
        -------
        bool
            True si ambos recursos tienen el mismo nombre, False en caso contrario.
        """

        if isinstance(other, Recurso):
            return self.nombre == other.nombre
        return False

    def __ge__(self, other):
        """
        Compara si la cantidad de este recurso es mayor o igual que la de otro recurso.

        Parameters
        ----------
        other : Recurso
            Instancia de Recurso con la que se compara la cantidad.

        Returns
        -------
        bool
            True si la cantidad de este recurso es mayor o igual que la de `other`, False en caso contrario.
        """

        if isinstance(other, Recurso):
            return self.cantidad >= other.cantidad
        return False


    def regenerar(self, porcentaje):
        """
        Regenera la cantidad del recurso en función de un porcentaje de su tasa de regeneración.

        Parameters
        ----------
        porcentaje : float o int
            Porcentaje de la tasa de regeneración que se aplicará para incrementar la cantidad del recurso.

        Returns
        -------
        None

        Notas
        -----
        Si la cantidad resultante supera el valor máximo (`valor_max`), se ajusta al valor máximo permitido.
        """

        percent = porcentaje / 100
        cant_regenerada = self.regeneracion * percent
        self.cantidad += cant_regenerada
        
        if self.cantidad > self.valor_max:
            self.cantidad = self.valor_max

