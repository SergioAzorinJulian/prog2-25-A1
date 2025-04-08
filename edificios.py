'''
La clase Edificio representa cualquier estructura dentro del reino.
Es la clase base para todos los edificios.

Atributos
----------
nombre : str - Nombre del edificio.
nivel : int - Nivel actual del edificio.
costo_construccion : dict - Costo inicial para construir el edificio.
costo_mejora : dict - Diccionario con los recursos necesarios para mejorar el edificio.
familias_asignadas : int - Número de familias necesarias para operar o mejorar el edificio.

Métodos
---------
__init__ : Constructor de la instancia.
construir : Construye el edificio si hay suficientes recursos y familias disponibles.
subir_nivel : Sube el nivel del edificio si hay suficientes recursos y familias disponibles.
__str__ : Devuelve información del edificio.
'''

class Edificio:
    def __init__(self, nombre: str, nivel: int, costo_construccion: dict, familias_asignadas: int):
        self.nombre = nombre
        self.nivel = nivel
        self.costo_construccion = costo_construccion
        self.costo_mejora = {}
        self.familias_asignadas = familias_asignadas

    def construir(self, recursos_disponibles: dict, familias_disponibles: int):
        if self.nivel > 0:
            print(f"{self.nombre} ya está construido.")
            return False

        if familias_disponibles < self.familias_asignadas:
            print(f"No hay suficientes familias para construir {self.nombre}.")
            return False

        for recurso in self.costo_construccion:
            cantidad_necesaria = self.costo_construccion[recurso]
            if recurso in recursos_disponibles:
                cantidad_disponible = recursos_disponibles[recurso].cantidad
                if cantidad_disponible < cantidad_necesaria:
                    print(f"No hay suficientes {recurso} para construir {self.nombre}.")
                    return False
            else:
                print(f"Falta el recurso {recurso} para construir {self.nombre}.")
                return False

        for recurso in self.costo_construccion:
            recursos_disponibles[recurso].cantidad -= self.costo_construccion[recurso]

        self.nivel = 1
        print(f"{self.nombre} ha sido construido.")
        return True

    def subir_nivel(self, recursos_disponibles: dict, familias_disponibles: int):
        if self.nivel == 0:
            print(f"{self.nombre} aún no ha sido construido.")
            return False

        if familias_disponibles < self.familias_asignadas:
            print(f"No hay suficientes familias disponibles para mejorar {self.nombre}.")
            return False

        for recurso, cantidad in self.costo_mejora.items():
            if recurso not in recursos_disponibles or recursos_disponibles[recurso].cantidad < cantidad:
                print(f"No hay suficientes {recurso} para mejorar {self.nombre}.")
                return False

        for recurso, cantidad in self.costo_mejora.items():
            recursos_disponibles[recurso].cantidad -= cantidad

        self.nivel += 1
        print(f"El {self.nombre} ha subido al nivel {self.nivel}.")
        return True

    def __str__(self):
        return f"{self.nombre} (Nivel {self.nivel}) - Familias asignadas: {self.familias_asignadas}"


# Clases de edificios generadores

'''
Las siguientes clases heredan de Edificio y representan estructuras
que producen recursos o cumplen una función en el reino.
'''

class Mina(Edificio):
    '''
    Descripción: representa una mina que produce piedra.

    INFORMACIÓN
     ----------------------------------------
     - Recurso producido: piedra
     - Construcción: 10 piedra, 5 madera
     - Mejora: 10 * nivel piedra, 5 * nivel madera
     - Familias necesarias: 2
     ----------------------------------------

    Métodos adicionales
    -------------------
    producir : Devuelve la cantidad de piedra producida según el nivel.
    '''
    def __init__(self, nivel=0):
        super().__init__("Mina", nivel, {"piedra": 10, "madera": 5}, familias_asignadas=2)
        self.costo_mejora = {"piedra": 10 * max(nivel, 1), "madera": 5 * max(nivel, 1)}
        self.produccion_por_nivel = 5

    def producir(self):
        return {"piedra": self.produccion_por_nivel * self.nivel}


class Granja(Edificio):
    '''
    Representa una granja que produce comida.

    INFORMACIÓN
     ----------------------------------------
     - Recurso producido: comida
     - Construcción: 8 madera, 6 agua
     - Mejora: 6 * nivel agua, 8 * nivel madera
     - Familias necesarias: 1
     ----------------------------------------

    Métodos adicionales
    -------------------
    producir : Devuelve la cantidad de comida producida según el nivel.
    '''
    def __init__(self, nivel=0):
        super().__init__("Granja", nivel, {"madera": 8, "agua": 6}, familias_asignadas=1)
        self.costo_mejora = {"madera": 8 * max(nivel, 1), "agua": 6 * max(nivel, 1)}
        self.produccion_por_nivel = 10

    def producir(self):
        return {"comida": self.produccion_por_nivel * self.nivel}


class Pozo(Edificio):
    '''
    Representa un pozo que produce agua.

    INFORMACIÓN
    ----------------------------------------
    - Recurso producido: agua
    - Construcción: 3 madera, 5 piedra
    - Mejora: 3 * nivel madera, 5 * nivel piedra
    - Familias necesarias: 1
    ----------------------------------------

    Métodos adicionales
    -------------------
    producir : Devuelve la cantidad de agua producida según el nivel.
    '''
    def __init__(self, nivel=0):
        super().__init__("Pozo", nivel, {"madera": 3, "piedra": 5}, familias_asignadas=1)
        self.costo_mejora = {"madera": 3 * max(nivel, 1), "piedra": 5 * max(nivel, 1)}
        self.produccion_por_nivel = 10

    def producir(self):
        return {"agua": self.produccion_por_nivel * self.nivel}


class Muros(Edificio):
    '''
    Representa los muros defensivos del reino.

    INFORMACIÓN
    ----------------------------------------
    - Propósito: defensa (no produce recursos)
    - Construcción: 5 madera, 5 piedra
    - Mejora: 5 * nivel madera, 5 * nivel piedra
    - Familias necesarias: 0
    - Vida: 50 * nivel
 ----------------------------------------

    Atributos adicionales
    ---------------------
    vida : int
        Puntos de vida de los muros.
    '''
    def __init__(self, nivel=0):
        super().__init__('Muros', nivel, {'madera': 5, 'piedra': 5}, familias_asignadas=0)
        self.costo_mejora = {'madera': 5 * max(nivel, 1), 'piedra': 5 * max(nivel, 1)}
        self.vida = 50 * max(nivel, 1)


class GranAlmacén(Edificio):
    '''
    Representa el almacén central del reino, donde se guardan recursos como agua y comida.

    Atributos adicionales
    ---------------------
    capacidad_comida : int - Capacidad máxima de almacenamiento de comida.
    capacidad_agua : int - Capacidad máxima de almacenamiento de agua.
    cantidad_agua : int - Cantidad actual de agua almacenada.
    cantidad_comida : int - Cantidad actual de comida almacenada.
    '''
    def __init__(self, capacidad_agua, capacidad_comida, cantidad_agua, cantidad_comida, nivel=1):
        super().__init__("Almacén", nivel, {"piedra": 8, "madera": 6}, familias_asignadas=3)
        self.costo_mejora = {"piedra": 8 * max(nivel, 1), "madera": 6 * max(nivel, 1)}
        self.capacidad_comida = capacidad_comida
        self.capacidad_agua = capacidad_agua
        self.cantidad_agua = cantidad_agua
        self.cantidad_comida = cantidad_comida

    def __str__(self):
        return (f'Nivel: {self.nivel})'
                f'Nivel de agua: {self.cantidad_agua} / {self.capacidad_agua}'
                f'Nivel de comida: {self.cantidad_comida} / {self.capacidad_comida}')


class Castillo(Edificio):
    '''
    Representa el castillo del reino, el edificio principal.

    Atributos adicionales
    ---------------------
    vida : int - Puntos de vida del castillo.
    '''
    def __init__(self, nivel=1):
        super().__init__('Castillo', nivel, {"piedra": 0, "madera": 0}, familias_asignadas=0)
        self.costo_mejora = {"piedra": 15 * nivel, "madera": 10 * nivel}
        self.vida = 100 * nivel
