#TROPAS
from regionprueba import Region


class Tropa:
    tropa_stats = {}
    def __init__(self,recursos=int, nombre=str, puntos_vida=float, ataque=float):
        self.nombre = nombre
        self.puntos_vida = puntos_vida
        self.ataque = ataque
        self.recursos=recursos


    def anadir_tropa_stats(self):
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


# -----------------------------------------------
# CLASES INTERMEDIAS
# -----------------------------------------------

class TropaAtaque(Tropa):
    def __init__(self,recursos=int, nombre=str, puntos_vida=float, ataque=float):
        super().__init__(recursos,nombre, puntos_vida, ataque)





class TropaDefensa(Tropa):
    def __init__(self, recursos=int, nombre=str, puntos_vida=float, ataque=float):
        super().__init__(recursos, nombre, puntos_vida, ataque)





class TropaAlcance(Tropa):
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












Region.Regiones[(0,0)]=Region((0,0),'terreno',False)
Region.Regiones[(0,1)]=Region((0,1),'terreno',False)


Region.agregar_tropa(Region.Regiones[(0,0)],'ballestero',5)

Region.agregar_tropa(Region.Regiones[(0,0)],'caballero',5)

Region.agregar_tropa(Region.Regiones[(0,0)],'ogro',5)

Region.agregar_tropa(Region.Regiones[(0,1)],'ballestero',5)

Region.agregar_tropa(Region.Regiones[(0,1)],'caballero',5)

Region.agregar_tropa(Region.Regiones[(0,1)],'ogro',5)
import random
class Batalla:
    @staticmethod
    def preparacion_combate(posAtk:tuple,posDef:tuple):

        tropas_def =Region.Regiones[posDef]._tropas
        tropas_atk=Region.Regiones[posAtk]._tropas

        Ejercito_Atk = []
        Ejercito_Def = []

        for _ in range(0,len(tropas_def.keys())):
            Ejercito_Def.append([])

        for _ in range(0,len(tropas_atk.keys())):
            Ejercito_Atk.append([])

        for keys_tropasAtk in tropas_atk.keys():
            orden_random=random.randint(0,len(Ejercito_Atk)-1)

            while Ejercito_Atk[orden_random]!=[]:
                orden_random = random.randint(0, len(Ejercito_Atk)-1)

            Ejercito_Atk[orden_random].append(keys_tropasAtk)
            Ejercito_Atk[orden_random].append(tropas_atk[keys_tropasAtk])

        for keys_tropasDef in tropas_def.keys():
            orden_random = random.randint(0, len(Ejercito_Def) - 1)

            while Ejercito_Def[orden_random] != []:
                orden_random = random.randint(0, len(Ejercito_Def) - 1)

            Ejercito_Def[orden_random].append(keys_tropasDef)
            Ejercito_Def[orden_random].append(tropas_atk[keys_tropasDef])

        return Ejercito_Atk,Ejercito_Def


    @staticmethod
    def combate(Ejercito_Atk,Ejercito_Def):
        print(Ejercito_Atk)
        print(Ejercito_Def)
        Tropa.rellenar_tropa_stats()
        print(Tropa.tropa_stats)

        while Ejercito_Atk!=[] and Ejercito_Def!=[]:
            Ataque_Atk=Tropa.tropa_stats[Ejercito_Atk[0][0]]['ataque']*Ejercito_Atk[0][1]
            print(Ataque_Atk)
            Ataque_Def = Tropa.tropa_stats[Ejercito_Def[0][0]]['ataque'] * Ejercito_Def[0][1]
            print(Ataque_Def)
