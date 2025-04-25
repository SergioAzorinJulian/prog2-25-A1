from jugador import Jugador
from mapa import Mapa
import random

class Partida:
    def __init__(self,id,host,jugadores : list = [],estado: str = 'Esperando',privada=False):
        self.id = id
        self.host = host
        self.jugadores = jugadores
        self.estado = estado
        self.privada = privada
    def add_jugador(self,id_jugador,reino):
        self.jugadores.append(Jugador(id_jugador, reino, self.mapa))
        self.jugadores[self.jugadores.index(id_jugador)].establecer_reino()
    def inicializar_mapa(self,size,terrenos):
        map = Mapa(size, size, terrenos)
        nodos = map.crear_nodos()
        conexiones = map.crear_aristas(nodos)
        map.anyadir_terreno(conexiones)
        map.asigna_zonas()
        self.mapa = map
    def inicializar_partida(self):
        self.estado = 'Empezada'
        self.turno = random.choice(self.jugadores).usuario
        return self.turno
    def cancelar_partida(self):
        self.estado = 'Cancelada'
    def estado_jugador(self,id_jugador):
        if self.turno == id_jugador:
            return True
        else:
            return False
    def estado_partida(self): 
        return self.estado
    def cambiar_turno(self):
        if self.turno == self.jugadores[0]:
            self.turno = self.jugadores[1].usuario
        else:
            self.turno = self.jugadores[0].usuario
    def __str__(self):
        str_jugadores = ''
        for jugador in self.jugadores:
            str_jugadores += str(jugador)+'\n'

        return f'Partida de id: {self.id}\nJugadores:\n{str_jugadores}\nEstado: {self.estado}'

