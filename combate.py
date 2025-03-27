#TROPAS
from copy import deepcopy
##################################################################################################
class Region:
    Regiones={}
    def __init__(self, posicion: tuple[int, int], tipo_terreno: str, es_reino: bool = False, recursos_base: dict = None):
        self._posicion = posicion
        self._propietario: str = 'Neutral'
        self._tipo_terreno = tipo_terreno
        self._es_reino = es_reino
        self._recursos = recursos_base
        self._edificios: dict = {}
        self._tropas: dict = {}
        self._conexiones: list = []
        self._lugar_especial: str | None = None

    ### GETTERS ###
    def get_posicion(self):
        return deepcopy(self._posicion)

    def get_propietario(self):
        return self._propietario

    def get_tipo_terreno(self):
        return self._tipo_terreno

    def get_es_reino(self):
        return self._es_reino

    def get_recursos(self):
        return deepcopy(self._recursos)

    def get_edificios(self):
        return deepcopy(self._edificios)

    def get_tropas(self):
        return deepcopy(self._tropas)

    def get_conexiones(self):
        return deepcopy(self._conexiones)

    def get_lugar_especial(self):
        return self._lugar_especial


    ### SETTERS ###
    def set_posicion(self, nueva_posicion: tuple[int, int]):
        self._posicion = nueva_posicion

    def set_propietario(self, nuevo_propietario: str):
        self._propietario = nuevo_propietario

    def set_tipo_terreno(self, nuevo_tipo_terreno: str):
        self._tipo_terreno = nuevo_tipo_terreno

    def set_es_reino(self, nuevo_es_reino: bool):
        self._es_reino = nuevo_es_reino

    def set_recursos(self, nuevo_recursos: dict):
        self._recursos = nuevo_recursos

    def set_edificio(self, nuevo_edificios: dict):
        self._edificios = nuevo_edificios

    def set_tropas(self, nueva_tropas: dict):
        self._tropas = nueva_tropas

    def set_conexiones(self, nueva_conexiones: list):
        self._conexiones = nueva_conexiones

    def set_lugar_especial(self, nuevo_lugar: str):
        self._lugar_especial = nuevo_lugar


    ### METODOS PARA EDIFICIOS ###
    def construir_edificio(self, nombre: str, nivel: int = 1):
        """Añade un edificio o mejora su nivel."""
        if nombre in self._edificios:
            self._edificios[nombre] += 1
        else:
            self._edificios[nombre] = nivel

    def eliminar_edificio(self, nombre: str):
        if nombre in self._edificios:
            del self._edificios[nombre]

    ### METODOS PARA TROPAS ###
    def agregar_tropa(self, tipo: str, cantidad: int):
        if tipo in self._tropas:
            self._tropas[tipo] += cantidad
        else:
            self._tropas[tipo] = cantidad

    def eliminar_tropa(self, tipo: str, cantidad: int):
        if tipo in self._tropas:
            self._tropas[tipo] -= cantidad

            if self._tropas[tipo] <= 0:
                del self._tropas[tipo]


    ### METODO PARA MOSTRAR INFORMACION SOBRE LA REGION ###
    def __str__(self) -> str:
        return (f"Posición: {self._posicion} | Terreno: {self._tipo_terreno} | Reino: {self._es_reino} | "
                f"Propietario: {self._propietario} | "
                f"Recursos: {self._recursos} | "
                f"Edificios: {self._edificios} | Tropas: {self._tropas}")

region1 = Region((1, 2), 'bosque', recursos_base = {'oro': 100})

region1.construir_edificio('Horno', 2)
region1.agregar_tropa('mago', 2)
print(region1)
######################################################################################################################3


class Tropa:
    tropa_stats = {}
    def __init__(self,recursos=int, nombre=str, puntos_vida=float, ataque=float):
        self.nombre = nombre
        self.puntos_vida = puntos_vida
        self.ataque = ataque
        self.recursos=recursos


    def anadir_tropa_stats(self):
        Tropa.tropa_stats[self.nombre]=self


    @staticmethod
    def rellenar_tropa_stats():
        soldado = Soldado()
        caballero = Caballero()
        arquero = Arquero()
        ogro = Ogro()
        ballestero = Ballestero()
        mago = Mago()




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
        x=0
        while Ejercito_Atk!=[] and Ejercito_Def!=[]:


            Ataque_Atk = Tropa.tropa_stats[Ejercito_Atk[0][0]].ataque * Ejercito_Atk[0][1]
            print(Ataque_Atk)
            if isinstance(Tropa.tropa_stats[Ejercito_Atk[0][0]],TropaAtaque) and isinstance(Tropa.tropa_stats[Ejercito_Def[0][0]],TropaAlcance):
                Ataque_Atk+= (Ataque_Atk*0.2)//1
                print('Ataque vs Alcance',Ataque_Atk)

            elif isinstance(Tropa.tropa_stats[Ejercito_Atk[0][0]], TropaAlcance) and isinstance(Tropa.tropa_stats[Ejercito_Def[0][0]], TropaDefensa):
                Ataque_Atk += (Ataque_Atk * 0.1) // 1
                print('Alcance vs Defensa', Ataque_Atk)

            Ataque_Def = Tropa.tropa_stats[Ejercito_Def[0][0]].ataque * Ejercito_Def[0][1]
            print(Ataque_Def)
            if isinstance(Tropa.tropa_stats[Ejercito_Def[0][0]],TropaAtaque) and isinstance(Tropa.tropa_stats[Ejercito_Atk[0][0]],TropaAlcance):
                Ataque_Atk+= (Ataque_Atk*0.2)//1
                print('Ataque vs Alcance', Ataque_Def)

            elif isinstance(Tropa.tropa_stats[Ejercito_Def[0][0]], TropaAlcance) and isinstance(Tropa.tropa_stats[Ejercito_Atk[0][0]], TropaDefensa):
                Ataque_Atk += (Ataque_Atk * 0.1) // 1
                print('Alcance vs Defensa', Ataque_Def)


            Vida_Atk = Tropa.tropa_stats[Ejercito_Atk[0][0]].puntos_vida * Ejercito_Atk[0][1]
            print(Vida_Atk)
            if isinstance(Tropa.tropa_stats[Ejercito_Atk[0][0]],TropaDefensa) and isinstance(Tropa.tropa_stats[Ejercito_Def[0][0]],TropaAtaque):
                Vida_Atk+= (Vida_Atk*0.2)//1
                print('Defensa vs Ataque', Vida_Atk)

            elif isinstance(Tropa.tropa_stats[Ejercito_Atk[0][0]], TropaAlcance) and isinstance(Tropa.tropa_stats[Ejercito_Def[0][0]], TropaDefensa):
                Vida_Atk += (Vida_Atk * 0.1) // 1
                print('Alcance vs Defensa', Vida_Atk)

            Vida_Def = Tropa.tropa_stats[Ejercito_Def[0][0]].puntos_vida * Ejercito_Def[0][1]
            print(Vida_Def)
            if isinstance(Tropa.tropa_stats[Ejercito_Def[0][0]],TropaDefensa) and isinstance(Tropa.tropa_stats[Ejercito_Atk[0][0]],TropaAtaque):
                Vida_Def+= (Vida_Def*0.2)//1
                print('Defensa vs Ataque', Vida_Def)

            elif isinstance(Tropa.tropa_stats[Ejercito_Def[0][0]], TropaAlcance) and isinstance(Tropa.tropa_stats[Ejercito_Atk[0][0]], TropaDefensa):
                Vida_Def += (Vida_Def * 0.1) // 1
                print('Alcance vs Defensa', Vida_Def)

            while Vida_Atk > 0 or Vida_Def > 0:
                Vida_Atk-=Ataque_Def
                print(Vida_Atk)
                Vida_Def-=Ataque_Atk
                print(Vida_Def)
                if Vida_Atk <= 0:
                    print(Ejercito_Atk[0][0],'Ha sido derrotado (Atk)')
                    Ejercito_Atk.remove(Ejercito_Atk[0])
                    print(Ejercito_Atk)
                if Vida_Def <= 0:
                    print(Ejercito_Def[0][0], 'Ha sido derrotado (Def)')
                    Ejercito_Def.remove(Ejercito_Def[0])
                    print(Ejercito_Def)

            if Ejercito_Atk==[] and Ejercito_Def==[]:
                print('AMBOS EJERCITOS HAN MUERTO EN BATALLA')
                return 1
            elif Ejercito_Atk==[]:
                print('LA DEFENSA HA SIDO EFECTIVA')
                return 2
            elif Ejercito_Def==[]:
                print('LA ZONA HA SIDO CAPTURADA')
                return 3




Ejercito_Atk,Ejercito_Def=Batalla.preparacion_combate((0,0),(0,1))
Batalla.combate(Ejercito_Atk,Ejercito_Def)
