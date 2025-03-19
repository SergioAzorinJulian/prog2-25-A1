#TROPAS

from abc import ABC, abstractmethod

class Tropa(ABC):
    def __init__(self, nombre: str, puntos_vida: float, ataque: float, defensa: float):
        self.nombre = nombre
        self.puntos_vida = puntos_vida
        self.ataque = ataque
        self.defensa = defensa

    @abstractmethod
    def atacar(self, objetivo: "Tropa"):
        print(f"{self.nombre} ataca a {objetivo.nombre}")
        dano = self.ataque - objetivo.defensa
        objetivo.recibir_dano(dano)

    @abstractmethod
    def recibir_dano(self, dano: float):
        self.puntos_vida -= dano
        print(f"{self.nombre} fue atacado y recibe {dano} de daño. Vida restante: {self.puntos_vida}")
        if self.puntos_vida <= 0:
            print(f"{self.nombre} ha sido derrotado.")


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

    def recibir_dano(self, dano: float):
        super().recibir_dano(dano)

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

    def recibir_dano(self, dano: float):
        super().recibir_dano(dano)

    def curar(self, aliado : "Tropa"):
        if aliado.puntos_vida > 0:
            aliado.puntos_vida += self.curaciones
            print(f"{self.nombre} cura a {aliado.nombre} con {self.curaciones} puntos de vida.")
        else:
            print(f"{aliado.nombre} fue derrotado y no puede ser curado.")

# -----------------------------------------------
# CLASES ESPECIFICAS DE TROPAS
# -----------------------------------------------

# TROPAS DE ATAQUE
class Soldado(TropaAtaque):
    def __init__(self):
        super().__init__("Soldado", puntos_vida=100.00, ataque=10.00, defensa=5.00, bono_ataque=3.00)


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


# TROPAS DE CURACION
class Mago(TropaApoyo):
    def __init__(self):
        super().__init__("Mago", puntos_vida=50.00, ataque=8.00, defensa=4.00, curaciones=20.00)