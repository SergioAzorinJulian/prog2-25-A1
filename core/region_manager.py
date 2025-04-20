import random
from region import Region
from recursos import Recurso


class RegionManager:
    """
    Clase encargada de gestionar las regiones y sus recursos en el mapa.

    Attributes
    ----------
    mapa : Mapa
        Instancia del mapa que contiene las regiones.
    regiones : dict
        Diccionario con las regiones del mapa.
    recurso_presente : dict
        Diccionario que indica si un recurso se ha generado en el mapa al menos una vez.
    """

    # Lugares especiales que ofreceran recompensas
    LUGARES_ALEATORIOS = ["Campamento Bárbaro", "Ruinas Antiguas", "Mercado Secreto"]

    def __init__(self, mapa):
        """
        Parameters
        ----------
        mapa : Mapa
            Instancia del mapa que contiene las regiones.
        """

        self.mapa = mapa
        self.regiones = mapa.get_regiones()

        # Diccionario que nos indica si un recurso se ha generado en el mapa al menos una vez
        self.recurso_presente = {recurso: False for recurso in Recurso.PESOS_RECURSOS_BASE.keys()}


    ### GENERACIÓN DE RECURSOS ###
    def generar_recursos(self):
        """
        Asigna recursos a todas las regiones del mapa al inicio del juego, creando instancias de la clase Recurso.

        Raises
        ------
        Exception
            Si ocurre un error al generar los recursos.
        """

        try:
            for region in self.regiones.values():
                recursos = []

                if region.get_es_reino():  # Si la region en cuestion es un reino ...
                    # 80% de probabilidades para obtener 3 recursos en un reino, 20% de obtener 4 recursos
                    cantidad = 3 if random.random() < 0.8 else 4

                    # Recursos base que estaran en todos los reinos
                    recursos.append(Recurso("oro", random.randint(100, 300), 2, 300))
                    recursos.append(Recurso("agua", random.randint(200, 500), 5, 500))
                    comida = random.choice(["caza", "recolección"])
                    recursos.append(Recurso(comida, random.randint(200, 500), 5, 500))

                    cantidad -= 3  # Ya hemos asignado 3 recursos base, si hay extra, se sumarán con seleccionar_recursos()
                    # No contabilizamos si un recurso (comida o agua) ha aparecido en un reino
                    # porque siempre apareceran, lo haremos solo en las zonas neutras

                elif self.es_colindante_con_reino(region):  # Si la region colinda con un reino ...
                    # 60% de probabilidad de obtener 2 recursos, 40% de obtener 3 recursos
                    cantidad = 2 if random.random() < 0.6 else 3

                else:  # Si no colinda con ningun reino ...
                    # 70% de probabilidad de obtener 1 recursos, 30% de obtener 2 recursos
                    cantidad = 1 if random.random() < 0.7 else 2

                recursos.extend(self.seleccionar_recursos(cantidad))
                region.set_recursos(recursos)  # Asignamos los recursos a la region correspondiente

        except Exception as e:
            print(f"Error al generar recursos: {e}")


    def seleccionar_recursos(self, cantidad: int) -> list:
        """
        Selecciona una cantidad específica de recursos con pesos y los asigna a la región.
        Crea instancias de la clase Recurso.

        Parameters
        ----------
        cantidad : int
            Cantidad de recursos a seleccionar.

        Returns
        -------
        list
            Lista con los recursos seleccionados y sus instancias.
        """
        recursos_generados = []

        while len(recursos_generados) < cantidad: # En funcion de cantidad, se asignaran "cantidad" de recursos a la region

            recursos = list(Recurso.PESOS_RECURSOS_BASE.keys())
            pesos = list(Recurso.PESOS_RECURSOS_BASE.values())

            """
            random.choices toma como primer parametro el listado con los recursos base del juego, los que se 
            pueden generar en las zonas neutras. 
            
            Como segundo parametro toma los pesos (probabilidades) que hemos predefinido (lista), lo cual hace 
            que aquellos con mayor peso salgan mas veces que aquellos con menor peso. 
            
            Esta operacion nos devolvera una lista con el elemnto seleccionado, ejemplo ["madera"]. Usamos [0] al
            final para seleccionar este elemento que nos han devuelto, para que deje de ser una lista y pase a ser
            un string.
            """
            recurso_seleccionado = random.choices(recursos, weights=pesos)[0]
            cantidad_recurso = random.randint(100, 300)
            regeneracion_recurso = random.randint(1, 10)

            # Asignar el recurso si no está ya presente
            if recurso_seleccionado not in [recurso.nombre for recurso in recursos_generados]:
                recursos_generados.append(Recurso(recurso_seleccionado, cantidad_recurso, regeneracion_recurso, cantidad_recurso))
                self.recurso_presente[recurso_seleccionado] = True

        return recursos_generados


    def verificar_recursos_faltantes(self):
        """
        Si algún recurso no apareció en ninguna región neutra, forzamos que aparezca en una aleatoria.

        Raises
        ------
        Exception
            Si ocurre un error al verificar los recursos faltantes.
        """
        try:
            regiones_disponibles = list(self.regiones.values())

            for recurso, presente in self.recurso_presente.items():  # Cada recurso y su valor booleano de aparicion

                if not presente:  # Si no esta presente en ningun region neutra (present = False)
                    region_aleatoria = random.choice(regiones_disponibles)  # Se selecciona aleatoriamente una region
                    nuevos_recursos = region_aleatoria.get_recursos()  # Se optiene el diccionario con los recursos de la region
                    cantidad_recurso = random.randint(200, 400)
                    regeneracion_recurso = random.randint(1, 10)
                    nuevos_recursos.append(Recurso(recurso, cantidad_recurso, regeneracion_recurso, cantidad_recurso))  # Cantidades estandar para el nuevo recurso
                    region_aleatoria.set_recursos(nuevos_recursos)

                    self.recurso_presente[recurso] = True  # Ahora ya si que ha aparecido, por lo que cambiamos a True
                                                           # la variable booleana
        except Exception as e:
            print('Error al verificar recursos faltantes:', e)


    ### GESTIÓN DE REGIONES ###
    def es_colindante_con_reino(self, region: Region) -> bool:
        """
        Determina si una región es colindante con un reino.

        Parameters
        ----------
        region : Region
            Instancia de la región a verificar.

        Returns
        -------
        bool
            True si la región es colindante con un reino, False en caso contrario.
        """
        for coord_vecino in region.get_conexiones():  # coord_vecino es una tupla de coordenadas
            if coord_vecino in self.regiones:  # Verificamos si la coordenada existe en el mapa
                vecino = self.regiones[coord_vecino]  # Obtenemos la Region desde el mapa
                if vecino.get_es_reino():  # Ahora podemos llamar get_es_reino() en el objeto Region
                    return True
        return False


    def generar_lugares_aleatorios(self, cantidad: int = 5):
        """
        Genera lugares aleatorios en el mapa, asegurando que no aparezcan en un reino.

        Parameters
        ----------
        cantidad : int, optional
            Cantidad de lugares aleatorios a generar (por defecto es 5).
        """

        """
        Este for ternario, junto a un if ternario simplemente añade a la lista
        todas las regiones que hay en el mapa (self.regiones) que no sean reinos
        (region.get_es_reino())
        """
        regiones_validas = [region for region in self.regiones.values() if not region.get_es_reino()]

        if len(regiones_validas) < cantidad:
            # Si se tratan de anyadir mas zonas especiales en el mapa que regiones que no son reinos,
            # la cantidad se ajusta a lo que sea menor
            cantidad = len(regiones_validas)

        for _ in range(cantidad): # Ponemos _ porque no utilizamos la variable para nada
            region_aleatoria = random.choice(regiones_validas) # Elegimos una region de las que no son reinos
            lugar = random.choice(self.LUGARES_ALEATORIOS) # Elegimos un lugar/zona del listado
            region_aleatoria.set_lugar_especial(lugar) # Se le asigna a la region/zona
            regiones_validas.remove(region_aleatoria)  # Se elimina del listado porque ya tiene un lugar especial

    def mostrar_regiones_con_lugares(self):
        """
        Devuelve una lista con la información de cada región.

        Returns
        -------
        list
            Lista con la información de cada región.
        """

        info_regiones = []
        for region in self.regiones.values():
            info = (
                f"Región: {region.get_posicion()} - Propietario: {region.get_propietario()}\n"
                f"Terreno: {region.get_tipo_terreno()} - Reino: {region.get_es_reino()}\n"
                f"Recursos: {region.get_recursos() if region.get_recursos() else 'Ninguno'}\n"
                f"Edificios: {region.get_edificios() if region.get_edificios() else 'Ninguno'}\n"
                f"Tropas: {region.get_tropas() if region.get_tropas() else 'Ninguno'}\n"
                f"Conexiones: {region.get_conexiones() if region.get_conexiones() else 'Ninguno'}\n"
            )
            if region.get_lugar_especial():
                info += f"Lugar Especial: {region.get_lugar_especial()}\n"
            info += "-------------------------------------------------"
            info_regiones.append(info)
        return info_regiones


