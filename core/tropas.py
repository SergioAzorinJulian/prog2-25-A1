# from abc import ABC
import random
import math


# from __future__ import annotations
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

    def __init__(self, recursos: int, nombre: str, cantidad: int):
        self.recursos = recursos
        self.nombre = nombre
        self.cantidad = cantidad
        self.dmg = self.__class__.dmg_base * self.cantidad
        self.vida = self.__class__.vida_base * self.cantidad

    def actualizar_cantidad(self, aliado):
        ratio = math.ceil(self.vida / self.__class__.vida_base)  # Redondeo hacia arriba la cantidad
        self.cantidad = ratio
        if self.cantidad < 0:
            self.cantidad = 0
        if self.cantidad == 0:
            for i in aliado:
                if i.nombre == self.nombre:
                    aliado.remove(i)
                    break

    def atacar(self, aliado: list, enemigo: list) -> str:
        """ Ataque basico para las tropas """
        if enemigo != []:
            n = random.randint(0, len(enemigo) - 1)  # Elegimos una tropa al azar de la lista
            nombre = enemigo[n].nombre
            enemigo[n].recibir_dmg(self.dmg, aliado)
            return f'{self.nombre} ataca a {nombre} : {self.dmg}'

    def recibir_dmg(self, dmg, aliado):
        self.vida = self.vida - dmg
        self.actualizar_cantidad(aliado)

    def __iadd__(self, other):
        if isinstance(other, Tropa):
            self.cantidad += other.cantidad
        else:
            self.cantidad += other
        return self

    def __isub__(self, other):
        self.cantidad -= other
        return self

    def __str__(self):
        return f"{self.nombre}: Daño: {self.__class__.dmg_base}, Vida: {self.__class__.vida_base}, Cantidad: {self.cantidad}"

    def __repr__(self):
        return \
            (f'Tropa \nNombre: {self.nombre} Cantidad: {self.cantidad}')


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

    def atacar(self, aliado: list[Tropa], enemigo: list[Tropa]) -> str:
        if enemigo != []:
            critico = self.critico()
            n = random.randint(0, len(enemigo) - 1)  # Elegimos una tropa al azar de la lista
            nombre = enemigo[n].nombre
            if critico[0]:
                dmg = self.dmg * critico[1]
                enemigo[n].recibir_dmg(dmg, enemigo)
                return critico[2], f'{self.nombre} ataca a {nombre} : {dmg}'
            else:
                enemigo[n].recibir_dmg(self.dmg, enemigo)
                return f'{self.nombre} ataca a {nombre} : {self.dmg}'


class TropaDefensa(Tropa):
    '''
    Clase de la que heredarán las tropas de tipo "Defensa"
    '''

    def recibir_dmg(self, dmg, aliado, reducion=5):
        print('hla')
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
    vida_base = 10

    def __init__(self, cantidad, recursos=50, nombre='Soldado'):
        super().__init__(recursos, nombre, cantidad)


# TROPAS DE DEFENSA
class Gigante(TropaDefensa):
    dmg_base = 100
    vida_base = 500

    def __init__(self, cantidad, recursos=50, nombre='Gigante'):
        super().__init__(recursos, nombre, cantidad)

    def atacar(self, aliado: list[Tropa], enemigo: list[Tropa]):  # Solo ataca estructuras
        if enemigo != []:
            for i in enemigo:
                if isinstance(i, TropaEstructura):
                    i.recibir_dmg(self.dmg, enemigo)


# TROPAS DE ALCANCE
class Arquero(TropaAlcance):
    '''
    Arquero: ''Dispara varias flechas''
    '''
    dmg_base = 80
    vida_base = 150

    def __init__(self, cantidad, recursos=50, nombre='Arquero'):
        super().__init__(recursos, nombre, cantidad)

    def atacar(self, aliado: list[Tropa], enemigo: list[Tropa]):
        if enemigo != []:
            n = 0
            for i in enemigo:
                if random.random() < 0.8:  # < 80% de probabilidad
                    i.recibir_dmg(self.dmg, enemigo)
                    n += 1
            return f'{self.nombre} acertó {n} veces : {self.dmg * n}'
        else:
            return None


# TROPAS DE ESTRUCTURA
class Canon(TropaEstructura):
    '''
    Cañon: ''Daño en area'' -> Ataca cada 2 Turnos (De combate)
    '''
    dmg_base = 300
    vida_base = 500

    def __init__(self, cantidad, recursos=100, nombre='Cañon'):
        super().__init__(recursos, nombre, cantidad)
        self.activo = True

    def toggle(self) -> bool:  # Activa y desactiva el cañon
        estado = self.activo
        self.activo = not self.activo
        return estado

    def atacar(self, aliado: list[Tropa], enemigo: list[Tropa]):

        if enemigo != []:
            dmg_total = 0
            reduccion = 1.0
            if self.toggle():
                print('ATACA')
                for i in enemigo:
                    if reduccion > 0:
                        i.recibir_dmg(self.dmg * reduccion, enemigo)
                        dmg_total += self.dmg * reduccion
                        reduccion -= 0.4

                return f'{self.nombre} dispara : {dmg_total}'
            else:
                return f'{self.nombre} sobrecalentado'
        else:
            return None
