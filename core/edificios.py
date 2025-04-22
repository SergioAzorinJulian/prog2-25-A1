from recursos import Recurso

class Edificio:
    """
    La clase Edificio representa cualquier estructura dentro del reino.
    Es la clase base para todos los edificios.

    Atributos
    ----------
    nombre : str - Nombre del edificio.
    nivel : int - Nivel actual del edificio.
    Métodos
    ---------
    __init__ : Constructor de la instancia.
    subir_nivel : Sube el nivel del edificio si hay suficientes recursos y familias disponibles.
    __str__ : Devuelve información del edificio.
    """
    def __init__(self, nombre: str, nivel: int = 1,efectividad : float = 0.5):
        self.nombre = nombre
        self.nivel = nivel
        self.efectividad = efectividad

    def subir_nivel(self,recursos_jugador : list) -> str:
        if recursos_jugador[recursos_jugador.index(self.__class__.costo)] >= self.__class__.costo * self.nivel:
            recursos_jugador[recursos_jugador.index(self.__class__.costo)] -= self.__class__.costo * self.nivel
            self.nivel += 1
            self.efectividad += 0.2
        else:
            return f'Recurso {self.__class__.costo} insuficiente'
    def producir(self,recursos_region : list[Recurso], recursos_jugador : list[Recurso]) -> None:
        if self.__class__.produce in recursos_region:
            recurso_region = recursos_region[recursos_region.index(self.__class__.produce)]
            recurso_nuevo = recurso_region - recurso_region * self.efectividad
            recursos_region[recursos_region.index(self.__class__.produce)] -= recurso_nuevo
            recursos_jugador[recursos_jugador.index(self.__class__.produce)] += recurso_nuevo
        else:
            return None
    def __str__(self) -> str:
        return f'{self.nombre}: Nivel={self.nivel}, Efectividad={self.efectividad}, Costo={self.__class__.costo}, Produce={self.__class__.produce}'


class Mina(Edificio):
    '''
    Descripción: representa una mina que produce piedra.

    INFORMACIÓN
     ----------------------------------------
     - produce: piedra
     - costo: 15 piedra
    '''
    costo = [Recurso('piedra',15,0)]
    produce = Recurso('piedra',0,0)
    def __init__(self, nombre = 'Mina', nivel = 1, efectividad = 0.5):
        super().__init__(nombre, nivel, efectividad)

class Pozo(Edificio):
    '''
    Representa un pozo que produce agua.

    INFORMACIÓN
    ----------------------------------------
    - Recurso producido: agua
    - Construcción: 15 madera
    '''
    costo = [Recurso('madera',15,0)]
    produce = Recurso('agua',0,0)
    def __init__(self, nombre = 'Pozo', nivel = 1, efectividad = 0.5):
        super().__init__(nombre, nivel, efectividad)
