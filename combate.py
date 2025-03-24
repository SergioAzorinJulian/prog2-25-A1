#Tropas


from Region import Region

Region.Regiones[(0,0)]=Region((0,0),'terreno',False)
class Tropa:
    tropa_stats = {}
    def __init__(self,recursos=int, nombre=str, puntos_vida=float, ataque=float):
        self.nombre = nombre
        self.puntos_vida = puntos_vida
        self.ataque = ataque
        self.recursos=recursos


    def anadir_tropa(self):
        Tropa.tropa_stats[self.nombre]={}
        Tropa.tropa_stats[self.nombre]['recursos']=self.recursos
        Tropa.tropa_stats[self.nombre]['puntos_vida']=self.puntos_vida
        Tropa.tropa_stats[self.nombre]['ataque'] = self.ataque

    @staticmethod
    def rellenar_tropa_stats():
        soldado = Soldado()
        caballero = Caballero()
        arquero = Arquero()
        ogro = Ogro()
        ballestero = Ballestero()
        mago = Mago()

# TROPAS DE ATAQUE
class Soldado(TropaAtaque):

    def __init__(self, recursos=50, nombre='Soldado', puntos_vida=100, ataque=100):
        super().__init__(recursos,nombre, puntos_vida, ataque)
        super().anadir_tropa()

class Caballero(TropaAtaque):

    def __init__(self, recursos= 70, nombre='Caballero', puntos_vida=200, ataque=85):
        super().__init__( recursos, nombre, puntos_vida, ataque)
        super().anadir_tropa()
# TROPAS DE DEFENSA
class Ogro(TropaDefensa):

    def __init__(self, recursos=80, nombre='Ogro', puntos_vida=250, ataque=60):
        super().__init__( recursos, nombre, puntos_vida, ataque)
        super().anadir_tropa()
# TROPAS DE ALCANCE
class Arquero(TropaAlcance):

    def __init__(self,  recursos=80, nombre='Arquero', puntos_vida=50, ataque=150):
        super().__init__( recursos, nombre, puntos_vida, ataque)
        super().anadir_tropa()


class Ballestero(TropaAlcance):

    def __init__(self, recursos=100, nombre='Ballestero', puntos_vida=300, ataque=70):
        super().__init__( recursos, nombre, puntos_vida, ataque)
        super().anadir_tropa()


class Mago(TropaAlcance):

    def __init__(self, recursos=110, nombre='Mago', puntos_vida=100, ataque=110):
        super().__init__(recursos, nombre, puntos_vida, ataque)
        super().anadir_tropa()



   
print(Region.Regiones[(0,0)])
import random
class Batalla:
    @staticmethod
    def preparacion(xAtk,yAtk,xDef,yDef):

        tropas_atk=[]
        tropas_def =[]
        dic_tropas_atk=Region.Regiones[(xAtk,yAtk)]
        tropas_atk.append(
        print(dic_tropas_atk)
Batalla.preparacion(0,0,0,0)

     
















































        

























