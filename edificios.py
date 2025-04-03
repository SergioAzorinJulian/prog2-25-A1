# Clase padre Edificio que se usa de base para cualquier edificio

class Edificio:
    def __init__(self, nombre: str, nivel: int, costo_mejora: dict, familias_asignadas: int):
        self.nombre = nombre
        self.nivel = nivel
        self.costo_mejora = costo_mejora  # Diccionario con los recursos necesarios para mejorar
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


# Edificios generadores

class Mina(Edificio):
    def __init__(self):
        super().__init__("Mina", nivel, {"piedra": 10 * nivel, "madera": 5 * nivel}, familias_asignadas=2)
        self.produccion_por_nivel = 5  # La mina produce más recursos al subir de nivel

    def producir(self):
        return {"piedra": self.produccion_por_nivel * self.nivel}


class Granja(Edificio):  # Cada granja tiene asignada una familia y produce comida
    def __init__(self):
        super().__init__("Granja", nivel, {"madera": 8 * nivel, "agua": 6 * nivel}, familias_asignadas=1)
        self.produccion_por_nivel = 10

    def producir(self):
        return {"comida": self.produccion_por_nivel * self.nivel}


class Pozo(Edificio):  # Cada pozo tiene asignado una familia y produce agua
    def __init__(self):
        super().__init__("Pozo", nivel, {"madera": 3 * nivel, "piedra": 5 * nivel}, familias_asignadas=1)
        self.produccion_por_nivel = 10

    def producir(self):
        return {"agua": self.produccion_por_nivel * self.nivel}


class Muros(Edificio):
    def __init__(self, vida):
        super().__init__('Pozo', nivel, {'madera': 5 * nivel, 'piedra': 5 * nivel}, familias_asignadas=0)
        self.vida = vida
        vida = 50 * nivel


class GranAlmacén(
    Edificio):  # El Gran Almacén es el edificio que guarda todos los recursos para el reino (comida y agua)
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


class Castillo(Edificio):  # El castillo es el edificio principal del reino
    def __init__(self, vida: int):
        super().__init__("Castillo", nivel, {'piedra': 25 * nivel, 'madera': 20 * nivel}, familias_asignadas=1)
        self.vida = vida