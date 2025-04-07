

class Recurso():
    '''
    Con la clase recurso se crean los diferentes recursos
     Attributos
     -------------
     creados: dict
     atributo de clase que almacena los recursos creados
     nombre: str
     atributo de intancia, es el nombre del recurso
     cantidad: int
     atributo de instancia, es la cantidad de unidades del recurso
     regeneracion: int
     atribunto de instancia, es la cantidad de regeneracion del  recurso

     Metodos
     ---------
     __init__: constructor de la instancia
     __str__: muestra la info del objeto en formato str
     dict: convierte la instancia en formato de diccionario
     desde_dict: permite la construccion de la instancia desde la creacion de un diccionario con los datos
     '''

    PESOS_RECURSOS_BASE = {
        "madera": 4,
        "caza": 3,
        "recolección": 3,
        "agua": 3,
        "piedra": 2,
        "hierro": 2
    }

    RECURSOS_ESPECIALES = ["oro"]

    creados = {}
    def __init__(self, nombre: str, cantidad:int, regeneracion: int): # constructor del objeto recurso
        self.nombre = nombre
        self.cantidad = cantidad
        self.regeneracion = regeneracion
        self.creados[self.nombre] = self.dict()

    def __str__(self) -> str:  # metodo para mostrar el recurso
        return f'{self.nombre}: {self.cantidad} unidades; regeneracion: {self.regeneracion}'


    def dict(self) -> dict: # muestra la instancia en diccionario
        return {
            'nombre': self.nombre,
            'cantidad': self.cantidad,
            'regeneracion': self.regeneracion
    }
    @classmethod
    def desde_dict(cls, datos: dict): # clase abstracta para guardar el estado de los objetos
        nombre = datos['nombre']
        cantidad = datos['cantidad']
        regeneracion = datos['regeneracion']
        return cls(nombre, cantidad, regeneracion)








# los siguientes comentarios pueden ser utiles para la gestion de recursos
'''
    def regenerar(self):
            self.cantidad += self.regeneracion
            return self

    def __sub__(self, other:int) -> int: # permite gastar recursos
        try:
            other + 0
        except TypeError:
            raise TypeError(f'Se debe de introducir un valor numérico')
        if other > self.cantidad:
            raise ValueError(f'no tiene suficiente {self.nombre}')
        else:
            nueva_cantidad = self.cantidad - other
        return Recurso(self.nombre, nueva_cantidad, self.regeneracion)
    def __rsub__(self, other:int)->int:
        return other - self.cantidad
    def __add__(self,other:int)->int:
        try:
            other + 0
        except TypeError:
            raise TypeError(f'Se debe de introducir un valor numérico')
        nueva_cantidad = self.cantidad + other
        return Recurso(self.nombre, nueva_cantidad, self.regeneracion)
    def __radd__(self,other:int)->int:
        return other + self.cantidad
'''
