
# from abc import ABC
from random import random
import math
#from __future__ import annotations
class Tropa:

    '''
    Clase base para todas las tropas.

    ATRIBUTOS:
    -------------
    recursos: int
        Coste de recursos para entrenar la tropa.
    nombre: str
        Nombre de la tropa.
    cantidad: int
        Número de instancias de esta tropa.

    METODOS:
    -----------

    '''

    def __init__(self ,recursos :int, nombre :str, cantidad :int):
        self.recursos = recursos
        self.nombre = nombre
        self.cantidad = cantidad
        self.dmg = self.__class__.dmg_base * self.cantidad
        self.vida = self.__class__.vida_base * self.cantidad

    def actualizar_cantidad(self,aliado):
        ratio = math.ceil(self.vida / self.__class__.vida_base) # Redondeo hacia arriba la cantidad
        self.cantidad = ratio
        if self.cantidad <= 0:
            aliado.drop(self)

    def atacar(self,aliado: list, enemigo : list) -> str:
        """ Ataque basico para las tropas """
        n = random.randint(0 ,len(enemigo)) # Elegimos una tropa al azar de la lista
        enemigo[n].recibir_dmg(self.dmg)
        return f'{self.nombre} ataca a {enemigo[n].nombre} : {self.dmg}'

    def recibir_dmg(self ,dmg,aliado):
        self.vida = self.vida - dmg
        self.actualizar_cantidad(aliado)

    def __iadd__(self ,other):
        if isinstance(other ,Tropa):
            self.cantidad += other.cantidad
        else:
            self.cantidad += other
        return self

    def __isub__(self ,other):
        self.cantidad -= other
        return self

    def __str__(self):
        return f"{self.nombre}: Daño: {self.__class__.dmg_base}, Vida: {self.__class__.vida_base}, Cantidad: {self.cantidad}"

    def __repr__(self):
        return \
            (f'Tropa \nNombre: {self.nombre}\n Daño: {self.__class__.dmg_base}, Vida: {self.__class__.vida_base}, Cantidad: {self.cantidad}')

    """
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
    """


class TropaAtaque(Tropa):
    '''
    Clase de la que heredarán las tropas de tipo "Ataque"
    '''

    def critico(self) -> tuple:
        """ Probabilidad de golpe critico """
        if self.vida < self.__class__.vida_base:
            if random.random() < 0.8:  # < 80% de probabilidad
                return True, 2, f'{self.nombre} : Golpe crítico \n'
        else:
            if random.random() < 0.2:  # < 20% de probabilidad
                return True, 2, f'{self.nombre} : Golpe crítico \n'
        return False, 1

    def atacar(self,aliado: list[Tropa], enemigo: list[Tropa]) -> str:
        critico = self.critico()
        n = random.randint(0, len(enemigo))  # Elegimos una tropa al azar de la lista
        if critico[0]:
            dmg = self.dmg * critico[1]
            enemigo[n].recibir_dmg(dmg)
            return critico[2], f'{self.nombre} ataca a {enemigo[n].nombre} : {dmg}'
        else:
            enemigo[n].recibir_dmg(self.dmg)
            return f'{self.nombre} ataca a {enemigo[n].nombre} : {self.dmg}'


class TropaDefensa(Tropa):
    '''
    Clase de la que heredarán las tropas de tipo "Defensa"
    '''

    def recibir_dmg(self, dmg,aliado, reducion=0.8):
        dmg_reducido = dmg * reducion
        self.vida = self.vida - dmg_reducido
        self.actualizar_cantidad(aliado)


class TropaAlcance(Tropa):
    '''
    Clase de la que heredarán las tropas de tipo "Alcance"
    '''


class TropaEstructura(Tropa):
    '''
    Clase de la que heredarán las tropas de tipo "Inmóviles"
    '''


# TROPAS DE ATAQUE
class Soldado(TropaAtaque):
    '''
    Soldado: Clase Default de Tropa de Atk
    '''
    dmg_base = 100
    vida_base = 300

    def __init__(self, cantidad, recursos=50, nombre='Soldado'):
        super().__init__(recursos, nombre, cantidad)


# TROPAS DE DEFENSA
class Gigante(TropaDefensa):
    dmg_base = 100
    vida_base = 500

    def __init__(self, cantidad, recursos=50, nombre='Gigante'):
        super().__init__(recursos, nombre, cantidad)

    def atacar(self,aliado: list[Tropa] ,enemigo: list[Tropa]):  # Solo ataca estructuras
        for i in enemigo:
            if isinstance(i, TropaEstructura):
                i.recibir_dmg(self.dmg)


# TROPAS DE ALCANCE
class Arquero(TropaAlcance):
    '''
    Arquero: ''Dispara varias flechas''
    '''
    dmg_base = 80
    vida_base = 150

    def __init__(self, cantidad, recursos=50, nombre='Arquero'):
        super().__init__(recursos, nombre, cantidad)

    def atacar(self,aliado: list[Tropa], enemigo: list[Tropa]):
        n = 0
        for i in enemigo:
            if random.random() < 0.8:  # < 80% de probabilidad
                i.recibir_dmg(self.dmg)
                n += 1
        return f'{self.nombre} acertó {n} veces : {self.dmg * n}'


# TROPAS DE ESTRUCTURA
class Canon(TropaEstructura):
    '''
    Cañon: ''Daño en area'' -> Ataca cada 2 Turnos (De combate)
    '''
    dmg_base = 200
    vida_base = 400

    def __init__(self, cantidad, recursos=100, nombre='Cañon'):
        super().__init__(recursos, nombre, cantidad)
        self.activo = True

    def toggle(self) -> bool:  # Activa y desactiva el cañon
        estado = self.activo
        self.activo = not self.activo
        return estado

    def atacar(self,aliado: list[Tropa],enemigo: list[Tropa]):
        dmg_total = 0
        reduccion = 1.0
        if self.toggle():
            for i in enemigo:
                if reduccion > 0:
                    i.recibir_dmg(self.dmg * reduccion)
                    dmg_total += self.dmg * reduccion
                    reduccion -= 0.4

            return f'{self.nombre} dispara : {dmg_total}'
        else:
            return f'{self.nombre} sobrecalentado'
