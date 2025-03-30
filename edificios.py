
class Edificio:

    """
    Clase base para representar un edificio dentro del juego y sus mejoras.

    ATRIBUTOS:
    -------------
    nombre: str
        Nombre del edificio.

    nivel: int
        Nivel actual del edificio, que puede ser mejorado.

    costo_mejora: dict
        Diccionario que contiene los recursos necesarios para mejorar el edificio.

    familias_asignadas: int
        Número de familias necesarias para operar o mejorar el edificio.

    METODOS:
    -----------
    subir_nivel: bool
        Intenta mejorar el nivel del edificio si hay suficientes recursos y familias disponibles.
        Reduce los recursos utilizados y aumenta el nivel en caso de éxito.

    __str__: str
        Representación en cadena del edificio, mostrando su nombre, nivel y familias asignadas.
    """

    def __init__(self, nombre: str, nivel: int, costo_mejora: dict, familias_asignadas: int):
        self.nombre = nombre
        self.nivel = nivel
        self.costo_mejora = costo_mejora  #Diccionario con los recursos necesarios para mejorar
        self.familias_asignadas = familias_asignadas

    def subir_nivel(self, recursos_disponibles: dict, familias_disponibles: int):
        if familias_disponibles < self.familias_asignadas:
            print(f"No hay suficientes familias para mejorar {self.nombre}.")
            return False

        for recurso, cantidad in self.costo_mejora.items():
            if recurso not in recursos_disponibles or recursos_disponibles[recurso].cantidad < cantidad:
                print(f"No hay suficientes {recurso} para mejorar {self.nombre}.")
                return False

        # Restar los recursos usados
        for recurso, cantidad in self.costo_mejora.items():
            recursos_disponibles[recurso].cantidad -= cantidad

        self.nivel += 1
        print(f"El {self.nombre} ha subido al nivel {self.nivel}.")
        return True

    def __str__(self):
        return f"{self.nombre} (Nivel {self.nivel}) - Familias asignadas: {self.familias_asignadas}"

# Clases de edificios

class Mina(Edificio):

    """
    Clase Mina (hereda de Edificio): Representa una mina dentro del juego.

    ATRIBUTOS:
    -------------
    produccion_por_nivel: int
        Cantidad de piedra producida por cada nivel de la mina.

    METODOS:
    -----------
    producir: dict
        Devuelve un diccionario con la cantidad de piedra generada según el nivel de la mina.
    """

    def __init__(self, nivel=1):
        super().__init__("Mina", nivel, {"piedra": 10 * nivel, "madera": 5 * nivel}, familias_asignadas=2)
        self.produccion_por_nivel = 5  # La mina produce más recursos al subir de nivel

    def producir(self):
        return {"piedra": self.produccion_por_nivel * self.nivel}


class Granja(Edificio):

    """
    Clase Granja (hereda de Edificio): Representa una granja dentro del juego.

    ATRIBUTOS:
    -------------
    produccion_por_nivel: int
        Cantidad de comida producida por cada nivel de la granja.

    METODOS:
    -----------
    producir: dict
        Devuelve un diccionario con la cantidad de comida generada según el nivel de la granja.
    """

    def __init__(self, nivel=1):
        super().__init__("Granja", nivel, {"madera": 8 * nivel, "agua": 6 * nivel}, familias_asignadas=3)
        self.produccion_por_nivel = 10

    def producir(self):
        return {"comida": self.produccion_por_nivel * self.nivel}

class Almacén(Edificio):

    """
    Clase Almacén (hereda de Edificio): Representa un almacén para recursos.

    ATRIBUTOS:
    -------------
    capacidad_comida: int
        Capacidad máxima de almacenamiento de comida.

    capacidad_agua: int
        Capacidad máxima de almacenamiento de agua.
    """

    def __init__(self, nivel=1, capacidad_agua, capacidad_comida):
        super().__init__("Almacén", nivel, {"": 8 * nivel, "agua": 6 * nivel}, familias_asignadas=1)
        self.capacidad_comida = capacidad_comida
        self.capacidad_agua = capacidad_agua