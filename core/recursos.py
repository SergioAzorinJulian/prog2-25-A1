class Recurso:
    """
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
     atributo de instancia, es la cantidad de regeneracion del  recurso

     Metodos
     ---------
     __init__: constructor de la instancia
     __str__: muestra la info del objeto en formato str
     to_dict: convierte la instancia en formato de diccionario
     desde_dict: permite la construccion de la instancia desde la creacion de un diccionario con los datos
     __isub__: metodo para gestionar el uso de recursos, concretamente para el momento en que hay que gastar recursos
     __iadd__: gestion de recursos, en este caso para sumar un recurso obtenido al mismo ya regustristrado
     """

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
    def __init__(self, nombre: str, cantidad:int, regeneracion: int):
        """constructor del objeto recurso"""
        self.nombre = nombre
        self.cantidad = cantidad
        self.regeneracion = regeneracion
        self.creados[self.nombre] = self.to_dict()


    def __str__(self) -> str:
        """metodo para mostrar el recurso en formato str"""
        return f'{self.nombre}: {self.cantidad} unidades; regeneracion: {self.regeneracion}'
    def __repr__(self) -> str:
        """metodo para mostrar el recurso"""
        return f'Recurso(nombre= {self.nombre}, cantidad={self.cantidad}, regeneración= {self.regeneracion})'


    def to_dict(self) -> dict:
        """introduce la instancia en un diccionario"""
        return {
            'nombre': self.nombre,
            'cantidad': self.cantidad,
            'regeneracion': self.regeneracion
    }


    @classmethod
    def desde_dict(cls, datos: dict):
        """metodo para construir el objeto desde un diccionario"""
        nombre = datos['nombre']
        cantidad = datos['cantidad']
        regeneracion = datos['regeneracion']
        return cls(nombre, cantidad, regeneracion)


    def __isub__(self, other:int):
        """restar los recursos que van a ser utilizados"""
        if isinstance(other,Recurso):
            self.cantidad -= other.cantidad
        else:
            self.cantidad -= other
        return self

    def __iadd__(self, other: int):
        """agregar mas cantidad del recurso"""
        if isinstance(other,Recurso):
            self.cantidad += other.cantidad
        else:
            self.cantidad += other
        return self

    def regenerar(self):
        """cantidad de regeneracion del recurso -> Se regenera cada turno"""
        self.cantidad += self.regeneracion