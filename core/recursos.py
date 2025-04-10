import random
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

    def __init__(self, nombre: str, cantidad: int, regeneracion: int, valor_max: int):
        """constructor del objeto recurso"""
        self.nombre = nombre
        self.cantidad = cantidad
        self.regeneracion = regeneracion
        self.valor_max = valor_max
        self.creados[self.nombre] = self.to_dict()

    def __str__(self) -> str:
        """metodo para mostrar el recurso"""
        return f"{self.nombre}: {self.cantidad} unidades; regeneracion: {self.regeneracion}"
    def __repr__(self) -> str:
        """metodo para mostrar el recurso"""
        return f"Recurso(nombre = {self.nombre}, cantidad = {self.cantidad}, regeneracion = {self.regeneracion})"

    def to_dict(self) -> dict:
        """introduce la instancia en un diccionario"""
        return {
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "regeneracion": self.regeneracion,
        }

    @classmethod
    def desde_dict(cls, datos: dict):
        """metodo para construir el objeto desde un diccionario"""
        nombre = datos["nombre"]
        cantidad = datos["cantidad"]
        regeneracion = datos["regeneracion"]
        return cls(nombre, cantidad, regeneracion)

    def __isub__(self, other: int):
        """restar los recursos que van a ser utilizados"""
        if isinstance(other, Recurso):
            self.cantidad -= other.cantidad
        else:
            self.cantidad -= other
        return self

    def __iadd__(self, other: int):
        """agregar mas cantidad del recurso"""
        if isinstance(other, Recurso):
            self.cantidad += other.cantidad
        else:
            self.cantidad += other
        return self

    def regenerar(self):
        """cantidad de regeneracion del recurso -> Se regenera cada turno"""
        porcentaje = random.randint(20,100)
        self.valor_max /= (porcentaje / 100)
        self.cantidad += self.valor_max
