from jugador import Jugador
from mapa import Mapa
import random

class Partida:
    def __init__(self,id,host,jugadores : list[Jugador] = [],estado: str = 'Esperando',privada=False):
        self.id = id
        self.host = host
        self.jugadores = jugadores
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

    def combatir(self,atacantes_pos : tuple[int, int], defensores_pos: tuple[int, int]):
        ejercito_atk = self.mapa.regiones[atacantes_pos].tropas
        ejercito_def = self.mapa.regiones[defensores_pos].tropas
        texto_lista = []
        while ejercito_atk!=[] and ejercito_def!=[]:    #El bucle se repetirá hasta que uno de los ejercitos esté vacio

            max_tropas = max(len(ejercito_atk), len(ejercito_def)) #Cogemos la longitud del ejercito más grande
            for i in range(max_tropas):  #Repetimos el bucle hasta que lleguemos a la longitud del ejercito más grande
                if i < len(ejercito_atk):
                    texto_lista.append(ejercito_atk[i].atacar(ejercito_atk, ejercito_def))  #La tropa 'i' ataca al ejercito enemigo

                if i < len(ejercito_def):
                    texto_lista.append(ejercito_def[i].atacar(ejercito_def, ejercito_atk))  #La tropa 'i' ataca al ejercito enemigo

        if ejercito_atk==[]:    #Si el ejercito de ataque se ha quedado sin tropas...
            texto_lista.append('El ataque fracasó.')
            return texto_lista,self.estado  
        elif ejercito_def==[]:  #Si el ejercito de defensa se ha quedado sin tropas...
            texto_lista.append(f'Ataque exitoso. \nMoviendo tropas a {defensores_pos}...')
            self.mapa.regiones[defensores_pos].set_propietario(self.turno)
            self.jugadores[self.jugadores.index(self.turno)].mover_batallon(defensores_pos)
            if self.mapa.regiones[defensores_pos].get_es_reino():
                self.estado = 'Finalizada'
                self.ganador = self.turno #El que estaba jugando
                texto_lista.append('Felicidades! Ganastes en madafaking Kingdom Craft')
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




