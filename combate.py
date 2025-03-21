#TROPAS



class Tropa(ABC):
    def __init__(self, numero: int, recursos: int, nombre:str , puntos_vida: float, ataque: float):

        self.nombre = nombre
        self.puntos_vida = puntos_vida
        self.ataque = ataque
        self.numero=numero
        self.recursos=recursos



# -----------------------------------------------
# CLASES INTERMEDIAS
# -----------------------------------------------

class TropaAtaque(Tropa):
    def __init__(self, numero: int, recursos: int, nombre:str , puntos_vida: float, ataque: float):
        super().__init__(numero, recursos,nombre, puntos_vida, ataque)





class TropaDefensa(Tropa):
    def __init__(self, numero: int, recursos: int, nombre: str, puntos_vida: float, ataque: float):
        super().__init__(numero, recursos, nombre, puntos_vida, ataque)





class TropaApoyo(Tropa):
    def __init__(self, numero: int, recursos: int, nombre: str, puntos_vida: float, ataque: float):
        super().__init__(numero, recursos, nombre, puntos_vida, ataque)


# TROPAS DE ATAQUE
class Soldado(TropaAtaque):
    Soldados={}
    def __init__(self, numero: int, recursos=50, nombre='Soldado', puntos_vida=100, ataque=100):
        super().__init__(numero, recursos, nombre, puntos_vida, ataque)


class Caballero(TropaAtaque):
    Caballeros={}
    def __init__(self, numero: int, recursos= 70, nombre='Caballero', puntos_vida=200, ataque=85):
        super().__init__(numero, recursos, nombre, puntos_vida, ataque)


class Arquero(TropaAtaque):
    Arqueros={}
    def __init__(self, numero: int, recursos=80, nombre='Arquero', puntos_vida=50, ataque=150):
        super().__init__(numero, recursos, nombre, puntos_vida, ataque)


# TROPAS DE DEFENSA
class Ballestero(TropaDefensa):
    Ballesteros={}
    def __init__(self, numero: int, recursos=100, nombre='Ballestero', puntos_vida=300, ataque=70):
        super().__init__(numero, recursos, nombre, puntos_vida, ataque)


# TROPAS DE CURACION
class Mago(TropaApoyo):
    Magos={}
    def __init__(self, numero: int, recursos=110, nombre='Mago', puntos_vida=100, ataque=110):
        super().__init__(numero, recursos, nombre, puntos_vida, ataque)





Mago1=Mago(5)
Mago2=Mago(4)
Caballero1=Caballero(4)
Caballero2=Caballero(3)
Ballestero1=Ballestero(3)
Ballestero2=Ballestero(3)




class Combate:
    escenario_batalla={'atacantes':['','',''],'defensores':['','','']}
    @staticmethod
    def preparando_batalla(tropas_ataque,tropas_defensa):
        

























