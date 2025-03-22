#TROPAS



class Tropa:
    tropas={}
    def __init__(self, x:int,y:int,numero:int, recursos=int, nombre=str, puntos_vida=float, ataque=float):
        self.x = x
        self.y = y
        self.nombre = nombre
        self.puntos_vida = puntos_vida
        self.ataque = ataque
        self.numero=numero
        self.recursos=recursos

    def anadir_tropa(self):
        if self.x!=-1 and self.y!=-1:
            if f'{self.x}{self.y}' not in Tropa.tropas.keys():
                Tropa.tropas[f'{self.x}{self.y}']=[]

            Tropa.tropas[f'{self.x}{self.y}'].append([self.nombre,self.numero])


# -----------------------------------------------
# CLASES INTERMEDIAS
# -----------------------------------------------

class TropaAtaque(Tropa):
    def __init__(self, x:int,y:int,numero:int, recursos=int, nombre=str, puntos_vida=float, ataque=float):
        super().__init__(x,y,numero, recursos,nombre, puntos_vida, ataque)





class TropaDefensa(Tropa):
    def __init__(self, x:int,y:int,numero:int, recursos=int, nombre=str, puntos_vida=float, ataque=float):
        super().__init__(x,y,numero, recursos, nombre, puntos_vida, ataque)





class TropaAlcance(Tropa):
    def __init__(self, x:int,y:int,numero:int, recursos=int, nombre=str, puntos_vida=float, ataque=float):
        super().__init__(x,y,numero, recursos, nombre, puntos_vida, ataque)


# TROPAS DE ATAQUE
class Soldado(TropaAtaque):

    def __init__(self,x:int,y:int, numero: int, recursos=50, nombre='Soldado', puntos_vida=100, ataque=100):
        super().__init__(x,y,numero, recursos, nombre, puntos_vida, ataque)
        super().anadir_tropa()

class Caballero(TropaAtaque):

    def __init__(self,x:int,y:int, numero: int, recursos= 70, nombre='Caballero', puntos_vida=200, ataque=85):
        super().__init__(x,y,numero, recursos, nombre, puntos_vida, ataque)
        super().anadir_tropa()
# TROPAS DE DEFENSA
class Ogro(TropaDefensa):

    def __init__(self,x:int,y:int, numero: int, recursos=80, nombre='Ogro', puntos_vida=250, ataque=60):
        super().__init__(x,y,numero, recursos, nombre, puntos_vida, ataque)
        super().anadir_tropa()
# TROPAS DE ALCANCE
class Arquero(TropaAlcance):

    def __init__(self, x:int,y:int,numero: int, recursos=80, nombre='Arquero', puntos_vida=50, ataque=150):
        super().__init__(x,y,numero, recursos, nombre, puntos_vida, ataque)
        super().anadir_tropa()


class Ballestero(TropaAlcance):

    def __init__(self,x:int,y:int, numero: int, recursos=100, nombre='Ballestero', puntos_vida=300, ataque=70):
        super().__init__(x,y,numero, recursos, nombre, puntos_vida, ataque)
        super().anadir_tropa()

# TROPAS DE CURACION
class Mago(TropaAlcance):

    def __init__(self, x:int,y:int,numero: int, recursos=110, nombre='Mago', puntos_vida=100, ataque=110):
        super().__init__(x,y,numero, recursos, nombre, puntos_vida, ataque)
        super().anadir_tropa()




soldado=Soldado(-1,-1,0)
caballero=Caballero(-1,-1,0)
arquero=Arquero(-1,-1,0)
ogro=Ogro(-1,-1,0)
ballestero=Ballestero(-1,-1,0)
mago=Mago(-1,-1,0)

tropas_stats={'Soldado':soldado,'Caballero':caballero,
              'Arquero':arquero,'Ogro':ogro,'Mago':mago}




Var=Mago(0,0,5)
Var=Mago(0,1,4)
Var=Caballero(0,0,4)
Var=Caballero(0,1,3)
#Var=Ballestero(0,0,3)
Var=Ballestero(0,1,2)

print(Tropa.tropas)     #PODEIS OBSERVAR QUE SE HAN AÑADIDO LAS TROPAS DE CADA POSICIÓN AL DICCIONARIO

import random
class Batalla:
    @staticmethod
    def preparacion(xa,ya,xb,yb):

        tropas_atk=[]
        tropas_def =[]

        while len(tropas_atk)!=len(Tropa.tropas[f'{xa}{ya}']):

            tropa_random_atk=random.randint(0,len(Tropa.tropas[f'{xa}{ya}'])-1)
            if Tropa.tropas[f'{xa}{ya}'][tropa_random_atk] not in tropas_atk:
                tropas_atk.append(Tropa.tropas[f'{xa}{ya}'][tropa_random_atk])
                print(tropas_atk)

        while len(tropas_def)!=len(Tropa.tropas[f'{xb}{yb}']):

            tropa_random_def = random.randint(0,len(Tropa.tropas[f'{xb}{yb}'])-1)
            if Tropa.tropas[f'{xb}{yb}'][tropa_random_def] not in tropas_def:
                tropas_def.append(Tropa.tropas[f'{xb}{yb}'][tropa_random_def])
                print(tropas_def)
        print(tropas_atk, tropas_def)
        return tropas_atk, tropas_def


    @staticmethod
    def combate(tropas_atk,tropas_def):
        fila1_atk=[tropas_atk[0]]
        try:
            fila2_atk=[tropas_atk[1]]
        except IndexError:
            fila2_atk=[]
        try:
            fila3_atk=[tropas_atk[2]]
        except IndexError:
            fila3_atk=[]

        fila1_def = [tropas_def[0]]
        try:
            fila2_def= [tropas_def[1]]
        except IndexError:
            fila2_def = []
        try:
            fila3_def = [tropas_def[2]]
        except IndexError:
            fila3_def = []
        print(fila1_atk, fila2_atk, fila3_atk)
        print(fila1_def, fila2_def, fila3_def)
    











tropas_atk,tropas_def= Batalla.preparacion(0,0,0,1)
Batalla.combate(tropas_atk,tropas_def)









        

























