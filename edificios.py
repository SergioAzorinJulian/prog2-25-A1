
'''
La clase Edificio representa cualquier estructura dentro del reino.
Es la clase base para todos los edificios.

Atributos
----------
nombre : str - Nombre del edificio.
nivel : int - Nivel actual del edificio.
costo_mejora : dict - Diccionario con los recursos necesarios para mejorar el edificio.
familias_asignadas : int - Número de familias necesarias para operar o mejorar el edificio.

Métodos
---------
__init__ : Constructor de la instancia.
subir_nivel : Sube el nivel del edificio si hay suficientes recursos y familias disponibles.
__str__ : Devuelve información del edificio.
'''

class Edificio:
    def __init__(self, nombre: str, nivel: int, costo_mejora: dict, familias_asignadas: int):
        self.nombre = nombre
        self.nivel = nivel
        self.costo_mejora = costo_mejora
        self.familias_asignadas = familias_asignadas

    def subir_nivel(self, recursos_disponibles: dict, familias_disponibles: int):
        # Verificar si hay suficientes familias disponibles
        if familias_disponibles < self.familias_asignadas:
            print(f"No hay suficientes familias disponibles para mejorar {self.nombre}.")
            return False

        # Verificar si hay suficientes recursos para mejorar
        for recurso, cantidad in self.costo_mejora.items():
            if recurso not in recursos_disponibles or recursos_disponibles[recurso].cantidad < cantidad:
                print(f"No hay suficientes {recurso} para mejorar {self.nombre}.")
                return False

        # Restar los recursos usados
        for recurso, cantidad in self.costo_mejora.items():
            recursos_disponibles[recurso].cantidad -= cantidad

        # Aumentar el nivel del edificio
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
    Representa una mina que produce piedra.

    Métodos adicionales
    -------------------
    producir : Devuelve la cantidad de piedra producida según el nivel.
    '''
    def __init__(self):
        super().__init__("Mina", nivel, {"piedra": 10 * nivel, "madera": 5 * nivel}, familias_asignadas=2)
        self.produccion_por_nivel = 5  # La mina produce más piedra con cada nivel

    def producir(self):
        return {"piedra": self.produccion_por_nivel * self.nivel}


class Granja(Edificio):
    '''
    Representa una granja que produce comida.

    Métodos adicionales
    -------------------
    producir : Devuelve la cantidad de comida producida según el nivel.
    '''
    def __init__(self):
        super().__init__("Granja", nivel, {"madera": 8 * nivel, "agua": 6 * nivel}, familias_asignadas=1)
        self.produccion_por_nivel = 10  # Producción base de comida

    def producir(self):
        return {"comida": self.produccion_por_nivel * self.nivel}


class Pozo(Edificio):
    '''
    Representa un pozo que produce agua.

    Métodos adicionales
    -------------------
    producir : Devuelve la cantidad de agua producida según el nivel.
    '''
    def __init__(self):
        super().__init__("Pozo", nivel, {"madera": 3 * nivel, "piedra": 5 * nivel}, familias_asignadas=1)
        self.produccion_por_nivel = 10  # Producción base de agua

    def producir(self):
        return {"agua": self.produccion_por_nivel * self.nivel}


class Muros(Edificio):
    '''
    Representa los muros defensivos del reino.

    Atributos adicionales
    ---------------------
    vida : int
        Puntos de vida de los muros.
    '''
    def __init__(self, vida):
        super().__init__('Muros', nivel, {'madera': 5 * nivel, 'piedra': 5 * nivel}, familias_asignadas=0)
        self.vida = vida  # Vida total de los muros
        vida = 50 * nivel  # Vida base según el nivel


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
    def __init__(self, capacidad_agua, capacidad_comida, cantidad_agua, cantidad_comida):
        super().__init__("Almacén", nivel, {"piedra": 8 * nivel, "cristal": 6 * nivel}, familias_asignadas=3)
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
    def __init__(self, vida: int):
        super().__init__("Castillo", nivel, {'piedra': 25 * nivel, 'madera': 20 * nivel}, familias_asignadas=1)
        self.vida = vida  # Vida total del castillo
