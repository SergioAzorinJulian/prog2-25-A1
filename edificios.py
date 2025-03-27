

class Edificio:
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
    def __init__(self, nivel=1):
        super().__init__("Mina", nivel, {"piedra": 10 * nivel, "madera": 5 * nivel}, familias_asignadas=2)
        self.produccion_por_nivel = 5  # La mina produce más recursos al subir de nivel

    def producir(self):
        return {"piedra": self.produccion_por_nivel * self.nivel}


class Granja(Edificio):
    def __init__(self, nivel=1):
        super().__init__("Granja", nivel, {"madera": 8 * nivel, "agua": 6 * nivel}, familias_asignadas=3)
        self.produccion_por_nivel = 10

    def producir(self):
        return {"comida": self.produccion_por_nivel * self.nivel}

class Almacén(Edificio):
    def __init__(self, nivel=1, capacidad_agua, capacidad_comida):
        super().__init__("Almacén", nivel, {"": 8 * nivel, "agua": 6 * nivel}, familias_asignadas=1)
        self.capacidad_comida = capacidad_comida
        self.capacidad_agua = capacidad_agua