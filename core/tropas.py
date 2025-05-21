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
        '''
        Actualiza la cantidad de la tropa

        Parametros:
        -------
        aliado: Lista con las tropas de su mismo ejercito

        Returns:
        ------
        str
            tropas que han muerto
        '''
        ratio = math.ceil(self.vida / self.__class__.vida_base)  # Redondeo hacia arriba la cantidad
        self.cantidad = ratio
        self.dmg=self.__class__.dmg_base*self.cantidad
        if self.cantidad == 0:
            for i in aliado:
                if i.nombre == self.nombre:
                    aliado.remove(i)
                    break
            return f'Las tropas {self.nombre} murieron'
        return f'{self.nombre}: {self.cantidad}'

    def atacar(self, aliado: list, enemigo: list) -> str:
        '''
        Hace daño al enemigo

        Parametros:
        -------
        aliado: Lista con las tropas de su mismo ejercito
        enemigo: Lista con las tropas del otro ejercito

        Returns:
        ------
        str
            mensaje de daño realizado
        '''
        if enemigo != []:
            n = random.randint(0, len(enemigo) - 1)  # Elegimos una tropa al azar de la lista
            nombre = enemigo[n].nombre
            txt_cantidad = enemigo[n].recibir_dmg(self.dmg, aliado)
            return f'{self.nombre} ataca a {nombre} : {self.dmg} \n' + txt_cantidad

    def recibir_dmg(self, dmg, aliado):
        """
        Recibe el daño del enemigo

        Parámetros
        ------------
        dmg: daño a recibir
        aliado: lista con las tropas de su mismo ejército

        Returns
        ----------
        str
            mensaje con la cantidad actualizada de tropas que han muerto
        """
        self.vida = self.vida - dmg
        if self.vida <= 0:
            self.vida = 0
        return self.actualizar_cantidad(aliado)

    def __iadd__(self, other):
        """
        Metodo para sumar

        Parámetros
        -----------
        other: objeto a sumar

        Returns
        ---------
        self
            instancia actualizada con la nueva cantidad

        """
        if isinstance(other, Tropa):
            self.cantidad += other.cantidad
        else:
            self.cantidad += other
        return self

    def __isub__(self, other):
        """
        Función para restar

        Parámetros
        -----------
        other: objeto a restar

        Returns
        ---------
        self
            instancia actualizada con la nueva cantidad

        """
        self.cantidad -= other
        return self

    def __add__(self, other):
        """
        Función que devuelve una nueva instancia de Tropa con la cantidad sumada

        Parámetros
        -----------
        other: objeto con el que operar

        Returns
        ---------
        self
            intancia con la nueva cantidad sumada

        """
        nueva_cantidad = self.cantidad
        if isinstance(other, Tropa): # Es una Tropa
            nueva_cantidad += other.cantidad
        else: # Es un entero
            nueva_cantidad += other

        return self.__class__(nueva_cantidad, self.recursos, self.nombre)
    
    def __sub__(self, other):
        """
        Función que devuelve una nueva instancia de Tropa con la cantidad restada

        Parámetros
        -----------
        other: objeto con el que operar

        Returns
        ---------
        self
            intancia con la nueva cantidad restada

        """
        nueva_cantidad = self.cantidad
        if isinstance(other, Tropa): # Es una Tropa
            nueva_cantidad -= other.cantidad
        else: # Es un entero
            nueva_cantidad -= other

        return self.__class__(nueva_cantidad, self.recursos, self.nombre)
    
    def __eq__(self, other):
        """
        Función para comparar dos tropas según su nombre

        Parámetros
        ------------
        other: objeto a comparar

        Returns
        ---------
        bool
            True si los nombres coinciden, False si no se cumple la igualdad

        """
        if isinstance(other, Tropa):
            return self.nombre == other.nombre
        else:
            return self.nombre.lower() == other
    
    def __str__(self):
        """
        Función str para mostrar la información del objeto

        Returns
        ----------
        str
            cadena de texto con la información de la instancia
        """
        texto = f"{self.nombre}: Daño: {self.__class__.dmg_base}, Vida: {self.__class__.vida_base}"
        if self.cantidad > 0:
            texto += f', Cantidad: {self.cantidad}'
        return texto 

    def __repr__(self):
        """
        Función str para mostrar la información del objeto

        Returns
        ----------
        str
            cadena de texto con la información de la instancia
        """
        return f'Tropa \nNombre: {self.nombre} Cantidad: {self.cantidad}'

    


class TropaAtaque(Tropa):
    """
    Subclase para crear las tropas de ataque del reino
    Hereda de la clase base Tropa, modifica el metodo recibir_dmg() para recibir menos daño

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
    recibir_dmg: metodo para recibir el daño enemigo
    critico: calcula la probabilidad de dar un golpe crítico
    atacar: metodo para atacar al enemigo
    """
    def critico(self) -> tuple:
        """
        Función para calcular la probabilidad de dar un golpe crítico

        Returns
        ---------
        tuple
            bool: True si se da el golpe crítico, False si no se da
            int: 2 si golpe crítico, 1 si no
            str: solo si se da el golpe crítico
        """
        if self.vida < self.__class__.vida_base:
            if random.random() < 0.8:  # < 80% de probabilidad
                return True, 2, f'{self.nombre} : Golpe crítico \n'
        else:
            if random.random() < 0.2:  # < 20% de probabilidad
                return True, 2, f'{self.nombre} : Golpe crítico \n'
        return False, 1

    def atacar(self, aliado: list[Tropa], enemigo: list[Tropa]) -> str:
        """
        Función para realizar un ataque

        Parámetros
        -----------------
        aliado: lista con las tropas aliadas
        enemigo: lista con las tropas enemigas

        Returns
        -----------
        str
            mensaje de texto describiendo el ataque
        """
        if enemigo != []:
            critico = self.critico()
            n = random.randint(0, len(enemigo) - 1)  # Elegimos una tropa al azar de la lista
            nombre = enemigo[n].nombre
            if critico[0]:
                dmg = self.dmg * critico[1]
                txt_cantidad = enemigo[n].recibir_dmg(dmg, enemigo)
                return critico[2] + f'{self.nombre} ataca a {nombre} : {dmg} \n' + txt_cantidad
            else:
                txt_cantidad = enemigo[n].recibir_dmg(self.dmg, enemigo)
                return f'{self.nombre} ataca a {nombre} : {self.dmg} \n' + txt_cantidad


class TropaDefensa(Tropa):
    """
    Subclase para crear las tropas de defensa del reino
    Hereda de la clase base Tropa, modifica el metodo recibir_dmg() para recibir menos daño

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
    recibir_dmg: metodo para recibir el daño enemigo
    """

    def recibir_dmg(self, dmg, aliado, reducion=0.8):
        """
        Recibe el daño del enemigo

        Parámetros
        ------------
        dmg: daño a recibir
        aliado: lista con las tropas de su mismo ejército
        reducion: porcentaje de reduccion de danyo recibido
        Returns
        ----------
        str
            mensaje con la cantidad actualizada de tropas que han muerto
        """
        dmg_reducido = dmg * reducion
        self.vida = self.vida - dmg_reducido
        if self.vida <= 0:
            self.vida = 0
        return self.actualizar_cantidad(aliado)


class TropaAlcance(Tropa):
    """
    Subclase para crear las tropas de tipo alcance
    Hereda de la clase base Tropa todos sus métodos
    """


class TropaEstructura(Tropa):
    """
    Subclase para crear las tropas de tipo estructura
    Hereda de la clase base Tropa todos sus métodos
    """


# TROPAS DE ATAQUE
class Soldado(TropaAtaque):
    """
        Subclase para crear las tropas soldado
        Hereda de la subclase TropaAtaque, redefine el constructor

        Atributos
        -----------
        recursos: int
            Coste de recursos para entrenar la tropa.
        nombre: str
            Nombre de la tropa.
        cantidad: int
            Número de instancias de esta tropa.
        dmg_base: int
            daño generado base del soldado
        vida_base: int
            vida base del soldado
        recursos: Recurso
            recursos necesarios para entranar la tropa

        """
    dmg_base = 100  #Daño de la tropa
    vida_base = 150  #Vida de la tropa
    recursos = Recurso('caza',10,0)
    def __init__(self, cantidad=0, recursos=50, nombre='Soldado'):
        super().__init__(recursos, nombre, cantidad)

class Oso(TropaAtaque):
    """
    Subclase para crear las tropas oso
    Hereda de la subclase TropaAtaque, redefine el constructor

    Atributos
    -----------
    recursos: int
        Coste de recursos para entrenar la tropa.
    nombre: str
        Nombre de la tropa.
    cantidad: int
        Número de instancias de esta tropa.
    dmg_base: int
        daño generado base del soldado
    vida_base: int
        vida base del soldado
    recursos: Recurso
        recursos necesarios para entranar la tropa

    Metodos
    ------------

    recibir_dmg: metodo para recibir el daño enemigo
    critico: calcula la probabilidad de dar un golpe crítico
    atacar: metodo para atacar al enemigo
    """
    dmg_base=20
    vida_base=100
    recursos=Recurso('caza',30,0)
    def __init__(self,cantidad=0, recursos=30, nombre='Oso'):
        super().__init__(recursos, nombre, cantidad)
 
# TROPAS DE DEFENSA
class Gigante(TropaDefensa):
    """
    Subclase para crear las tropas oso
    Hereda de la subclase TropaDefensa, redefine el constructor

    Atributos
    -----------
    recursos: int
        Coste de recursos para entrenar la tropa.
    nombre: str
        Nombre de la tropa.
    cantidad: int
        Número de instancias de esta tropa.
    dmg_base: int
        daño generado base del soldado
    vida_base: int
        vida base del soldado
    recursos: Recurso
        recursos necesarios para entranar la tropa

    Metodos
    ------------
    atacar: metodo de ataque del gigante
    recibir_dmg: metodo para recibir el daño enemigo
    """
    dmg_base = 100
    vida_base = 250
    recursos = Recurso('caza', 20, 0)
    def __init__(self, cantidad=0, recursos=50, nombre='Gigante'):
        super().__init__(recursos, nombre, cantidad)

    def atacar(self, aliado: list[Tropa], enemigo: list[Tropa]):  # Solo ataca estructuras
        """
        Metodo para atacar con el gigante

        Parámetros
        -------------
        aliado: lista con las tropas aliadas
        enemigo: lista con las tropas enemigas

        Returns
        ----------
        str
            mensaje para mostrar que se ha realizado el ataque
        """
        if enemigo != []:
            txt = None
            for i in enemigo:
                if isinstance(i, TropaEstructura):
                    if txt == None:
                        txt = ''
                    txt += f'{self.nombre} ataca a {i.nombre} \n' + i.recibir_dmg(self.dmg, enemigo)
            return txt
class Ogro(TropaDefensa):
    """
    Subclase para crear las tropas ogro
    Hereda de la subclase TropaDefensa, redefine el constructor

    Atributos
    -----------
    recursos: int
        Coste de recursos para entrenar la tropa.
    nombre: str
        Nombre de la tropa.
    cantidad: int
        Número de instancias de esta tropa.
    dmg_base: int
        daño generado base del soldado
    vida_base: int
        vida base del soldado
    recursos: Recurso
        recursos necesarios para entranar la tropa

    Metodos
    -------------
    recibir_dmg: metodo para recibir el daño enemigo
    """
    dmg_base=30
    vida_base=400
    recursos=Recurso('caza',50,0)
    def __init__(self,cantidad=0, recursos=50, nombre='Ogro'):
        super().__init__(recursos, nombre, cantidad)

# TROPAS DE ALCANCE
class Arquero(TropaAlcance):
    """
    Subclase para crear las tropas arquero
    Hereda de la subclase TropaAlcance, redefine el constructor

    Atributos
    -----------
    recursos: int
        Coste de recursos para entrenar la tropa.
    nombre: str
        Nombre de la tropa.
    cantidad: int
        Número de instancias de esta tropa.
    dmg_base: int
        daño generado base del soldado
    vida_base: int
        vida base del soldado
    recursos: Recurso
        recursos necesarios para entranar la tropa

    Metodos
    ---------
    atacar: metodo para atacar con la tropa arquero
    """
    dmg_base = 80
    vida_base = 150
    recursos = Recurso('caza', 5, 0)
    def __init__(self, cantidad=0, recursos=50, nombre='Arquero'):
        super().__init__(recursos, nombre, cantidad)

    def atacar(self, aliado: list[Tropa], enemigo: list[Tropa]):
        """
        Metodo para atacar con el arquero

        Parámetros
        -------------
        aliado: lista con las tropas aliadas
        enemigo: lista con las tropas enemigas

        Returns
        ----------
        str
            mensaje para mostrar que se ha realizado el ataque
        """
        if enemigo != []:
            n = 0
            for i in enemigo[:]:
                if random.random() < 0.8:  # < 80% de probabilidad
                    i.recibir_dmg(self.dmg, enemigo)
                    n += 1
            return f'{self.nombre} acertó {n} veces : {self.dmg * n}'

class Magician(TropaAlcance):
    """
    Subclase para crear las tropas magician
    Hereda de la subclase TropaAlcance, redefine el constructor

    Atributos
    -----------
    recursos: int
        Coste de recursos para entrenar la tropa.
    nombre: str
        Nombre de la tropa.
    cantidad: int
        Número de instancias de esta tropa.
    dmg_base: int
        daño generado base del soldado
    vida_base: int
        vida base del soldado
    recursos: Recurso
        recursos necesarios para entranar la tropa

    Metodos
    ------------
    curar: metodo para cuarar aliados
    atacar: metodo para atacar con la tropa magician


    """
    dmg_base=50
    vida_base=100
    recursos=Recurso('caza',50,0)
    healing_base=20
    def __init__(self,cantidad=0, recursos=50, nombre='Mago'):
        super().__init__(recursos, nombre, cantidad)
        self.heal = self.__class__.healing_base * self.cantidad
       
    def curar(self,aliado:list[Tropa]):
        """
        Metodo para curar aliados

        Parámetros
        -------------
        aliado: lista con las tropas aliadas

        Returns
        ----------
        str
            mensaje para mostrar que se ha realizado la operación de curar
        """
        if aliado!=[]:
            n = random.randint(0,len(aliado)-1)
            aliado[n].vida+=self.heal*aliado[n].cantidad
            return f'{self.nombre} cura a {aliado[n].nombre} : {self.heal*aliado[n].cantidad} \n'

    def atacar(self, aliado: list[Tropa], enemigo: list[Tropa]):
        """
        Metodo para atacar con el magician

        Parámetros
        -------------
        aliado: lista con las tropas aliadas
        enemigo: lista con las tropas enemigas

        Returns
        ----------
        str
            mensaje para mostrar que se ha realizado el ataque
        """
        if enemigo != []:
            self.heal = self.__class__.healing_base * self.cantidad
            n = random.randint(0, len(enemigo) - 1)
            dmg=self.dmg
            nombre=enemigo[n].nombre
            text_cantidad = enemigo[n].recibir_dmg(dmg,aliado) #Este texto devuelve si murieron tropas del enemigo
            txt_healing=self.curar(aliado)
            return (f'{self.nombre} ataca a {nombre} : {dmg}\n{text_cantidad}\n{txt_healing}')

        
# TROPAS DE ESTRUCTURA
class Cannon(TropaEstructura):
    """
    Subclase para crear las tropas cannon. ataca cada 2 turnos de combate y tiene daño en area
    Hereda de la subclase TropaEsctructura, redefine el constructor

    Atributos
    -----------
    recursos: int
        Coste de recursos para entrenar la tropa.
    nombre: str
        Nombre de la tropa.
    cantidad: int
        Número de instancias de esta tropa.
    dmg_base: int
        daño generado base del soldado
    vida_base: int
        vida base del soldado
    recursos: Recurso
        recursos necesarios para entranar la tropa

    Metodos
    ------------
    toggle: metodo para activar y desactivar el cannon
    atacar: metodo para atacar con la tropa magician


    """
    dmg_base = 300
    vida_base = 500
    recursos = Recurso('madera', 100, 0)
    def __init__(self, cantidad=0, recursos=100, nombre='Cannon'):
        super().__init__(recursos, nombre, cantidad)
        self.activo = True

    def toggle(self) -> bool:  # Activa y desactiva el cañon
        """
        Metodo para activar o desactivar el cannon

        Returns
        ----------
        bool
            True si está activado, False si no lo está
        """
        estado = self.activo
        self.activo = not self.activo
        return estado

    def atacar(self, aliado: list[Tropa], enemigo: list[Tropa]):
        """
        Metodo para atacar con el cañon

        Parámetros
        -------------
        aliado: lista con las tropas aliadas
        enemigo: lista con las tropas enemigas

        Returns
        ----------
        str
            mensaje para mostrar que se ha realizado el ataque o no
        """
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
            
class Catapulta(TropaEstructura):
    """
    Subclase para crear las tropas catapulta
    Hereda de la subclase TropaEsctructura, redefine el constructor

    Atributos
    -----------
    recursos: int
        Coste de recursos para entrenar la tropa.
    nombre: str
        Nombre de la tropa.
    cantidad: int
        Número de instancias de esta tropa.
    dmg_base: int
        daño generado base del soldado
    vida_base: int
        vida base del soldado
    recursos: Recurso
        recursos necesarios para entranar la tropa
"""
    dmg_base=275
    vida_base=200
    recursos=Recurso('madera',200,0)
    def __init__(self,cantidad=0, recursos=200, nombre='Catapulta'):
        super().__init__(recursos, nombre, cantidad)













