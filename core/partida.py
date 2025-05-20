from jugador import Jugador
from mapa import Mapa
from tropas import *
from mysql_base import add_elo
import random
import pickle_files


class Partida:
    """
    Representa una partida de Kingdom Craft, gestionando jugadores, mapa y estado del juego.

    Atributos
    ---------
    id : str
        Identificador único de la partida.
    privada : bool
        Indica si la partida es privada.
    host : str
        Usuario que creó la partida.
    jugadores : list
        Lista de jugadores en la partida.
    mapa : Mapa
        Objeto que representa el mapa de la partida.
    estado : str
        Estado actual de la partida ('Esperando', 'Empezada', 'Finalizada').
    turno : str
        Usuario al que le corresponde el turno actual.
    """

    def __init__(self, id, host, jugadores: list[Jugador] = None, estado: str = 'Esperando', privada=False):
        """
        Inicializa una nueva instancia de la clase Partida.

        Parámetros
        ----------
        id : str
            Identificador único de la partida.
        host : str
            Usuario que crea la partida.
        jugadores : list[Jugador], opcional
            Lista de jugadores iniciales.
        estado : str, opcional
            Estado inicial de la partida.
        privada : bool, opcional
            Indica si la partida es privada.

        Returns
        -------
        None
        """

        self.id = id
        self.host = host
        self.jugadores = jugadores if jugadores is not None else []
        self.estado = estado
        self.privada = privada
        self.mapa = None
        self.turno = None
        self.ganador = None

    def add_jugador(self,id_jugador,reino):
        """
        Añade un jugador a la partida con el reino especificado.

        Parámetros
        ----------
        id_jugador : str
            Identificador del jugador a añadir.
        reino : str
            Nombre del reino que el jugador controlará.

        Returns
        -------
        None

        Raises
        ------
        Exception
            Si el jugador ya está en la partida o si no se puede añadir.
        """

        self.jugadores.append(Jugador(id_jugador, reino, self.mapa))
        self.jugadores[self.jugadores.index(id_jugador)].establecer_reino()


    def inicializar_mapa(self,size,terrenos):
        """
        Inicializa el mapa de la partida con el tamaño y los terrenos especificados.

        Parámetros
        ----------
        size : int
            Tamaño del mapa (número de filas y columnas).
        terrenos : list or str
            Lista o cadena con los tipos de terrenos a utilizar en el mapa.

        Returns
        -------
        None
        """

        map = Mapa(size, size, terrenos)
        nodos = map.crear_nodos()
        conexiones = map.crear_aristas(nodos)
        map.anyadir_terreno(conexiones)
        map.asigna_zonas()
        self.mapa = map


    def inicializar_partida(self):
        """
        Inicializa la partida, cambiando su estado a 'Empezada' y eligiendo aleatoriamente el primer turno.

        Returns
        -------
        str
            Usuario al que le corresponde el primer turno.
        """

        self.estado = 'Empezada'
        self.turno = random.choice(self.jugadores).usuario
        return self.turno


    def cancelar_partida(self):
        """
        Cancela la partida y realiza las operaciones necesarias para su finalización.

        Returns
        -------
        None

        Raises
        ------
        Exception
            Si ocurre un error al cancelar la partida.
        """

        self.estado = 'Cancelada'


    def estado_jugador(self,id_jugador):
        """
        Devuelve el estado del jugador especificado en la partida.

        Parámetros
        ----------
        id_jugador : str
            Identificador del jugador.

        Returns
        -------
        dict
            Estado del jugador.

        Raises
        ------
        Exception
            Si el jugador no existe en la partida.
        """

        if self.turno == id_jugador:
            return True
        else:
            return False


    def estado_partida(self):
        """
        Devuelve el estado actual de la partida.

        Returns
        -------
        str
            Estado de la partida ('Esperando', 'Empezada', 'Finalizada').
        """

        return self.estado

    
    def cambiar_turno(self):
        """
        Cambia el turno al siguiente jugador en la partida.

        Returns
        -------
        None

        Raises
        ------
        Exception
            Si no hay jugadores o no se puede cambiar el turno.
        """

        jugador = self.jugadores[self.jugadores.index(self.turno)]
        jugador.actualizar_conquista()
        self.producir_edificios(jugador)
        if self.turno == self.jugadores[0]:
            self.turno = self.jugadores[1].usuario
        else:
            self.turno = self.jugadores[0].usuario


    def combatir(self,atacante : str,atacantes_pos : tuple[int, int], defensores_pos: tuple[int, int]):
        """
        Realiza un combate entre dos regiones del mapa.

        Parámetros
        ----------
        atacante : str
            Identificador del jugador atacante.
        atacantes_pos : tuple[int, int]
            Coordenadas de la región atacante.
        defensores_pos : tuple[int, int]
            Coordenadas de la región defensora.

        Returns
        -------
        tuple
            Resultado del combate y estado de la partida.

        Raises
        ------
        Exception
            Si ocurre un error durante el combate.
        """

        # Obtener el propietario de la región defensora
        defensor = self.mapa.regiones[defensores_pos].get_propietario()
        # Obtener las tropas de la región atacante y defensora
        ejercito_atk = self.mapa.regiones[atacantes_pos].tropas
        ejercito_def = self.mapa.regiones[defensores_pos].tropas

        # Buscar tropas de alcance en las regiones vecinas a la región defensora
        tropas_alcance_def : list[Tropa] = []
        tropas_alcance_atk : list[Tropa] = []
        for vecino in self.mapa.get_conexiones()[defensores_pos]:
            propietario = self.mapa.regiones[vecino].get_propietario()
            if propietario == defensor:
                # Si el vecino es del defensor, añadir sus tropas de alcance
                for tropa in self.mapa.regiones[vecino].tropas:
                    if isinstance(tropa, TropaAlcance):
                        tropas_alcance_def.append(tropa)
            elif propietario == atacante:
                # Si el vecino es del atacante, añadir sus tropas de alcance
                for tropa in self.mapa.regiones[vecino].tropas:
                    if isinstance(tropa, TropaAlcance):
                        tropas_alcance_atk.append(tropa)
            
        # Lista para almacenar los mensajes del combate
        texto_lista = []

        # Bucle principal del combate: se repite mientras ambos ejércitos tengan tropas
        while ejercito_atk != [] and ejercito_def != []:
            # Determinar el número máximo de tropas entre todos los grupos
            max_tropas = max(len(ejercito_atk), len(ejercito_def), len(tropas_alcance_atk), len(tropas_alcance_def))
            for i in range(max_tropas):
                # Atacan las tropas del atacante si existen
                if i < len(ejercito_atk):
                    texto_lista.append(ejercito_atk[i].atacar(ejercito_atk, ejercito_def))
                # Atacan las tropas del defensor si existen
                if i < len(ejercito_def):
                    texto_lista.append(ejercito_def[i].atacar(ejercito_def, ejercito_atk))
                # Atacan las tropas de alcance del atacante si existen
                if i < len(tropas_alcance_atk):
                    texto_lista.append(tropas_alcance_atk[i].atacar(ejercito_atk, ejercito_def))
                # Atacan las tropas de alcance del defensor si existen
                if i < len(tropas_alcance_def):
                    texto_lista.append(tropas_alcance_def[i].atacar(ejercito_def, ejercito_atk))

        # Si el ejército atacante se queda sin tropas, el ataque fracasa
        if ejercito_atk == []:
            texto_lista.append('El ataque fracasó.')
            return texto_lista,self.estado  
        # Si el ejército defensor se queda sin tropas, el atacante conquista la región
        elif ejercito_def == []:
            texto_lista.append(f'Ataque exitoso. \nMoviendo tropas a {defensores_pos}...')
            # Cambiar el propietario de la región conquistada
            self.mapa.regiones[defensores_pos].set_propietario(self.turno)
            # Mover el batallón del jugador atacante a la nueva región
            self.jugadores[self.jugadores.index(self.turno)].mover_batallon(defensores_pos)
            # Si la región conquistada es un reino, la partida termina y se otorgan puntos
            if self.mapa.regiones[defensores_pos].get_es_reino():
                self.estado = 'Finalizada'
                self.ganador = self.turno  # El jugador actual es el ganador
                texto_lista.append('Felicidades! Ganastes en madafaking Kingdom Craft')
                text_sql = add_elo(atacante, 25)  # Sumar puntos al ranking
                texto_lista.append(text_sql)
            # Devolver los mensajes del combate y el estado de la partida
            return texto_lista, self.estado


    def producir_edificios(self,jugador : Jugador) -> None:
        for region in self.mapa.regiones.values():
            if region.get_propietario() == jugador.usuario:
                for edificio in region.edificios:
                    edificio.producir(region.recursos,jugador.recursos)

    def __str__(self):
        str_jugadores = ''
        for jugador in self.jugadores:
            str_jugadores += str(jugador)+'\n'

        return f'Partida de id: {self.id}\nJugadores:\n{str_jugadores}\nEstado: {self.estado}'




