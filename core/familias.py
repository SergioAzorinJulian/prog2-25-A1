#Carlos Peñalver Mora


#Clase para definir familias en general
class Familia:
    def __init__(self, id_familia: int, miembros: int = 5, rango: int = 1):
        self.id = id_familia
        self.miembros = miembros
        self.tarea_asignada = None
        self.viva = True
        self.rango = rango

    def asignar_tarea(self, tarea: str):
        if self.viva:
            self.tarea_asignada = tarea
        else:
            print('Esta familia no está viva y no puede ser asignada a tareas.')

    def sufrir_bajas(self, cantidad: int):
        self.miembros -= cantidad
        if self.miembros <= 0:
            self.miembros = 0
            self.viva = False
            self.tarea_asignada = None

    def aumentar_miembros(self, cantidad: int):
        if self.viva:
            self.miembros += cantidad

    def aumentar_rango(self):
        if self.viva:
            self.rango += 1

    def __str__(self):
        estado = "viva" if self.viva else "muerta"
        tarea = self.tarea_asignada if self.tarea_asignada else "ninguna"
        return (f"Familia {self.id} | Miembros: {self.miembros} | "
                f"Rango: {self.rango} | Estado: {estado} | Tarea asignada: {tarea}")

#Clase para añadir o consultar familias
class GestorFamilias:
    def __init__(self):
        self.familias = []
        self.contador_id = 0

    def crear_familia(self, miembros: int = 5, rango: int = 1):
        nueva_familia = Familia(id_familia=self.contador_id, miembros=miembros, rango=rango)
        self.familias.append(nueva_familia)
        self.contador_id += 1
        return nueva_familia

    def mostrar_familias(self):
        print("Registro de familias:")
        for familia in self.familias:
            print(familia)
