from mapa import Mapa
from region import Region
from region_manager import RegionManager
from recursos import Recurso
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
        
        AÑADIR FAMILIA -> Añade familias, escribir aquí que recurso consume añadir cada familia -> []
            Sistema de generación de familias:
                Se parte de una cantidad inicial (6 o las que se definan) y cada 2 o 3 (o X) turnos se hace "recuento" de recursos del reino;
                es decir, si se tiene comida y agua "de sobra" (superavit) vendra 1 o 2 (o Y) familias nuevas al reino; de igual manera, si para 
                el turno X no tienes suficiente agua y comida para sustentar al pueblo (déficit) se empezaran a ir las familias del reino; pero 
                más paulatinamente, porque sino podría llegar un punto crítico en el que no haya familias, y por tanto tampoco quien trabaje ...
                
        VOLVER
        
Mover tropa, y mover batallón consumen el turno, si mueves la tropa a territorio enemigo -> COMBATIR o ABORTAR
'''

class Jugador:
    def __init__(self,usuario,mapa,recursos : list[Recurso] = [Recurso('madera',100,0),Recurso('agua',100,0),Recurso('piedra',50,0),Recurso('hierro',25,0),Recurso('oro',25,0), \
        Recurso('caza',400,0),Recurso('recoleccion',400,0)] ,conquista : list[tuple[int,int]] = []):
        self.usuario = usuario
        self.mapa = mapa
        self.conquista = conquista #Se debe actualizar en cada interacción
        self.recursos = recursos
        self.region_actual : tuple[int,int] = None  #La zona que esta consultando el jugador dentro del bucle principal
    def mapa_grafico(self,mapa):
        pass
    def ver_zona(self,region : tuple[int,int]): #Actualiza a su vez la región actual
        self.region_actual = region
        return str(self.mapa.regiones[self.region_actual])
    def añadir_tropa(self,tropa,cantidad):
        clases_disponibles={} #Diccionario con Tropas
        for key,value in globals().items():
            if isinstance(value,Tropa):
                clases_disponibles[key.lower()] = value
        if tropa in clases_disponibles.keys():
            pass
        else:
            return f'{tropa} no disponible'
    def mover_tropa(self,destino : tuple[int,int],tropa,cantidad):
        for i in self.mapa.regiones[self.region_actual].tropas:
            if i.nombre == tropa:
                if cantidad < i.cantidad:
                    i -= cantidad
                    if i in self.mapa.regiones[destino].tropas:
                        for y in self.mapa.regiones[destino].tropas:
                            if y.nombre == tropa:
                                y += cantidad
                    else:
            



    def mover_batallon(self,destino : tuple[int,int]):
        pass
    def combatir(destino : tuple[int,int]):
        pass
    def construir_edificio(self,edificio):
        pass
    def añadir_familia(region : tuple[int,int],familia):
        pass
    def regenerar_recursos():
        pass
    def actualizar_conquista():
        pass
    def actualizar_tropas():
        pass
