
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
     atributo de instancia, es la cantidad de regeneracion del  recurso

     Metodos
     ---------
     __init__: constructor de la instancia
     __str__: muestra la info del objeto en formato str
     dict: convierte la instancia en formato de diccionario
     desde_dict: permite la construccion de la instancia desde la creacion de un diccionario con los datos
     __sub__: metodo para gestionar el uso de recursos, concretamente para el momento en que hay que gastar recursos
     __rsub__: metodo para realizar operaciones aritmeticas correctas con el recurso
     __add__: gestion de recursos, en este caso para sumar un recurso obtenido al mismo ya regustristado
     __radd__: metodo para realizar operaciones de suma correctas con la cantidad de un recurso
     '''
    creados = {}
    def __init__(self, nombre: str, cantidad:int, regeneracion: int): # constructor del objeto recurso
        self.nombre = nombre
        self.cantidad = cantidad
        self.regeneracion = regeneracion
        self.creados[self.nombre] = self.dict()

    def __str__(self) -> str:  # metodo para mostrar el recurso
        return f'{self.nombre}: {self.cantidad} unidades; regeneracion: {self.regeneracion}'


    def dict(self) -> dict:
        '''introduce la instancia en un diccionario'''
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
        '''restar los recursos que van a ser utilizados'''
        try:
            other + 0
        except TypeError:
            raise TypeError(f'Se debe de introducir un valor numérico')
        if other > self.cantidad:
            raise ValueError(f'no tiene suficiente {self.nombre}')
        else:
            self.cantidad -= other
        return self.cantidad

    def __rsub__(self, other:int):
        return other - self.cantidad

    def __add__(self,other:int):
        '''agregar mas cantidad del recurso'''
        try:
            other + 0
        except TypeError:
            raise TypeError(f'Se debe de introducir un valor numérico')
        self.cantidad += other
        return self.cantidad

    def __radd__(self,other:int):
        return other + self.cantidad
    def regenerar(self):
        '''cantidad de regeneracion del recurso'''
        self.cantidad = self.cantidad + self.__add__(self.regeneracion)
        return self.cantidad




















