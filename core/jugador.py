from mapa import Mapa
from region import Region
from region_manager import RegionManager
from recursos import Recurso
from tropas import *
from edificios import *

'''
PLANTEAMIENTO DEL MENÚ DEL JUGADOR:
    VER MAPA GRÁFICO -> La idea seria mostrar tus zonas con una X, las de nadie con ? y las del enemigo con O (No es prioridad para el viernes)
        Se podría quizá dibujar un grafo, pero ya se verá ... 

    ACCEDER A ZONA:
        (SE MUESTRA LA INFORMACIÓN DE LA ZONA), Se actualiza self.region_actual a la zona que esta viendo
        AÑADIR TROPAS -> Se crean tropas en la zona actual, consume recursos:[] (escribir que recurso consume cada tropa el que lo sepa)
            Tropas normales -> Comida y Agua
            Tropas de asedio (elefantes y arietes) -> Comida, Agua y Madera

        MOVER_TROPA -> Se mueve la tropa indicada a destino, es necesario implementar un método que permita restar cant a la instancia del obj tropa, y otro para sumarlo en caso de que en destino ya esté esa tropa
            Para movimientos dentro de tu dominio -> Puedes avanzar 2 (o 3, ya se ve en el desarrollo) "casillas" en un turno
            Para movimientos en zonas neutras o enemigas -> Puedes avanzar una zona por turno

        MOVER_BATALLÓN -> Lo mismo pero mueve todas las tropas de una

        CONSTRUIR EDIFICIO -> Construye edificios, escribir aquí edificios y recursos que consumen crearlos -> []

        VOLVER

Mover tropa, y mover batallón consumen el turno, si mueves la tropa a territorio enemigo -> COMBATIR o ABORTAR
'''


class Jugador:
    """
    Representa a un jugador en el juego, el cual puede gestionar su reino, recursos,
    tropas y otras acciones sobre el mapa durante las partidas.

    Parameters
    ----------
    usuario : str
        Nombre de usuario del jugador.
    reino : str
        Nombre del reino del jugador.
    mapa : Mapa
        Instancia del mapa del juego.
    recursos : list of Recurso, optional
        Lista de recursos iniciales del jugador.
    conquista : list of tuple of int, optional
        Lista de coordenadas conquistadas por el jugador.

    Attributes
    ----------
    usuario : str
        Nombre de usuario del jugador.
    reino : str
        Nombre del reino del jugador.
    mapa : Mapa
        Instancia del mapa del juego.
    conquista : list of tuple of int
        Coordenadas conquistadas por el jugador.
    recursos : list of Recurso
        Recursos actuales del jugador.
    region_actual : tuple of int or None
        Región actualmente seleccionada por el jugador.
    """


    def __init__(self, usuario, reino, mapa, recursos: list[Recurso] = [Recurso('madera', 100, 0, 100), Recurso('agua', 100, 0, 100),
                                                                 Recurso('piedra', 50, 0, 100), Recurso('hierro', 25, 0, 100),
                                                                 Recurso('oro', 50, 0, 100),
                                                                 Recurso('caza', 400, 0, 400),
                                                                 Recurso('recoleccion', 400, 0, 400)],
                 conquista: list[tuple[int, int]] = []):
        self.usuario = usuario
        self.reino = reino
        self.mapa = mapa
        self.conquista = conquista  # Se debe actualizar en cada interacción
        self.recursos = recursos
        self.region_actual: tuple[int, int] | None = None  # La zona que esta consultando el jugador dentro del bucle principal


    def __str__(self):
        """
        Devuelve el nombre del jugador.

        Returns
        -------
        str
            Nombre del usuario.
        """
        return f'Usuario: {self.usuario}'


    def mapa_grafico(self):
        """
        Muestra el mapa gráfico del jugador.

        X representa las regiones que el jugador posee,
        ? las neutrales y
        O las del enemigo.

        Returns
        -------
        str
            Mapa gráfico en formato de cadena.
        """

        map_graf = '' # Inicializamos el mapa gráfico como una cadena vacía
        fila_previa = -1 # Inicializamos la fila previa a -1
        coordenadas = self.mapa.get_regiones().keys() # Obtenemos todas las coordenadas de las regiones
        coordenadas = sorted(coordenadas)  # Ordenamos las coordenadas por filas y columnas
        todas_regiones = self.mapa.get_regiones() # Obtenemos todas las regiones del mapa

        for coordenada in coordenadas:
            fila_actual = coordenada[0] # Guardamos la fila actual

            # Obtenemos el objeto Region y su propietario
            region = todas_regiones[coordenada]
            propietario = region.get_propietario()

            # Si cambiamos de fila y no es la primera iteración, añadimos un salto de línea
            if fila_actual != fila_previa and fila_previa != -1:
                map_graf += '\n'

            # Actualizamos la fila previa a la actual para la siguiente iteración
            fila_previa = fila_actual

            # Determinamos el símbolo a mostrar en función del propietario de la región
            if propietario == self.usuario:
                map_graf += 'X '
            elif propietario == 'Neutral':
                map_graf += '? '
            else:
                map_graf += 'O '

        # Eliminamos el último espacio en blanco y devolvemos el mapa gráfico
        return map_graf.strip()


    def establecer_reino(self):
        """
        Establece un reino del mapa como propiedad de
        un jugador.

        Asigna el primer reino neutral (sin dueño) disponible al jugador.
        """

        for region in self.mapa.reinos:
            if region.get_propietario() == 'Neutral':
                region.set_propietario(self.usuario)  
                region.set_nombre_reino(self.reino)
                break

    def ver_zona(self, region: tuple[int, int]):
        """
        Actualiza y muestra la información de una región específica.

        Parameters
        ----------
        region : tuple of int
            Coordenadas de la región a consultar.

        Returns
        -------
        tuple
            (Descripción de la región, bool indicando si es propiedad del jugador)
        """
        self.region_actual = region
        return str(self.mapa.regiones[self.region_actual]), True if self.mapa.regiones[self.region_actual].get_propietario() == self.usuario else False


    @classmethod
    def mostrar_catalogo(cls):
        """
        Muestra el catálogo de tipos de tropas disponibles.

        Returns
        -------
        tuple
            (Lista de nombres de tropas válidos, catálogo en formato de cadena)
        """

        if not hasattr(cls, 'tropas_objetos'):
            cls.tropas_objetos = {
                key.lower(): value
                for key, value in globals().items()
                if isinstance(value, type) and (
                        issubclass(value, TropaAtaque) or
                        issubclass(value, TropaDefensa) or
                        issubclass(value, TropaAlcance) or
                        issubclass(value, TropaEstructura)) and value not in (
                   TropaAtaque, TropaDefensa, TropaEstructura,
                   TropaAlcance)}  # isinstance -> objeto, issubclas-> objeto
        catalogo = ''
        for i in cls.tropas_objetos.values():
            catalogo += str(i()) + '\n'
        valores_validos = [key for key in cls.tropas_objetos.keys()]
        return valores_validos, catalogo


    @classmethod
    def mostrar_catalogo_edificios(cls):
        """
        Muestra el catálogo de tipos de edificios disponibles.

        Returns
        -------
        tuple
            (Lista de nombres de edificios válidos, catálogo en formato de cadena)
        """

        if not hasattr(cls,'edificios_objetos'):
            cls.edificios_objetos = {
            key.lower(): value
                for key, value in globals().items()
                if isinstance(value,type) and
                        (issubclass(value, Edificio))
                        and value is not Edificio
        }
        catalogo = ''
        for i in cls.edificios_objetos.values():
            catalogo += str(i()) + '\n'
        valores_validos = [key for key in cls.edificios_objetos.keys()]
        return valores_validos, catalogo


    def add_tropa(self, tropa, cantidad):
        """
        Añade una(s) tropa(s) a la región actual del jugador
        si dispone de recursos suficientes para crearla(s).

        Parameters
        ----------
        tropa : str
            Nombre de la tropa a añadir.
        cantidad : int
            Cantidad de tropas a añadir.

        Returns
        -------
        str
            Mensaje indicando el resultado de la operación.
        """

        costo = self.__class__.tropas_objetos[tropa].recursos
        recurso_player = self.recursos[self.recursos.index(costo)]
        if recurso_player >= costo * cantidad:
            recurso_player -= costo * cantidad
        else:
            return f'Cantidad insuficiente de {costo}'
        nueva_tropa = self.__class__.tropas_objetos[tropa](cantidad=cantidad)
        for i in self.mapa.regiones[self.region_actual].tropas:
            if nueva_tropa == i:
                i += nueva_tropa
                return f'Tropa añadida correctamente'
        self.mapa.regiones[self.region_actual].tropas.append(nueva_tropa)
        return f'Tropa añadida correctamente'


    def mover_tropa(self, destino: tuple[int, int], tropa, cantidad):
        """
        Mueve una tropa desde la región actual a una región destino.

        Parameters
        ----------
        destino : tuple of int
            Coordenadas de la región destino.
        tropa : str
            Nombre de la tropa a mover.
        cantidad : int
            Cantidad de tropas a mover.

        Returns
        -------
        str or tuple
            Mensaje de éxito o error, o tupla con el mensaje a mostrar y
            el valor booleano False si la región es enemiga.
        """

        # Verifica si el destino está dentro de las regiones conquistadas o conectadas; si no, retorna error
        if destino not in self.conquista + self.mapa.regiones[self.region_actual].get_conexiones():
            return f'No puedes moverte a {destino}, fuera de rango'

        # Si el destino es del jugador o neutral, permite el movimiento
        if self.mapa.regiones[destino].get_propietario() == self.usuario or self.mapa.regiones[destino].get_propietario() == 'Neutral':

            # Verifica si la tropa existe en la región actual
            if tropa in self.mapa.regiones[self.region_actual].tropas:
                # Obtiene la tropa a mover
                tropa_mover = self.mapa.regiones[self.region_actual].tropas[self.mapa.regiones[self.region_actual].tropas.index(tropa)]

                # Si hay más tropas de las que se quieren mover
                if  tropa_mover.cantidad > cantidad:
                    nueva_tropa = tropa_mover - cantidad  # Crea una nueva tropa con la cantidad a mover
                    tropa_mover -= cantidad  # Resta la cantidad movida de la tropa original

                    # Si ya existe esa tropa en el destino, sumamos la cantidad
                    if tropa in self.mapa.regiones[destino].tropas:
                        tropa_destino = self.mapa.regiones[destino].tropas[self.mapa.regiones[destino].tropas.index(tropa)]
                        tropa_destino += nueva_tropa
                        self.mapa.regiones[destino].set_propietario(self.usuario)
                        return f'Tropa movida a {destino}'

                    # Si no existe, añadimos la nueva tropa al destino
                    self.mapa.regiones[destino].tropas.append(nueva_tropa)
                    self.mapa.regiones[destino].set_propietario(self.usuario)
                    return f'Tropa movida a {destino}'

                # Si la cantidad es exactamente la que hay, mueve toda la tropa
                elif tropa_mover.cantidad == cantidad:
                    nueva_tropa = self.mapa.regiones[self.region_actual].tropas[self.mapa.regiones[self.region_actual].tropas.index(tropa)]
                    self.mapa.regiones[self.region_actual].tropas.remove(tropa)

                    # Si ya existe esa tropa en el destino, sumamos la cantidad
                    if tropa in self.mapa.regiones[destino].tropas:
                        tropa_destino = self.mapa.regiones[destino].tropas[self.mapa.regiones[destino].tropas.index(tropa)]
                        tropa_destino += nueva_tropa
                        self.mapa.regiones[destino].set_propietario(self.usuario)
                        return f'Tropa movida a {destino}'

                    # Si no existe, añadimos la tropa al destino
                    self.mapa.regiones[destino].tropas.append(nueva_tropa)
                    self.mapa.regiones[destino].set_propietario(self.usuario)
                    return f'Tropa movida a {destino}'

                else:
                    # Si no hay suficientes tropas para mover
                    return f'No dispones de {cantidad} {tropa}'

            # Si la tropa no está en la región actual
            return f'No dispones de {tropa} en la region'

        else:
            # Si la región destino es enemiga, pregunta si desea combatir
            return f'La zona pertenece a {self.mapa.regiones[destino].get_propietario()}\n¿Deseas librar combate?', False


    def mover_batallon(self, destino: tuple[int, int]):
        """
        Mueve todas las tropas de la región actual a una región destino.

        Parameters
        ----------
        destino : tuple of int
            Coordenadas de la región destino.

        Returns
        -------
        str or tuple
            Mensaje de éxito o error, o tupla con el mensaje a mostrar y
            el valor booleano False si la región es enemiga.
        """

        if destino not in self.conquista + self.mapa.regiones[self.region_actual].get_conexiones():
            return f'No puedes moverte a {destino}, fuera de rango'
        if self.mapa.regiones[destino].get_propietario() == self.usuario or self.mapa.regiones[destino].get_propietario() == 'Neutral':
            for i in self.mapa.regiones[self.region_actual].tropas[:]:
                cantidad = i.cantidad
                nombre = i.nombre.lower()
                self.mover_tropa(destino, nombre, cantidad)
            return "Tropas movidas correctamente"
        else:
            return f'La zona pertenece a {self.mapa.regiones[destino].get_propietario()}\nCombatir?',False


    def construir_edificio(self, edificio):
        """
        Construye un edificio en la región actual si el jugador dispone
        de recursos suficientes para hacerlo.

        Parameters
        ----------
        edificio : str
            Nombre del edificio a construir.

        Returns
        -------
        str
            Mensaje indicando el resultado de la operación.
        """

        # Obtenemos el costo del edificio a construir
        costo = self.__class__.edificios_objetos[edificio].costo
        # Verificamos si el jugador tiene suficientes recursos para construir el edificio
        if all(self.recursos[self.recursos.index(recurso)] >= recurso for recurso in costo):
            # Descontamos los recursos necesarios
            for recurso in costo:
                self.recursos[self.recursos.index(recurso)] -= recurso
            # Añadimos el edificio a la región actual
            self.mapa.regiones[self.region_actual].edificios.append(self.__class__.edificios_objetos[edificio]())
            return f'Edificio: {edificio} construido'
        else:
            # Si no hay recursos suficientes, devolvemos un mensaje de error
            return 'Recursos insuficientes'


    def subir_nivel_edificio(self, edificio: 'Edificio'):
        """
        Sube el nivel de un edificio en la región actual si es posible.

        Parameters
        ----------
        edificio : Edificio
            Instancia del edificio a mejorar.

        Returns
        -------
        str
            Mensaje indicando el resultado de la operación.
        """

        # Verifica si el edificio está en la lista de edificios de la región actual
        if edificio in self.mapa.regiones[self.region_actual].edificios:
            # Busca el edificio en la lista de edificios de la región actual,
            # llama a su método subir_nivel pasando los recursos del jugador y guarda el resultado en salida
            salida = self.mapa.regiones[self.region_actual].edificios[
                self.mapa.regiones[self.region_actual].edificios.index(edificio)
            ].subir_nivel(self.recursos)
            return salida
        else:
            # Si no está, devuelve un mensaje indicando que el edificio no se encuentra en la región
            return f'{edificio} no se encuentra en la región'


    def actualizar_conquista(self) -> None:
        """
        Actualiza la lista de regiones conquistadas por el jugador.

        Returns
        -------
        None
        """

        for coordenada,region in self.mapa.regiones.items():
            if region.get_propietario() == self.usuario and coordenada not in self.conquista:
                self.conquista.append(coordenada)


    def ver_recursos(self) -> list:
        """
        Devuelve una lista con la representación en cadena de los recursos del jugador.

        Returns
        -------
        list of str
            Lista de recursos en formato de cadena.
        """

        recursos_list = []
        for recurso in self.recursos:
            recursos_list.append(str(recurso))
        return recursos_list


    def __eq__(self,other):
        """
        Compara si el usuario del jugador es igual a otro valor.

        Parameters
        ----------
        other : Any
            Valor a comparar con el usuario.

        Returns
        -------
        bool
            True si el usuario es igual a `other`, False en caso contrario.
        """

        if self.usuario == other:
            return True
        else:
            return False
