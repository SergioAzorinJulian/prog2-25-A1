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
     __sub__: metodo para gestionar el uso de recursos, concretamente para el momento en que hay que gastar recursos
     __rsub__: metodo para realizar operaciones aritmeticas correctas con el recurso
     __add__: gestion de recursos, en este caso para sumar un recurso obtenido al mismo ya regustristrado
     __radd__: metodo para realizar operaciones de suma correctas con la cantidad de un recurso
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
    def __init__(self, nombre: str, cantidad:int, regeneracion: int): # constructor del objeto recurso
        self.nombre = nombre
        self.cantidad = cantidad
        self.regeneracion = regeneracion
        self.creados[self.nombre] = self.to_dict()


    def __str__(self) -> str:  # metodo para mostrar el recurso
        return f'{self.nombre}: {self.cantidad} unidades; regeneracion: {self.regeneracion}'


    def to_dict(self) -> dict:
        """introduce la instancia en un diccionario"""
        return {
            'nombre': self.nombre,
            'cantidad': self.cantidad,
            'regeneracion': self.regeneracion
    }


    @classmethod
    def desde_dict(cls, datos: dict):
        nombre = datos['nombre']
        cantidad = datos['cantidad']
        regeneracion = datos['regeneracion']
        return cls(nombre, cantidad, regeneracion)


    def __sub__(self, other:int):
        """restar los recursos que van a ser utilizados"""
        try:
            other + 0
        except TypeError:
            print(f'Advertencia: No se puede restar "{other}" porque no es un valor numérico.')
        else:
            try:
                if other > self.cantidad:
                    print(f'Advertencia: No tiene suficiente {self.nombre}')
                else:
                    self.cantidad -= other
            except ValueError:
                print(f'Advertencia: No tiene suficiente {self.nombre}')
            except Exception as e:
                print(f'Error inesperado: {e}')
        return self.cantidad


    def __rsub__(self, other: int):
        """Realiza la resta con el recurso como operando derecho."""
        return self.__sub__(other)


    def __add__(self, other: int):
        """agregar mas cantidad del recurso"""
        try:
            other + 0
        except TypeError:
            print(f'Advertencia: No se puede agregar "{other}" porque no es un valor numérico.')
        else:
            self.cantidad += other
        return self.cantidad


    def __radd__(self,other:int):
        """Realiza la suma con el recurso como operando derecho."""
        return self.__add__(other)


    def regenerar(self):
        """cantidad de regeneracion del recurso"""
        self.cantidad = self.__add__(self.regeneracion)
        return self.cantidad