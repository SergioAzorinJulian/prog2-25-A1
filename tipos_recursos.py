
class Recurso():
    def __init__(self, nombre, cantidad:str):
        self.nombre = nombre
        self.cantidad = cantidad
    def obtener(self) -> int:
        print(f'se han obtenido {self.cantidad} de {self.nombre}')
        return self.cantidad
    def sumar(self, cantidad:int) -> int:
        self.cantidad += cantidad
        print(f'se han agregado {cantidad} piezas de {self.nombre}')
        print(f'ahora cuentas con {self.cantidad} piezas de {self.nombre}')
        return self.cantidad
    def gastar(self,cantidad:int) -> bool:
        if cantidad<=self.cantidad:
            self.cantidad -= cantidad
            print(f'se han usado {cantidad} piezas de {self.nombre}')
            print(f'ahora cuentas con {self.cantidad} piezas de {self.nombre}')
            return True
        else:
            print(f'no tiene suficiente {self.nombre} para realizar la acción')
            return False
    def mostrar_info(self)->str:
        return f'{self.nombre}: {self.cantidad} piezas'


class Madera(Recurso):
    def __init__(self, nombre:str, cantidad:int, construccion:str):
        super().__init__(nombre, cantidad)
        self.construccion = construccion
    def mostrar_info(self) -> str:
       return f'{self.nombre}: {self.cantidad} piezas'
    def construir(self,cantidad:int)->int:
        print(f'para construir {self.construccion} necesitas gastar {cantidad} piezas de {self.nombre}')
        super().gastar(cantidad)
    def sumar(self,cantidad:int)->int:
        super().sumar(cantidad)


class Hierro(Recurso):
    def __init__(self,nombre:str, cantidad:int, entrenamiento:str):
        super().__init__(nombre, cantidad)
        self.entrenamiento = entrenamiento
    def mostrar_info(self) -> str:
        return f'{self.nombre}: {self.cantidad} piezas'
    def entrenar(self,cantidad:int)->int:
        print(f'para entrenar {self.entrenamiento} necesitas gastar {cantidad} piezas de {self.nombre}')
        super().gastar(cantidad)
    def sumar(self,cantidad:int)->int:
        super().sumar(cantidad)


class Agua(Recurso):
    def __init__(self,nombre:str,cantidad:int, destino:str):
        super().__init__(nombre, cantidad)
        self.destino = destino
    def mostrar_info(self)->str:
        return f'{self.nombre}: {self.cantidad} piezas'
    def usar(self,cantidad:int)->int:
        print(f'para hidratar {self.destino} necesitas gastar {cantidad} piezas de {self.nombre}')
        super().gastar(cantidad)
    def sumar(self,cantidad:int)->int:
        super().sumar(cantidad)

        
class Comida(Recurso):
    def __init__(self,nombre:str,cantidad:int, destino:str):
        super().__init__(nombre, cantidad)
        self.destino = destino
    def mostrar_info(self)->str:
        return f'{self.nombre}: {self.cantidad} piezas'
    def usar(self,cantidad:int)->int:
        print(f'para alimentar {self.destino} necesitas gastar {cantidad} piezas de {self.nombre}')
        super().gastar(cantidad)
    def sumar(self,cantidad:int)->int:
        super().sumar(cantidad)

class Denario(Recurso):
    def __init__(self,nombre:str,cantidad:int, destino:str):
        super().__init__(nombre, cantidad)
        self.destino = destino
    def mostrar_info(self)->str:
        return f'{self.nombre}: {self.cantidad} piezas'
    def usar(self,cantidad:int)->int:
        print(f'para {self.destino} necesitas gastar {cantidad} piezas de {self.nombre}')
        super().gastar(cantidad)
    def sumar(self,cantidad:int)->int:
        super().sumar(cantidad)






