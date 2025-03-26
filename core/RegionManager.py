import random
from region import Region


class RegionManager:

    # Lista con los recurso base del juego (los que se generan en las zonas neutras)
    RECURSOS_BASE = ["agua", "piedra", "madera", "hierro", "caza", "recolección"]
    # Recursos especiales (que no se generan en las zonas neutras)
    RECURSOS_ESPECIALES = ["oro"]

    # Lugares especiales que ofreceran recompensas
    LUGARES_ALEATORIOS = ["Campamento Bárbaro", "Ruinas Antiguas", "Mercado Secreto"]

    # Probabilidad de que salga un recurso u otro, mayor peso = mas probable
    PESOS_RECURSOS = {
        "madera": 4,
        "caza": 3,
        "recolección": 3,
        "agua": 3,
        "piedra": 2,
        "hierro": 2
    }

    def __init__(self, mapa):
        self.mapa = mapa
        self.regiones = mapa.get_regiones()

        # Diccionario que nos indica si un recurso se ha generado en el mapa al menos una vez
        self.recurso_presente = {recurso: False for recurso in self.RECURSOS_BASE}


    ### GENERACIÓN DE RECURSOS ###
    def generar_recursos(self):
        """Asigna recursos a todas las regiones del mapa al inicio del juego."""
        for region in self.regiones:
            recursos = {}


            if region.get_es_reino(): # Si la region es un reino, se le asignan sus tres recursos basicos
                recursos["oro"] = random.randint(100, 300)
                recursos["agua"] = random.randint(200, 500)
                comida = random.choice(["caza", "recolección"]) # Se selecciona aleatoriamente un tipo de comida
                recursos[comida] = random.randint(200, 500)
            # No contabilizamos si un recurso (comida o agua) ha aparecido en un reino
            # porque siempre apareceran, lo haremos solo en las zonas neutras

            elif self.es_colindante_con_reino(region):  # Si la región colinda con un reino, tendrá 2 recursos
                recursos.update(self.seleccionar_recursos(2))

            else:  # Si la región no colinda con un reino, tendrá solo 1 recurso
                recursos.update(self.seleccionar_recursos(1))

            region.set_recursos(recursos) # Asignamos los recursos a la region correspondiente


    def seleccionar_recursos(self, cantidad: int) -> dict:
        """Selecciona una cantidad específica de recursos con pesos y los asigna a la región."""
        recursos_generados = {}

        while len(recursos_generados) < cantidad: # En funcion de cantidad, se asignaran "cantidad" de recursos a la region

            lista_pesos = [] # Creamos una lista vacia
            for recurso in self.RECURSOS_BASE: # Almacenamos los pesos para cada recurso
                lista_pesos.append(self.PESOS_RECURSOS[recurso])

            """
            random.choices toma como primer parametro el listado con los recursos base del juego, los que se 
            pueden generar en las zonas neutras. 
            
            Como segundo parametro toma los pesos (probabilidades) que hemos predefinido (lista), lo cual hace 
            que aquellos con mayor peso salgan mas veces que aquellos con menor peso. 
            
            Esta operacion nos devolvera una lista con el elemnto seleccionado, ejemplo ["madera"]. Usamos [0] al
            final para seleccionar este elemento que nos han devuelto, para que deje de ser una lista y pase a ser
            un string.
            """
            recurso_seleccionado = random.choices(self.RECURSOS_BASE, weights=lista_pesos)[0]
            cantidad_recurso = random.randint(100, 300)

            # Asignar el recurso si no está ya presente
            if recurso_seleccionado not in recursos_generados:
                recursos_generados[recurso_seleccionado] = cantidad_recurso
                self.recurso_presente[recurso_seleccionado] = True

        return recursos_generados


    def verificar_recursos_faltantes(self):
        """Si algún recurso no aparecio en ninguna region neutra, forzamos que aparezca en una aleatoria."""
        regiones_disponibles = list(self.regiones)

        for recurso, presente in self.recurso_presente.items(): # Cada recurso y si valor booleano de aparicion

            if not presente: # Si no esta presente en ningun region neutra (present = False)
                region_aleatoria = random.choice(regiones_disponibles)     # Se selecciona aleatoriamente una region
                nuevos_recursos = region_aleatoria.get_recursos()          # Se optiene el diccionario con los recursos de la region
                nuevos_recursos[recurso] = random.randint(200, 400)  # Cantidades estandar para el nuevo recurso
                region_aleatoria.set_recursos(nuevos_recursos)

                self.recurso_presente[recurso] = True                      # Ahora ya si que ha aparecido, por lo que cambiamos a True
                                                                           # la variable booleana


    ### GESTIÓN DE REGIONES ###
    @staticmethod
    def es_colindante_con_reino(region: Region) -> bool:
        """Determina si una región es colindante con un reino."""
        for vecino in region.get_conexiones(): # Buscamos entre los vecinos de una region
            if vecino.get_es_reino(): # Si alguno tiene el atributo de ser reino a True
                return True # Devolvemos que si que es colindante, y ya salimos
        return False # Sino devolvemos que ninguno de sus vecinos es un reino


    @staticmethod
    def asignar_propietario_a_region(region: Region, jugador: str):
        """Asigna un jugador como propietario de una región."""
        region.set_propietario(jugador)


    def generar_lugares_aleatorios(self, cantidad: int = 5):
        """Genera lugares aleatorios en el mapa, asegurando que no aparezcan en un reino."""

        """
        Este for ternario, junto a un if ternario simplemente añade a la lista
        todas las regiones que hay en el mapa (self.regiones) que no sean reinos
        (region.get_es_reino())
        """
        regiones_validas = [region for region in self.regiones if not region.get_es_reino()]

        if len(regiones_validas) < cantidad:
            # Si se tratan de anyadir mas zonas especiales en el mapa que regiones que no son reinos,
            # la cantidad se ajusta a lo que sea menor
            cantidad = len(regiones_validas)

        for _ in range(cantidad): # Ponemos _ porque no utilizamos la variable para nada
            region_aleatoria = random.choice(regiones_validas) # Elegimos una region de las que no son reinos
            lugar = random.choice(self.LUGARES_ALEATORIOS) # Elegimos un lugar/zona del listado
            region_aleatoria.asignar_lugar_especial(lugar) # Se le asigna a la region/zona
            regiones_validas.remove(region_aleatoria)  # Se elimina del listado porque ya tiene un lugar especial


    def mostrar_regiones_con_lugares(self):
        """Muestra todas las regiones que tienen un lugar especial."""
        for region in self.regiones:
            if region.get_lugar_especial():
                propietario = region.get_propietario() or "Neutral"
                print(f"Región {region.get_posicion()} ({propietario}) tiene un {region.get_lugar_especial()}")


