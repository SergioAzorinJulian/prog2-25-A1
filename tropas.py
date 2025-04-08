#from abc import ABC
from random import random

class Tropa:

    '''
    Clase base para todas las tropas.

    ATRIBUTOS:
    -------------
    total_tropas: int
        Contador global de todas las instancias de tropas creadas.
    nombre: str
        Nombre de la tropa.
    puntos_vida: float
        Vida actual de la tropa.
    ataque_base: float
        Daño base del ataque de la tropa.
    recursos: int
        Coste de recursos para entrenar la tropa.
    cantidad: int
        Número de instancias de esta tropa.

    METODOS:
    -----------
    reducir_cantidad(cantidad_perdida: int) -> None
        Reduce la cantidad de tropas y ajusta el contador global total_tropas.
    atacar(enemigo: Tropa) -> float
        Método base para atacar, sobrescrito por las subclases. Devuelve el daño infligido.
    recibir_daño(daño: float) -> None
        Método base para recibir daño, puede ser sobrescrito para defensas especiales.
    __str__() -> str
        Representación legible de la tropa (nombre, vida, ataque, cantidad).
    '''

    total_tropas = 0

    def __init__(self,recursos=int, nombre=str, puntos_vida=int, ataque_base=int, cantidad=int):
        self.nombre = nombre
        self.puntos_vida = puntos_vida
        self.ataque_base = ataque_base
        self.recursos = recursos
        self.cantidad = cantidad
        Tropa.total_tropas += self.cantidad

    def reducir_cantidad_tropas(self, cantidad_perdida):
        if cantidad_perdida >= self.cantidad:
            self.cantidad = 0
        else:
            self.cantidad -= cantidad_perdida
        Tropa.total_tropas -= cantidad_perdida

    def atacar(self, enemigo):
        pass

    def __str__(self):
        return f"{self.nombre} (Vida: {self.puntos_vida}, Ataque: {self.ataque_base}, Cantidad: {self.cantidad}"

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

    def atacar(self, enemigo= 'Tropa'):
        dano = self.ataque_base * 1.5   #MUltiplicador 1.5 por ser tropa de ataque
        enemigo.puntos_vida = dano
        if enemigo.puntos_vida <= 0:
            enemigo.reducir_cantidad(1)
        return dano



class TropaDefensa(Tropa):
    '''
    Clase de la que heredarán las tropas de tipo "Ataque"
    '''

    def ataque(self, enemigo = 'Tropa'):
        """ Ataque basico para las tropas de defensa y alcance """
        dano = self.ataque_base
        enemigo.puntos_vida -= dano
        if enemigo.puntos_vida <= 0:
            enemigo.reducir_cantidad(1)
        return dano



class TropaAlcance(Tropa):
    '''
    Clase de la que heredarán las tropas de tipo "Ataque"
    '''

    def ataque(self, enemigo = 'Tropa'):
        """ Ataque basico para las tropas de defensa y alcance """
        dano = self.ataque_base
        enemigo.puntos_vida -= dano
        if enemigo.puntos_vida <= 0:
            enemigo.reducir_cantidad(1)
        return dano

    def curar(self, aliado = 'Tropa'):
        """ Curacion basica, restaura 20 puntos de vida """
        curacion = 20
        if aliado.puntos_vida > 0:
            aliado.puntos_vida += curacion
            print(f'{self.nombre} cura a {aliado.nombre} con {curacion} puntos de vida.')
        else:
            print(f'{aliado.nombre} no puede ser curado, ya que no tiene vida.')
        return curacion



# TROPAS DE ATAQUE
class Soldado(TropaAtaque):

    def __init__(self, recursos=50, nombre="soldado", puntos_vida=100, ataque_base=50, cantidad=1):
        super().__init__(recursos, nombre, puntos_vida, ataque_base, cantidad)

    def atacar(self, enemigo = 'Tropa'):
        dano = self.ataque_base * 1.5
        enemigo.puntos_vida = dano
        """ 20% de probabilidad de golpe critico """
        if random.random() < 0.2:  """ --->   < 0.2 quiere decir que hay un 20% de probabilidad """
            dano *= 2
            print(f'Golpe critico de {self.nombre}!')
        enemigo.puntos_vida -= dano
        if enemigo.puntos_vida <= 0:
            enemigo.reducir_cantidad(1)
        return dano


class Caballero(TropaAtaque):

    def __init__(self, recursos=40, nombre="caballero", puntos_vida=80, ataque_base=70, cantidad=1):
        super().__init__(recursos, nombre, puntos_vida, ataque_base, cantidad)

    def atacar(self, enemigo= 'Tropa'):
        super().atacar()


class Hueste(TropaAtaque):

    def __init__(self, recursos=50, nombre="hueste", puntos_vida=50, ataque_base=50, cantidad=1):
        super().__init__(recursos, nombre, puntos_vida, ataque_base, cantidad)

    def atacar(self, enemigo= 'Tropa'):
        dano = self.ataque_base * 1.5
        enemigo.puntos_vida = dano
        """ Al atacar se cura un 10% """

        curacion = dano * 0.1
        self.puntos_vida += curacion
        print(f'{self.nombre} se cura {curacion} puntos de vida al atacar!')

        if enemigo.puntos_vida <= 0:
            enemigo.reducir_cantidad(1)
        return dano



# TROPAS DE DEFENSA
class Escudero(TropaDefensa):
    def __init__(self, recursos=50, nombre="escudero", puntos_vida=150, ataque_base=50, cantidad=1):
        super().__init__(recursos, nombre, puntos_vida, ataque_base, cantidad)


class Ogro(TropaDefensa):
    def __init__(self, recursos=80, nombre="ogro", puntos_vida=250, ataque_base=60, cantidad=1):
        super().__init__(recursos, nombre, puntos_vida, ataque_base, cantidad)

    def recibir_dano(self, dano):
        """ Defensa especial: reduce el daño recibido en un 20% """
        dano_reducido = dano * 0.8
        self.puntos_vida -= dano_reducido
        print(f"{self.nombre} reduce el daño recibido a {dano_reducido}!")
        if self.puntos_vida <= 0:
            self.reducir_cantidad(1)



# TROPAS DE ALCANCE
class Arquero(TropaAlcance):
    def __init__(self, recursos=80, nombre="arquero", puntos_vida=50, ataque_base=150, cantidad=1):
        super().__init__(recursos, nombre, puntos_vida, ataque_base, cantidad)

    def curar(self, aliado):
        """Curación mejorada: cura 30 puntos de vida."""
        curacion = 30
        aliado.puntos_vida += curacion
        print(f"{self.nombre} cura a {aliado.nombre} por {curacion} puntos de vida.")
        return curacion


class Ballestero(TropaAlcance):
    def __init__(self, recursos=100, nombre="ballestero", puntos_vida=300, ataque_base=70, cantidad=1):
        super().__init__(recursos, nombre, puntos_vida, ataque_base, cantidad)

    def curar(self, aliado):
        """Curación mejorada: cura 25 puntos de vida."""
        curacion = 25
        aliado.puntos_vida += curacion
        print(f"{self.nombre} cura a {aliado.nombre} por {curacion} puntos de vida.")
        return curacion

class Mago(TropaAlcance):
    def __init__(self, recursos=110, nombre="mago", puntos_vida=100, ataque_base=110, cantidad=1):
        super().__init__(recursos, nombre, puntos_vida, ataque_base, cantidad)

    def curar(self, aliado):
        """Curación especial: revive si el aliado está muerto, o cura normalmente."""
        if aliado.cantidad == 0:
            aliado.cantidad = 1
            aliado.puntos_vida = 50  # Vida inicial al revivir
            Tropa.total_tropas += 1
            print(f"{self.nombre} revive a {aliado.nombre} con 50 de vida!")
            return 50
        else:
            curacion = 20
            aliado.puntos_vida += curacion
            print(f"{self.nombre} cura a {aliado.nombre} por {curacion} puntos de vida.")
            return curacion

