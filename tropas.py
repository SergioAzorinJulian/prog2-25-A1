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
        hueste = Hueste()



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


class Hueste(TropaAtaque):

    def __init__(self, recursos=100, nombre='hueste', puntos_vida=200, ataque=120):
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
