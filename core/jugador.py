from mapa import Mapa
from region import Region
from region_manager import RegionManager
from tipos_recursos import Recurso
'''
PLANTEAMIENTO DEL MENÚ DEL JUGADOR:
    VER MAPA GRÁFICO -> La idea seria mostrar tus zonas con una X, las de nadie con ? y las del enemigo con O (No es prioridad para el viernes)
    ACCEDER A ZONA:
        (SE MUESTRA LA INFORMACIÓN DE LA ZONA), Se actualiza self.region_actual a la zona que esta viendo
        AÑADIR TROPAS -> Se crean tropas en la zona actual, consume recursos:[] (escribir que recurso consume cada tropa el que lo sepa)
        MOVER_TROPA -> Se mueve la tropa indicada a destino, es necesario implementar un método que permita restar cant a la instancia del obj tropa, y otro para sumarlo en caso de que en destino ya esté esa tropa
        MOVER_BATALLÓN -> Lo mismo pero mueve todas las tropas de 1
        CONSTRUIR EDIFICIO -> Construye edificios, escribir aquí edificios y recursos que consumen crearlos -> []
        AÑADIR FAMILIA -> Añade familias, escribir aquí que recurso consume añadir cada familia -> []
        VOLVER
Mover tropa, y mover batallón consumen el turno, si mueves la tropa a territorio enemigo -> COMBATIR o ABORTAR
'''
#Recursos de region debe de ser una lista con los objetos recursos, no un diccionario
#Tropas de region debería de ser una lista con el objeto el cual contenga su cantidad, añadir un método para poder sumar tropas y restar
#Tropas tiene que tener un método que actualiza la cantidad tropas de la instancia y por ende su ataque en función de la vida que perdió ej: vida de 1 caballero 250, actualizar divide la vida total entre 250, redondear el número y esa es la cantidad
class Jugador:
    def __init__(self,usuario,mapa,recursos,conquista = list[tuple[int,int]]):
        self.usuario = usuario
        self.mapa = mapa
        self.conquista = conquista #Se debe actualizar en cada interacción
        self.recursos = recursos
        self.region_actual : tuple[int,int] = None  #La zona que esta consultando el jugador dentro del bucle principal
    def mapa_grafico(self,mapa):
        pass
    def ver_zona(self,region): #Actualiza a su vez la región actual
        pass
    def añadir_tropa(self,tropa,cantidad):
        pass
    def mover_tropa(self,destino : tuple[int,int],tropa,cantidad):
        pass
    def mover_batallon(self,destino : tuple[int,int]):
        pass
    def combatir(destino : tuple[int,int]):
        pass
    def construir_edificio(self,edificio):
        pass
    def añadir_familia(region : tuple[int,int],familia):
        pass
    def actualizar_recursos():
        pass
    def actualizar_conquista():
        pass
