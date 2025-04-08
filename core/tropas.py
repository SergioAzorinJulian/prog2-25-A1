



class Tropa():

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
    tropa_stats={}


    def __init__(self,recursos=int, nombre=str, puntos_vida=int, ataque_base=int, cantidad=int):
        self.nombre = nombre
        self.puntos_vida = puntos_vida
        self.ataque_base = ataque_base
        self.recursos = recursos
        self.cantidad = cantidad
        Tropa.anadir_tropa_stats(self)

    def atacar(self, aliado=tuple, enemigo=tuple):
        dano = self.ataque_base
        return dano


    def __str__(self):
        return f"{self.nombre} (Vida: {self.puntos_vida}, Ataque: {self.ataque_base}, Cantidad: {self.cantidad}"


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
        escudero=Escudero()
        hueste = Hueste()




class TropaAtaque(Tropa):
    '''
    Clase de la que heredarán las tropas de tipo "Ataque"
    '''
    def __init__(self, recursos=int, nombre=str, puntos_vida=int, ataque_base=int, cantidad=int):
        super().__init__(recursos, nombre, puntos_vida, ataque_base, cantidad)




class TropaDefensa(Tropa):
    '''
    Clase de la que heredarán las tropas de tipo "Defensa"
    '''

    def __init__(self, recursos=int, nombre=str, puntos_vida=int, ataque_base=int, cantidad=int):
        super().__init__(recursos, nombre, puntos_vida, ataque_base, cantidad)




class TropaAlcance(Tropa):
    '''
    Clase de la que heredarán las tropas de tipo "Alcance"
    '''

    def __init__(self, recursos=int, nombre=str, puntos_vida=int, ataque_base=int, cantidad=int):
        super().__init__(recursos, nombre, puntos_vida, ataque_base, cantidad)





# TROPAS DE ATAQUE
class Soldado(TropaAtaque):

    def __init__(self, recursos=50, nombre="soldado", puntos_vida=100, ataque_base=50, cantidad=1):
        super().__init__(recursos, nombre, puntos_vida, ataque_base, cantidad)
        Tropa.anadir_tropa_stats(self)

    def atacar(self,aliado=tuple,enemigo=tuple ):
        dano = self.ataque_base
        return dano




    ''' 
        .puntos_vida = dano
        """ 20% de probabilidad de golpe critico """
        if random.random() < 0.2:  """ --->   < 0.2 quiere decir que hay un 20% de probabilidad """
            dano *= 2
            print(f'Golpe critico de {self.nombre}!')
        enemigo.puntos_vida -= dano
        if enemigo.puntos_vida <= 0:
            enemigo.reducir_cantidad(1)
        return dano
    '''

class Caballero(TropaAtaque):

    def __init__(self, recursos=40, nombre="caballero", puntos_vida=80, ataque_base=70, cantidad=1):
        super().__init__(recursos, nombre, puntos_vida, ataque_base, cantidad)
        Tropa.anadir_tropa_stats(self)
    def atacar(self):
        dano = self.ataque_base
        return dano


class Hueste(TropaAtaque):

    def __init__(self, recursos=50, nombre="hueste", puntos_vida=50, ataque_base=50, cantidad=1):
        super().__init__(recursos, nombre, puntos_vida, ataque_base, cantidad)
        Tropa.anadir_tropa_stats(self)
    def atacar(self):
        dano = self.ataque_base
        return dano



# TROPAS DE DEFENSA
class Escudero(TropaDefensa):
    def __init__(self, recursos=50, nombre="escudero", puntos_vida=150, ataque_base=50, cantidad=1):
        super().__init__(recursos, nombre, puntos_vida, ataque_base, cantidad)
        Tropa.anadir_tropa_stats(self)
    def atacar(self):
        dano = self.ataque_base
        return dano


class Ogro(TropaDefensa):
    def __init__(self, recursos=80, nombre="ogro", puntos_vida=250, ataque_base=60, cantidad=1):
        super().__init__(recursos, nombre, puntos_vida, ataque_base, cantidad)
        Tropa.anadir_tropa_stats(self)
    def atacar(self):
        dano = self.ataque_base
        return dano



# TROPAS DE ALCANCE
class Arquero(TropaAlcance):
    def __init__(self, recursos=80, nombre="arquero", puntos_vida=50, ataque_base=150, cantidad=1):
        super().__init__(recursos, nombre, puntos_vida, ataque_base, cantidad)
        Tropa.anadir_tropa_stats(self)
    def atacar(self):
        dano = self.ataque_base
        return dano


class Ballestero(TropaAlcance):
    def __init__(self, recursos=100, nombre="ballestero", puntos_vida=300, ataque_base=70, cantidad=1):
        super().__init__(recursos, nombre, puntos_vida, ataque_base, cantidad)
        Tropa.anadir_tropa_stats(self)
    def atacar(self):
        dano = self.ataque_base
        return dano

class Mago(TropaAlcance):
    def __init__(self, recursos=110, nombre="mago", puntos_vida=100, ataque_base=110, cantidad=1):
        super().__init__(recursos, nombre, puntos_vida, ataque_base, cantidad)
        Tropa.anadir_tropa_stats(self)
    def atacar(self):
        dano = self.ataque_base
        return dano

Tropa.rellenar_tropa_stats()
print(Tropa.tropa_stats)