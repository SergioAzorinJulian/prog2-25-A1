
class Recurso():
    def __init__(self, nombre: str, cantidad:int, regeneracion: int):
        self.nombre = nombre
        self.cantidad = cantidad
        self.regeneracion = regeneracion
    def __sub__(self, other:int) -> int:   # permite gastar recursos
        if other > self.cantidad:
            raise ValueError(f'no tiene suficiente {self.nombre}')
        else:
            nueva_cantidad = self.cantidad - other
        return Recurso(self.nombre, nueva_cantidad, self.regeneracion)
    def __rsub__(self, other:int)->int:
        return other - self.cantidad
    def __add__(self,other:int)->int:
        nueva_cantidad = self.cantidad + other
        return Recurso(self.nombre, nueva_cantidad, self.regeneracion)
    def __radd__(self,other:int)->int:
        return other + self.cantidad

    def __str__(self)->str:
        return f'{self.nombre}: {self.cantidad} unidades (regeneracion: {self.regeneracion})'
    def dict(self)->dict:
        return {
            'nombre': self.nombre,
            'cantidad': self.cantidad,
            'regeneracion': self.regeneracion
        }
    @classmethod
    def desde_dict(cls, datos: dict):
        return cls(datos['nombre'], datos['cantidad', datos['regeneracion'])

    def regenerar(self):
            self.cantidad += self.regeneracion
            return self



















