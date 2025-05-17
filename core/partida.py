from jugador import Jugador
from mapa import Mapa
from tropas import *
from mysql_base import add_elo
import random

class Partida:
    def __init__(self, id, host, jugadores: list[Jugador] = None, estado: str = 'Esperando', privada=False):
        self.id = id
        self.host = host
        self.jugadores = jugadores if jugadores is not None else []
        self.estado = estado
        self.privada = privada
        self.mapa = None
        self.turno = None
        self.ganador = None

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
        jugador = self.jugadores[self.jugadores.index(self.turno)]
        jugador.actualizar_conquista()
        self.producir_edificios(jugador)
        if self.turno == self.jugadores[0]:
            self.turno = self.jugadores[1].usuario
        else:
            self.turno = self.jugadores[0].usuario

    def combatir(self,atacante : str,atacantes_pos : tuple[int, int], defensores_pos: tuple[int, int]):
        defensor = self.mapa.regiones[defensores_pos].get_propietario()
        ejercito_atk = self.mapa.regiones[atacantes_pos].tropas
        ejercito_def = self.mapa.regiones[defensores_pos].tropas
        #Buscamos Tropas de Alcance en los vecinos de la region
        tropas_alcance_def : list[Tropa] = []
        tropas_alcance_atk : list[Tropa] = []
        for vecino in self.mapa.get_conexiones()[defensores_pos]:
            propietario = self.mapa.regiones[vecino].get_propietario()
            if propietario == defensor:
                for tropa in self.mapa.regiones[vecino].tropas:
                    if isinstance(tropa, TropaAlcance):
                        tropas_alcance_def.append(tropa)
            elif propietario == atacante:
                for tropa in self.mapa.regiones[vecino].tropas:
                    if isinstance(tropa, TropaAlcance):
                        tropas_alcance_atk.append(tropa)
            
            
        texto_lista = []
        while ejercito_atk!=[] and ejercito_def!=[]:    #El bucle se repetirá hasta que uno de los ejercitos esté vacio

            max_tropas = max(len(ejercito_atk), len(ejercito_def), len(tropas_alcance_atk), len(tropas_alcance_def)) #Cogemos la longitud del ejercito más grande
            for i in range(max_tropas):  #Repetimos el bucle hasta que lleguemos a la longitud del ejercito más grande
                if i < len(ejercito_atk):
                    texto_lista.append(ejercito_atk[i].atacar(ejercito_atk, ejercito_def))  #La tropa 'i' ataca al ejercito enemigo

                if i < len(ejercito_def):
                    texto_lista.append(ejercito_def[i].atacar(ejercito_def, ejercito_atk))  #La tropa 'i' ataca al ejercito enemigo
                
                if i < len(tropas_alcance_atk):
                    texto_lista.append(tropas_alcance_atk[i].atacar(ejercito_atk, ejercito_def))
                
                if i < len(tropas_alcance_def):
                    texto_lista.append(tropas_alcance_def[i].atacar(ejercito_atk, ejercito_def))

        if ejercito_atk==[]:    #Si el ejercito de ataque se ha quedado sin tropas...
            texto_lista.append('El ataque fracasó.')
            return texto_lista,self.estado  
        elif ejercito_def==[]:  #Si el ejercito de defensa se ha quedado sin tropas...
            texto_lista.append(f'Ataque exitoso. \nMoviendo tropas a {defensores_pos}...')
            self.jugadores[self.jugadores.index(self.turno)].mover_batallon(defensores_pos)
            if self.mapa.regiones[defensores_pos].get_es_reino():
                self.estado = 'Finalizada'
                self.ganador = self.turno #El que estaba jugando
                texto_lista.append('Felicidades! Ganastes en madafaking Kingdom Craft')
                text_sql = add_elo(atacante,25)
                texto_lista.append(text_sql)
            return texto_lista,self.estado #devolvemos el estado para ver si hay que acabar el bucle de juego
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

