
import random
import math

#from recursos import Recurso


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
    actualizar_cantidad: Sirve para actualizar el número de tropas dentro de combate despues de recibir daño

    atacar: metodo que hace daño al enemigo (puedes ser diferente para algunas tropas

    recibir_dmg: metodo donde ser recibie el daño
    '''

    def __init__(self, recursos: int, nombre: str, cantidad: int):
        self.recursos = recursos
        self.nombre = nombre
        self.cantidad = cantidad
        self.dmg = self.__class__.dmg_base * self.cantidad   #El daño es el producto de la cantidad de tropas por el daño de cada una
        self.vida = self.__class__.vida_base * self.cantidad  #La vida es el producto de la cantidad de tropas por la vida de cada una

    def actualizar_cantidad(self, aliado):
        ratio = math.ceil(self.vida / self.__class__.vida_base)  # Redondeo hacia arriba la cantidad
        self.cantidad = ratio
        if self.cantidad < 0:   #Si la cantidad de tropas es < 0, asignamos a la cantidad = 0
            self.cantidad = 0
        if self.cantidad == 0:   #Si la cantidad es = 0, quitamos a la tropa de la lista en el combate
            for i in aliado:
                if i.nombre == self.nombre:
                    aliado.remove(i)
                    break

    def atacar(self, aliado: list, enemigo: list) -> str:
        """ Ataque basico para las tropas """
        if enemigo != []:
            n = random.randint(0, len(enemigo) - 1)  # Elegimos una tropa al azar de la lista
            nombre = enemigo[n].nombre   #Cogemos el nombre de la tropa que ataca
            enemigo[n].recibir_dmg(self.dmg, aliado)   #Hacemos que la tropa enemiga tome daño
            return f'{self.nombre} ataca a {nombre} : {self.dmg}'

    def recibir_dmg(self, dmg, aliado):
        self.vida = self.vida - dmg  #A la vida se le resta el daño del agresor
        self.actualizar_cantidad(aliado)     #Llamamo a actualizar_cantidad por si a muerto alguien del grupo de tropas

    def __iadd__(self, other):  #Metodo para añadir tropas
        if isinstance(other, Tropa):
            self.cantidad += other.cantidad
        else:
            self.cantidad += other
        return self

    def __isub__(self, other):  #Metodo para restar tropas
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

    METODOS:
    ----------
    critico: las clases de tipo "Ataque" tienen posibilidad de asentar un golpe crítico, este metodo calcula si esto ocurre

    atacar: metodo atacar modificado para las tropas de tipo ataque (
    '''

    def critico(self) -> tuple:
        """ Probabilidad de golpe critico """
        if self.vida < self.__class__.vida_base: #Para aplicar un bonus de probabilidad, calculamos si queda más de una tropa de ataque
            if random.random() < 0.8:  # < 80% de probabilidad (el critico es más probable si solo queda una tropa de ataque)
                return True, 2, f'{self.nombre} : Golpe crítico \n'
        else:
            if random.random() < 0.2:  # < 20% de probabilidad (probabilidad base de hacer critico)
                return True, 2, f'{self.nombre} : Golpe crítico \n'
        return False, 1

    def atacar(self, aliado: list[Tropa], enemigo: list[Tropa]) -> str:
        """atrobitps
        --------------
        aliado: lista con el resto de las tropas que forman parte de su ejercito

        enemigo: lista con las tropas enemigas
        """
        if enemigo != []:
            critico = self.critico()    #Guardamos lo que nos devuelve critico()
            n = random.randint(0, len(enemigo) - 1)  # Elegimos una tropa al azar de la lista
            nombre = enemigo[n].nombre
            if critico[0]:
                dmg = self.dmg * critico[1]   #Al daño se le añade el critico
                enemigo[n].recibir_dmg(dmg, enemigo)    #Enemigo recibe daño
                return  f'{self.nombre} ataca a {nombre} : {dmg}'
            else:
                enemigo[n].recibir_dmg(self.dmg, enemigo)  #Enemigo recibe daño base (no se ha realizado golpe critico)
                return f'{self.nombre} ataca a {nombre} : {self.dmg}'


class TropaDefensa(Tropa):
    '''
    Clase de la que heredarán las tropas de tipo "Defensa"

    METODOS:
    ---------
    recibir_dmg: metodo que reduce el daño recibido de las tropas de tipo defensa
    '''

    def recibir_dmg(self, dmg, aliado, reducion=5):
        '''Metodo donde las tropas de defensa reciben menos daño'''
        dmg_reducido = dmg * reducion
        self.vida = self.vida - dmg_reducido
        self.actualizar_cantidad(aliado)
        return ' Gigante: Se ha reducido el daño recibido'


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
  #  recursos = Recurso('caza',10,0)  #Recursos que cuesta entrenarla
    def __init__(self, cantidad, recursos=50, nombre='Soldado'):
        super().__init__(recursos, nombre, cantidad)

    def __str__(self):
        return Tropa.__str__(self) + ' Efecto especial: Puede hacer daño extra si tienes suerte'


# TROPAS DE DEFENSA
class Gigante(TropaDefensa):
    dmg_base = 100
    vida_base = 250
   # recursos = Recurso('caza', 20, 0)
    def __init__(self, cantidad, recursos=50, nombre='Gigante'):
        super().__init__(recursos, nombre, cantidad)
    def __str__(self):

        return Tropa.__str__(self)+' Efecto especial: Solo ataca estructuras'



    def atacar(self, aliado: list[Tropa], enemigo: list[Tropa]):  # Solo ataca estructuras
        n=0
        if enemigo != []:
            for i in enemigo:  #Detectamos la estructura en el ejercito enemigo, sino no hace daño

                if isinstance(i, TropaEstructura):
                    n += 1
                    i.recibir_dmg(self.dmg, enemigo) #Golpeamos la estructura
                    return f'{self.nombre} golpeó {n} veces : {self.dmg * n}'

# TROPAS DE ALCANCE
class Arquero(TropaAlcance):
    '''
    Arquero: ''Dispara varias flechas''

    METODOS
    .........
    atacar: metodo de ataque unico de la tropa arquero, ataca a todos los enemigos (si tienes suerte)
    '''
    dmg_base = 80
    vida_base = 150
   # recursos = Recurso('caza', 5, 0)
    def __init__(self, cantidad, recursos=50, nombre='Arquero'):
        super().__init__(recursos, nombre, cantidad)

    def __str__(self):

        return Tropa.__str__(self) + ' Efecto especial: Lanza una flecha a cada enemigo'


    def atacar(self, aliado: list[Tropa], enemigo: list[Tropa]):
        if enemigo != []:
            n = 0 #Número de veces que ataca (inicializado a 0)
            for i in enemigo:  #Para cada enemigo
                if random.random() < 0.5:  # < 50% de probabilidad
                    i.recibir_dmg(self.dmg, enemigo)  #Si tienes suerte, aciertas el disparo e inflinge daño
                    n += 1  #Incrementamos el número de aciertos
            return f'{self.nombre} acertó {n} veces : {self.dmg * n}'



# TROPAS DE ESTRUCTURA
class Canon(TropaEstructura):
    '''
    Cañon: ''Daño en area'' -> Ataca cada 2 Turnos (De combate)

    METODOS
    ---------
    toggle: decide si el cañon ataca (1 turno hace daño, el siguiente recarga)

    atacar: atacar único del cañón, hace daño a las tropas cercanas al frente de batalla (disminuyendo su
            daño a las tropas más lejanas) pero descansa 1 turno
    '''
    dmg_base = 300
    vida_base = 500
   # recursos = Recurso('madera', 10, 0)
    def __init__(self, cantidad, recursos=100, nombre='Cañon'):
        super().__init__(recursos, nombre, cantidad)
        self.activo = True  #Inicializamos el valor que nos dice si el cañon está listo

    def toggle(self) -> bool:  # Activa y desactiva el cañon
        estado = self.activo   #Cogemos el valor de self.activo (bool)
        self.activo = not self.activo  #Invertimos su valor para la siguiente interacción
        return estado   #Devolvemos el valor cogido

    def atacar(self, aliado: list[Tropa], enemigo: list[Tropa]):

        if enemigo != []:
            dmg_total = 0
            reduccion = 1  #Reducción del daño, aplicada a las tropas lejanas al impacto
            if self.toggle(): #Si está activo...
                for i in enemigo[:]: #Copia de la lista para no alterar el orden
                    if reduccion > 0:  #Si la recucción sigue existiendo
                        dmg_total += self.dmg * reduccion
                        i.recibir_dmg(self.dmg * reduccion, enemigo) #causa el daño por la disminución
                        reduccion -= 0.4
                return f'{self.nombre} dispara : {dmg_total}'
            else:
                return f'{self.nombre} sobrecalentado'

        return f'Cañon: No quedan tropas para atacar'

    def __str__(self):

        return Tropa.__str__(self) + ' Efecto especial: Ataca en area, pero debe recargar entre disparos'

