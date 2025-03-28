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

        self.generar_recursos()
        self.verificar_recursos_faltantes()

    ### GENERACIÓN DE RECURSOS ###
    def generar_recursos(self):
        """Asigna recursos a todas las regiones del mapa al inicio del juego."""
        for region in self.regiones:
            recursos = {}

            if region.get_es_reino(): # Si la region en cuestion es un reino ...
                # 80% de probabilidades para obtener 3 recursos en un reino, 20% de obtener 4 recursos
                cantidad = 3 if random.random() < 0.8 else 4

                # Recursos base que estaran en todos los reinos
                recursos["oro"] = random.randint(100, 300)
                recursos["agua"] = random.randint(200, 500)
                comida = random.choice(["caza", "recolección"])
                recursos[comida] = random.randint(200, 500)

                cantidad -= 3  # Ya hemos asignado 3 recursos base, si hay extra, se sumarán con seleccionar_recursos()
            # No contabilizamos si un recurso (comida o agua) ha aparecido en un reino
            # porque siempre apareceran, lo haremos solo en las zonas neutras

            elif self.es_colindante_con_reino(region): # Si la region colinda con un reino ...
                # 60% de probabilidad de obtener 2 recursos, 40% de obtener 3 recursos
                cantidad = 2 if random.random() < 0.6 else 3

            else: # Si no colinda con ningun reino ...
                # 70% de probabilidad de obtener 1 recursos, 30% de obtener 2 recursos
                cantidad = 1 if random.random() < 0.7 else 2

            recursos.update(self.seleccionar_recursos(cantidad))
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
        """Devuelve una lista con la información de cada región."""
        info_regiones = []
        for region in self.regiones:
            info = (
                f"Región: {region.get_nombre()} - Propietario: {region.get_propietario()}\n"
                f"Recursos: {', '.join(region.get_recursos()) if region.get_recursos() else 'Ninguno'}\n"
                f"Conexiones: {', '.join([r.get_nombre() for r in region.get_conexiones()])}\n"
                "-------------------------------------------------"
            )
            info_regiones.append(info)
        return info_regiones
