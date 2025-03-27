
class Recurso():
    def __init__(self, nombre: str, cantidad:int, regeneracion: int):
        self.nombre = nombre
        self.cantidad = cantidad
        self.regeneracion = regeneracion

    def __str__(self) -> str:  # almacena más del mismo recurso
        return f'{self.nombre}: {self.cantidad} unidades (regeneracion: {self.regeneracion})'

    def dict(self) -> dict:
        return {
            'nombre': self.nombre,
            'cantidad': self.cantidad,
            'regeneracion': self.regeneracion
    }
    @classmethod
    def desde_dict(cls, datos: dict):
        return cls(datos['nombre'], datos['cantidad'], datos['regeneracion'])

    def regenerar(self):
            self.cantidad += self.regeneracion
            return self

 #   def __sub__(self, other:int) -> int: # permite gastar recursos
  #      try:
  #          other + 0
  #      except TypeError:
   #         raise TypeError(f'Se debe de introducir un valor numérico')
#     if other > self.cantidad:
 #           raise ValueError(f'no tiene suficiente {self.nombre}')
#        else:
 #           nueva_cantidad = self.cantidad - other
#        return Recurso(self.nombre, nueva_cantidad, self.regeneracion)
  #  def __rsub__(self, other:int)->int:
 #       return other - self.cantidad
#    def __add__(self,other:int)->int:
#        try:
#            other + 0
#        except TypeError:
#            raise TypeError(f'Se debe de introducir un valor numérico')
#        nueva_cantidad = self.cantidad + other
#        return Recurso(self.nombre, nueva_cantidad, self.regeneracion)
#    def __radd__(self,other:int)->int:
#        return other + self.cantidad

'''Con la clase recurso se crean los diferentes recursos
 Attributos
 -------------
 nombre: el nombre del recurso
 cantidad: cantidad de unidades del recurso
 regeneracion: cantidad de regeneracion del  recurso
 
 Metodos
 ---------
 __str__: muestra la info del objeto
 dict: convierte la instancia en diccionario
 desde_dict: guarda el estado de los objetos
 '''




















