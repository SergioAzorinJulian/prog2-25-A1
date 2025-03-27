
# Tropas según Sergi
class Tropa:

    '''
    Clase en la que se encuentra todas las diferentes tropas

    ATRIBUTOS:
    -------------
    tropa_stats: Dic
    Diccionario empleado para almacenar las estadisticas de cada tropa

    recursos: int
    Número de recursos necesario para entrenar una tropa

    nombre: str
    Nombre de la tropa

    puntos_vida: float
    Puntos de vida de la tropa

    ataque: float
    Daño que hace la tropa

    METODOS:
    -----------
    añadir_tropa_stats: Metodo que añade la información de una cada tropa al diccionario tropa-stats (se activa cada vez que creas un objeto tropa, sea la tropa que sea)

    rellenar_tropa_stats: Metodo ligado a añadir_tropa_stats, se encarga de crear un objeto de cada tropa, siendo añadido inmediatamente al diccionario de las estadisticas mediante añadir_tropa_stats

    '''
    tropa_stats = {}
    def __init__(self,recursos=int, nombre=str, puntos_vida=float, ataque=float):
        self.nombre = nombre
        self.puntos_vida = puntos_vida
        self.ataque = ataque
        self.recursos=recursos


    def anadir_tropa_stats(self):
        Tropa.tropa_stats[self.nombre]=self   #Añadimos al diccionario el objeto, se puede acceder a él por el nombre de tropa


    @staticmethod
    def rellenar_tropa_stats():
        soldado = Soldado()    #Creamos un objeto de cada clase tropa
        caballero = Caballero()
        arquero = Arquero()
        ogro = Ogro()
        ballestero = Ballestero()
        mago = Mago()
        catapulta= Catapulta()
        escudero=Escudero()



class TropaAtaque(Tropa):

    '''
    Clase de la que heredarán las tropas de tipo "Ataque"
    '''

    def __init__(self,recursos=int, nombre=str, puntos_vida=float, ataque=float):
        super().__init__(recursos,nombre, puntos_vida, ataque)





class TropaDefensa(Tropa):
    '''
    Clase de la que heredarán las tropas de tipo "Ataque"
    '''

    def __init__(self, recursos=int, nombre=str, puntos_vida=float, ataque=float):
        super().__init__(recursos, nombre, puntos_vida, ataque)





class TropaAlcance(Tropa):
    '''
    Clase de la que heredarán las tropas de tipo "Ataque"
    '''
    def __init__(self, recursos=int, nombre=str, puntos_vida=float, ataque=float):
        super().__init__(recursos, nombre, puntos_vida, ataque)


# TROPAS DE ATAQUE
class Soldado(TropaAtaque):

    def __init__(self, recursos=50, nombre='soldado', puntos_vida=100, ataque=100):
        super().__init__(recursos,nombre, puntos_vida, ataque)
        super().anadir_tropa_stats()

class Caballero(TropaAtaque):

    def __init__(self, recursos= 70, nombre='caballero', puntos_vida=200, ataque=85):
        super().__init__( recursos, nombre, puntos_vida, ataque)
        super().anadir_tropa_stats()
# TROPAS DE DEFENSA
class Ogro(TropaDefensa):

    def __init__(self, recursos=80, nombre='ogro', puntos_vida=250, ataque=60):
        super().__init__( recursos, nombre, puntos_vida, ataque)
        super().anadir_tropa_stats()

class Escudero(TropaDefensa):

    def __init__(self, recursos=50, nombre='escudero', puntos_vida=150, ataque=50):
        super().__init__(recursos, nombre, puntos_vida, ataque)
        super().anadir_tropa_stats()

# TROPAS DE ALCANCE
class Arquero(TropaAlcance):

    def __init__(self,  recursos=80, nombre='arquero', puntos_vida=50, ataque=150):
        super().__init__( recursos, nombre, puntos_vida, ataque)
        super().anadir_tropa_stats()


class Ballestero(TropaAlcance):

    def __init__(self, recursos=100, nombre='ballestero', puntos_vida=300, ataque=70):
        super().__init__( recursos, nombre, puntos_vida, ataque)
        super().anadir_tropa_stats()


class Mago(TropaAlcance):

    def __init__(self, recursos=110, nombre='mago', puntos_vida=100, ataque=110):
        super().__init__(recursos, nombre, puntos_vida, ataque)
        super().anadir_tropa_stats()


class Catapulta(TropaAlcance):

    def __init__(self, recursos=350, nombre='catapulta', puntos_vida=400, ataque=200):
        super().__init__(recursos, nombre, puntos_vida, ataque)
        super().anadir_tropa_stats()



'''
#TROPAS de Tomás

from abc import ABC, abstractmethod

class Tropa(ABC):
    def __init__(self, nombre: str, puntos_vida: float, ataque: float, defensa: float):
        self.nombre = nombre
        self.puntos_vida = puntos_vida
        self.ataque = ataque
        self.defensa = defensa

    @abstractmethod
    def atacar(self, objetivo: "Tropa"):
        pass

    @abstractmethod
    def recibir_dano(self, dano: float):
        pass


# -----------------------------------------------
# CLASES INTERMEDIAS
# -----------------------------------------------

class TropaAtaque(Tropa):
    """ TROPAS DESTINADAS PARA ATACAR, ALTO ATAQUE Y BAJA DEFENSA """
    def __init__(self, nombre: str, puntos_vida: float, ataque: float, defensa: float, bono_ataque: float):
        super().__init__(nombre, puntos_vida, ataque, defensa)
        self.bono_ataque = bono_ataque
        self.ataque += self.bono_ataque

    def atacar(self, objetivo: "Tropa"):
        super().atacar(objetivo)
        print(f"{self.nombre} ataca a {objetivo.nombre}")
        dano = self.ataque - objetivo.defensa
        objetivo.recibir_dano(dano)

    def recibir_dano(self, dano: float):
        super().recibir_dano(dano)
        self.puntos_vida -= dano
        print(f"{self.nombre} fue atacado y recibe {dano} de daño. Vida restante: {self.puntos_vida}")
        if self.puntos_vida <= 0:
            print(f"{self.nombre} ha sido derrotado.")

    def ataque_especial(self, objetivo: "Tropa"):
        dano = self.ataque * 1.5
        objetivo.recibir_dano(dano)
        print(f"{self.nombre} usa un ATAQUE ESPECIAL contra {objetivo.nombre}.")


class TropaDefensa(Tropa):
    """ TROPAS DESTINADAS PARA DEFENDER, ALTA DEFENSA Y BAJO ATAQUE """
    def __init__(self, nombre: str, puntos_vida: float, ataque: float, defensa: float, armadura_extra: float):
        super().__init__(nombre, puntos_vida, ataque, defensa)
        self.armadura_extra = armadura_extra
        self.defensa += self.armadura_extra

    def atacar(self, objetivo: "Tropa"):
        super().atacar(objetivo)
        print(f"{self.nombre} ataca a {objetivo.nombre}")
        dano = self.ataque - objetivo.defensa
        objetivo.recibir_dano(dano)

    def recibir_dano(self, dano: float):
        """ Reduccion de daño por alta defensa """
        dano_reducido = dano - self.defensa
        super().recibir_dano(dano_reducido)
        print(f"{self.nombre} reduce el daño recibido a {dano_reducido} por su armadura extra.")


class TropaApoyo(Tropa):
    """ TROPAS QUE AYUDAN CON CURACIONES """
    def __init__(self, nombre: str, puntos_vida: float, ataque: float, defensa: float, curaciones: float):
        super().__init__(nombre, puntos_vida, ataque, defensa)
        self.curaciones = curaciones

    def atacar(self, objetivo: "Tropa"):
        super().atacar(objetivo)
        print(f"{self.nombre} ataca a {objetivo.nombre}")
        dano = self.ataque - objetivo.defensa
        objetivo.recibir_dano(dano)

    def recibir_dano(self, dano: float):
        super().recibir_dano(dano)
        self.puntos_vida -= dano
        print(f"{self.nombre} fue atacado y recibe {dano} de daño. Vida restante: {self.puntos_vida}")
        if self.puntos_vida <= 0:
            print(f"{self.nombre} ha sido derrotado.")

    def curar(self, aliado : "Tropa"):
        if aliado.puntos_vida > 0:
            aliado.puntos_vida += self.curaciones
            print(f"{self.nombre} cura a {aliado.nombre} con {self.curaciones} puntos de vida.")
        else:
            print(f"{aliado.nombre} fue derrotado y no puede ser curado.")

    def revivir_aliado(self, aliado= "Tropa"):
        if aliado.puntos_vida <= 0:
            aliado.puntos_vida = self.curaciones    #--> revive con la vida que tiene de curaciones el curador
            print(f"{self.nombre} ha revivido a {aliado.nombre} con {self.curaciones} de vida.")
        else:
            print(f"{aliado.nombre} todavia sigue vivo, no puede ser revivido.")

# -----------------------------------------------
# CLASES ESPECIFICAS DE TROPAS
# -----------------------------------------------

# TROPAS DE ATAQUE
class Caballero(TropaAtaque):
    def __init__(self):
        super().__init__("Caballero", puntos_vida=80.00, ataque=12.50, defensa=6.00, bono_ataque=2.50)


class Arquero(TropaAtaque):
    def __init__(self):
        super().__init__("Arquero", puntos_vida=50.00, ataque=15.00, defensa=5.00, bono_ataque=4.00)


# TROPAS DE DEFENSA
class Ballestero(TropaDefensa):
    def __init__(self):
        super().__init__("Ballestero", puntos_vida=70.00, ataque=8.00, defensa=15.00, armadura_extra=5.00)

class Escudero(TropaDefensa):
    def __init__(self):
        super().__init__("Escudero", puntos_vida=120.00, ataque=6.00, defensa=18.00, armadura_extra=8.00)


# TROPAS DE CURACION
class Mago(TropaApoyo):
    def __init__(self):
        super().__init__("Mago", puntos_vida=50.00, ataque=8.00, defensa=4.00, curaciones=20.00)

class Sacerdote(TropaApoyo):
    def __init__(self):
        super().__init__("Sacerdote", puntos_vida=70.00, ataque=5.00, defensa=6.50, curaciones=25.00)
        '''
