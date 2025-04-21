# from abc import ABC
import random
import math

from recursos import Recurso


# from __future__ import annotations
class Tropa:
    """
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

    atacar: metodo que hace daño al enemigo (puedes ser diferente para algunas tropas

    recibir_dmg: metodo donde ser recibie el daño
    """

    def __init__(self, recursos: int, nombre: str, cantidad: int):
        self.recursos = recursos
        self.nombre = nombre
        self.cantidad = cantidad
        self.dmg = self.__class__.dmg_base * self.cantidad
        self.vida = self.__class__.vida_base * self.cantidad

    def actualizar_cantidad(self, aliado):
        ratio = math.ceil(self.vida / self.__class__.vida_base)  # Redondeo hacia arriba la cantidad
        self.cantidad = ratio
        self.dmg=self.__class__.dmg_base*self.cantidad
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
    

    def __eq__(self, other):
        if isinstance(other, Tropa):
            return self.nombre == other.nombre
        return False

    def __sub__(self, other):
        """Devuelve una nueva instancia de Tropa con la cantidad restada."""
        nueva_cantidad = self.cantidad
        if isinstance(other, Tropa): # Es una Tropa
            nueva_cantidad -= other.cantidad
        else: # Es un entero
            nueva_cantidad -= other

        return self.__class__(self.recursos, self.nombre, nueva_cantidad)


    def __add__(self, other):
        """Devuelve una nueva instancia de Tropa con la cantidad sumada."""
        nueva_cantidad = self.cantidad
        if isinstance(other, Tropa): # Es una Tropa
            nueva_cantidad += other.cantidad
        else: # Es un entero
            nueva_cantidad += other

        return self.__class__(self.recursos, self.nombre, nueva_cantidad)
    
    def __eq__(self, other):
        if isinstance(other, Tropa):
            return self.nombre == other.nombre
        return False
    
    def __str__(self):
        return f"{self.nombre}: Daño: {self.__class__.dmg_base}, Vida: {self.__class__.vida_base}, Cantidad: {self.cantidad}"

    def __repr__(self):
        return \
            (f'Tropa \nNombre: {self.nombre} Cantidad: {self.cantidad}')

    def __sub__(self, other):
        """Devuelve una nueva instancia de Tropa con la cantidad restada."""
        nueva_cantidad = self.cantidad
        if isinstance(other, Tropa): # Es una Tropa
            nueva_cantidad -= other.cantidad
        else: # Es un entero
            nueva_cantidad -= other

        return self.__class__(self.recursos, self.nombre, nueva_cantidad)


    def __add__(self, other):
        """Devuelve una nueva instancia de Tropa con la cantidad sumada."""
        nueva_cantidad = self.cantidad
        if isinstance(other, Tropa): # Es una Tropa
            nueva_cantidad += other.cantidad
        else: # Es un entero
            nueva_cantidad += other

        return self.__class__(self.recursos, self.nombre, nueva_cantidad)


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
    dmg_base = 100  #Daño de la tropa
    vida_base = 150  #Vida de la tropa
    recursos = Recurso('caza',10,0, 150)  #Recursos que cuesta entrenarla
    dmg_base = 100
    vida_base = 1
    recursos = Recurso('caza',10,0)
    def __init__(self, cantidad=0, recursos=50, nombre='Soldado'):
        super().__init__(recursos, nombre, cantidad)


# TROPAS DE DEFENSA
class Gigante(TropaDefensa):
    dmg_base = 100
    vida_base = 250
    recursos = Recurso('caza', 20, 0, 150)
    vida_base = 10
    recursos = Recurso('caza', 20, 0)
    def __init__(self, cantidad=0, recursos=50, nombre='Gigante'):
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
    recursos = Recurso('caza', 5, 0, 150)
    recursos = Recurso('caza', 5, 0)
    def __init__(self, cantidad=0, recursos=50, nombre='Arquero'):
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
            return ''


# TROPAS DE ESTRUCTURA
class Canon(TropaEstructura):
    '''
    Cañon: ''Daño en area'' -> Ataca cada 2 Turnos (De combate)
    '''
    dmg_base = 300
    vida_base = 500
    recursos = Recurso('madera', 10, 0, 150)
    recursos = Recurso('madera', 10, 0)
    def __init__(self, cantidad=0, recursos=100, nombre='Cañon'):
        super().__init__(recursos, nombre, cantidad)
        self.activo = True

    def toggle(self) -> bool:  # Activa y desactiva el cañon
        estado = self.activo
        self.activo = not self.activo
        return estado

    def atacar(self, aliado: list[Tropa], enemigo: list[Tropa]):

        if enemigo != []:
            dmg_total = 0
            reduccion = 1
            if self.toggle():
                for i in enemigo[:]: #Copia de la lista para no alterar el orden
                    if reduccion > 0:
                        i.recibir_dmg(self.dmg * reduccion, enemigo)
                        dmg_total += self.dmg * reduccion
                        reduccion -= 0.4
                return f'{self.nombre} dispara : {dmg_total}'
            else:
                return f'{self.nombre} sobrecalentado'
        else:
            return ''


